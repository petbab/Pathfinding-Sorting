from typing import Tuple, List, Dict, Optional
import pygame as py

Coord = Tuple[int, int]
Block = List[Coord]
Circle = Tuple[Coord, int]
Color = Tuple[int, int, int]
Grid = List[List['Node']]

FREE, START, FINISH, WALL, OPEN, CLOSED, FINAL = range(7)
SFS_NOT_DEF = -1  # steps from start not defined
BLOCK_COLORS: Dict[int, Color] = {
    FREE: (0, 0, 0),
    START: (0, 255, 0),
    FINISH: (255, 0, 0),
    WALL: (15, 15, 15),
    OPEN: (150, 255, 150),
    CLOSED: (150, 150, 255),
    FINAL: (255, 150, 150)
}
WEIGHTED_COLOR = (30, 30, 30)
WC_MULTIPLIER = 10


def wall_shape(x: int, y: int, block_size: int, tick: float) -> Block:
    # wall | weighted
    return [(x + int(block_size / 4 - tick) + 9, y),
            (x + int(3 * block_size / 4 + tick) - 9, y),
            (x + block_size, y + int(block_size / 4 - tick) + 9),
            (x + block_size, y + int(3 * block_size / 4 + tick) - 9),
            (x + int(3 * block_size / 4 + tick) - 9, y + block_size),
            (x + int(block_size / 4 - tick) + 9, y + block_size),
            (x, y + int(3 * block_size / 4 + tick) - 9),
            (x, y + int(block_size / 4 - tick) + 9)]


def start_shape(x: int, y: int, block_size: int) -> Circle:
    # start | finish
    return (x + int(block_size / 2), y + int(block_size / 2)), int(block_size / 2)


def open_shape(x: int, y: int, block_size: int, tick: float) -> Circle:
    # open | closed | final
    return (x + int(block_size / 2), y + int(block_size / 2)), int(block_size / 3 - 9 + tick)


class Node:
    def __init__(self, col: int, row: int, steps_from_start: int, state: int = FREE) -> None:
        self.col, self.row = col, row
        self.steps_from_start = steps_from_start  # -1 if undefined
        self.prev_node: Optional[Node] = None
        self.state = state
        self.weight = 1
        # visual attributes:
        self.animation_tick: float = 0
        self.weighted_color = WEIGHTED_COLOR
        self.color = BLOCK_COLORS[state]

    def get_abs_coord(self, block_size: int) -> Coord:
        return self.col * block_size, self.row * block_size

    def set_color(self) -> None:
        self.color = BLOCK_COLORS[self.state]
        r, g, b = WEIGHTED_COLOR
        self.weighted_color = (r + self.weight * WC_MULTIPLIER, g, b)

    def show(self, screen: py.Surface, block_size: int) -> None:
        x, y = self.get_abs_coord(block_size)
        if self.weight != 1:
            vertices = wall_shape(x, y, block_size, self.animation_tick)
            py.draw.polygon(screen, self.weighted_color, vertices)
        if self.state == WALL:
            vertices = wall_shape(x, y, block_size, self.animation_tick)
            py.draw.polygon(screen, self.color, vertices)
        elif self.state == START or self.state == FINISH:
            center, radius = start_shape(x, y, block_size)
            py.draw.circle(screen, self.color, center, radius)
        elif self.state == OPEN or self.state == CLOSED or self.state == FINAL:
            center, radius = open_shape(x, y, block_size, self.animation_tick)
            py.draw.circle(screen, self.color, center, radius)
        self.animation_tick = min(10., self.animation_tick + 0.1)


class SearchGrid:
    def __init__(self, rows: int, cols: int, x: int, y: int,
                 block_size: int, start: Coord, finish: Coord) -> None:
        self.rows, self.cols = rows, cols
        self.x, self.y = x, y
        self.block_size = block_size
        self.start = start
        self.finish = finish
        self.grid: Grid = self.generate_grid()
        # attributes used in algorithms:
        self.open_nodes: List[Node] = []
        self.closed_nodes: List[Node] = []
        self.final_nodes: List[Node] = []

    def get_node(self, col: int, row: int) -> Node:
        return self.grid[row][col]

    def generate_grid(self) -> Grid:
        grid: Grid = []
        for row in range(self.rows):
            row_list: List[Node] = []
            for col in range(self.cols):
                if col == 0 or row == 0 or col == self.cols - 1 or row == self.rows - 1:
                    node = Node(col, row, SFS_NOT_DEF, WALL)
                elif (col, row) == self.start:
                    node = Node(col, row, 0, START)
                    self.closed_nodes.append(node)
                elif (col, row) == self.finish:
                    node = Node(col, row, SFS_NOT_DEF, FINISH)
                    self.final_nodes.append(node)
                else:
                    node = Node(col, row, -1)
                row_list.append(node)
            grid.append(row_list)
        return grid

    def show(self, screen: py.Surface, block_size: int) -> None:
        for row in self.grid:
            for node in row:
                node.show(screen, block_size)
