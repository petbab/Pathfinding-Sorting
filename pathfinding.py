from typing import Tuple, List, Dict, Optional
import pygame as py
from constants import *

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


def wall_shape(x: int, y: int, tick: int) -> Block:
    # wall | weighted
    offset = tick * BLOCK_SIZE // (4 * ANIMATION_TICKS)
    return [
        (x + BLOCK_SIZE // 2 - offset, y),
        (x + BLOCK_SIZE // 2 + offset, y),
        (x + BLOCK_SIZE, y + BLOCK_SIZE // 2 - offset),
        (x + BLOCK_SIZE, y + BLOCK_SIZE // 2 + offset),
        (x + BLOCK_SIZE // 2 + offset, y + BLOCK_SIZE),
        (x + BLOCK_SIZE // 2 - offset, y + BLOCK_SIZE),
        (x, y + BLOCK_SIZE // 2 + offset),
        (x, y + BLOCK_SIZE // 2 - offset)
    ]


def start_shape(x: int, y: int) -> Circle:
    # start | finish
    return (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2), BLOCK_SIZE // 2


def open_shape(x: int, y: int, tick: int) -> Circle:
    # open | closed | final
    center = (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2)
    radius = tick * BLOCK_SIZE // (3 * ANIMATION_TICKS)
    return center, radius


class Node:
    def __init__(self, col: int, row: int, steps_from_start: int, state: int = FREE) -> None:
        self.col, self.row = col, row
        self.steps_from_start = steps_from_start  # -1 if undefined
        self.prev_node: Optional[Node] = None
        self.state = state
        self.weight = 1
        # visual attributes:
        self.animation_tick: int = 0
        self.weighted_color = WEIGHTED_COLOR
        self.color = BLOCK_COLORS[state]

    def get_abs_coord(self, grid_pos: Coord) -> Coord:
        x, y = grid_pos
        return self.col * BLOCK_SIZE + x, self.row * BLOCK_SIZE + y

    def set_color(self) -> None:
        self.color = BLOCK_COLORS[self.state]
        r, g, b = WEIGHTED_COLOR
        self.weighted_color = (r + self.weight * WC_MULTIPLIER, g, b)

    def show(self, screen: py.surface.Surface, offset: Coord, block_size: int) -> None:
        x, y = self.get_abs_coord(offset)
        if self.weight != 1:
            vertices = wall_shape(x, y, self.animation_tick)
            py.draw.polygon(screen, self.weighted_color, vertices)
        if self.state == WALL:
            vertices = wall_shape(x, y, self.animation_tick)
            py.draw.polygon(screen, self.color, vertices)
        elif self.state == START or self.state == FINISH:
            center, radius = start_shape(x, y)
            py.draw.circle(screen, self.color, center, radius)
        elif self.state == OPEN or self.state == CLOSED or self.state == FINAL:
            center, radius = open_shape(x, y, self.animation_tick)
            py.draw.circle(screen, self.color, center, radius)
        self.animation_tick = min(ANIMATION_TICKS, self.animation_tick + 1)


class SearchGrid:
    def __init__(self, cols: int, rows: int, offset: Coord,
                 block_size: int, start: Coord, finish: Coord) -> None:
        self.rows, self.cols = rows, cols
        self.x, self.y = offset
        self.block_size = block_size
        self.start = start
        self.finish = finish
        # attributes used in algorithms:
        self.open_nodes: List[Node] = []
        self.closed_nodes: List[Node] = []
        self.final_nodes: List[Node] = []
        self.grid: Grid = []
        self.generate_grid()

    def get_node(self, col: int, row: int) -> Node:
        return self.grid[row][col]

    def reset_grid(self, start: Coord, finish: Coord) -> None:
        self.start = start
        self.finish = finish
        self.open_nodes = []
        self.closed_nodes = []
        self.final_nodes = []
        self.generate_grid()

    def generate_grid(self) -> None:
        self.grid = []
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
            self.grid.append(row_list)

    def show(self, screen: py.surface.Surface) -> None:
        for row in self.grid:
            for node in row:
                node.show(screen, (self.x, self.y), self.block_size)


def main(screen: py.surface.Surface, clock: py.time.Clock) -> None:
    cols, rows = SCREEN_W // BLOCK_SIZE, SCREEN_H // BLOCK_SIZE
    start = (cols // 2, 5)
    finish = (cols // 2, rows - 6)
    search_grid = SearchGrid(cols, rows, (0, 0), BLOCK_SIZE, start, finish)

    while True:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                return

        screen.fill(SCREEN_COLOR)
        search_grid.show(screen)
        py.display.update()


if __name__ == '__main__':
    py.init()
    text_font = py.font.SysFont('times new roman', int(BLOCK_SIZE * 1.5))
    screen_ = py.display.set_mode((SCREEN_W, SCREEN_H))
    clock_ = py.time.Clock()
    main(screen_, clock_)
