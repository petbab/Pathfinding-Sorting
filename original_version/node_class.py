import pygame as py
from setup import block, sw, sh, screen, START, FINISH


class Node:

    done_with_final = False
    done_with_closed = False
    nodes = []
    step = 0
    closed_set = []
    final_set = []
    open_set = []
    wait = 0

    def __init__(self, x, y, state, step):
        self.x = x
        self.y = y
        self.state = state
        self.step = step
        self.tick = 0
        self.parent = None
        self.weight = 1

    @classmethod
    def reset_nodes(cls):
        cls.done_with_final = False
        cls.done_with_closed = False
        cls.nodes = []
        cls.step = 0
        cls.closed_set = []
        cls.final_set = []
        cls.open_set = []
        cls.wait = 0

    @classmethod
    def generate_nodes(cls):
        for i in range(int(sw / 2)):
            temp = []
            for j in range(sh - 9):
                if [i, j] == START:
                    start = cls(i, j, 'start', 0)
                    temp.append(start)
                    cls.open_set = [start]
                elif [i, j] == FINISH:
                    fin = cls(i, j, 'finish', 0)
                    temp.append(fin)
                    cls.final_set = [fin]
                elif i == 0 or j == 0 or i == int(sw / 2) - 1 or j == sh - 10:
                    temp.append(cls(i, j, 'wall', 0))
                else:
                    temp.append(cls(i, j, '', 0))
            cls.nodes.append(temp)

    @classmethod
    def show_nodes(cls):
        for i in cls.nodes:
            for j in i:
                if j.weight != 1:
                    b1 = (j.x * block + int(block / 4 - j.tick) + 9, j.y * block)
                    b2 = (j.x * block + int(3 * block / 4 + j.tick) - 9, j.y * block)
                    b3 = (j.x * block + block, j.y * block + int(block / 4 - j.tick) + 9)
                    b4 = (j.x * block + block, j.y * block + int(3 * block / 4 + j.tick) - 9)
                    b5 = (j.x * block + int(3 * block / 4 + j.tick) - 9, j.y * block + block)
                    b6 = (j.x * block + int(block / 4 - j.tick) + 9, j.y * block + block)
                    b7 = (j.x * block, j.y * block + int(3 * block / 4 + j.tick) - 9)
                    b8 = (j.x * block, j.y * block + int(block / 4 - j.tick) + 9)
                    py.draw.polygon(screen, (30 + 10 * j.weight, 30, 30), (b1, b2, b3, b4, b5, b6, b7, b8))
                if j.state == 'start':
                    py.draw.circle(screen, (0, 255, 0), (int(j.x * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 2))
                elif j.state == 'finish':
                    py.draw.circle(screen, (255, 0, 0), (int(j.x * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 2))
                elif j.state == 'wall':
                    b1 = (j.x * block + int(block / 4 - j.tick) + 9, j.y * block)
                    b2 = (j.x * block + int(3 * block / 4 + j.tick) - 9, j.y * block)
                    b3 = (j.x * block + block, j.y * block + int(block / 4 - j.tick) + 9)
                    b4 = (j.x * block + block, j.y * block + int(3 * block / 4 + j.tick) - 9)
                    b5 = (j.x * block + int(3 * block / 4 + j.tick) - 9, j.y * block + block)
                    b6 = (j.x * block + int(block / 4 - j.tick) + 9, j.y * block + block)
                    b7 = (j.x * block, j.y * block + int(3 * block / 4 + j.tick) - 9)
                    b8 = (j.x * block, j.y * block + int(block / 4 - j.tick) + 9)
                    py.draw.polygon(screen, (15, 15, 15), (b1, b2, b3, b4, b5, b6, b7, b8))
                elif j.state == 'final':
                    py.draw.circle(screen, (255, 150, 150),
                                   (int(j.x * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 3 - 9 + j.tick))
                elif j.state == 'closed':
                    py.draw.circle(screen, (150, 150, 255),
                                   (int(j.x * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 3 - 10 + j.tick))
                elif j.state == 'open':
                    py.draw.circle(screen, (150, 255, 150),
                                   (int(j.x * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 3 - 10 + j.tick))
                if j.tick < 10:
                    j.tick += 0.1
