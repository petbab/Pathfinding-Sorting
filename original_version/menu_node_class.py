import pygame as py
import random
from a_star import ASNode
from setup import block, sw, sh, s


class MenuNode(ASNode):

    closed_set_color = []
    start_color = []
    START = [random.randint(1, sw - 2), random.randint(1, sh - 2)]
    FINISH = [random.randint(1, sw - 2), random.randint(1, sh - 2)]

    for i in range(3):
        c = random.randint(50, 245)
        closed_set_color.append(c)
        start_color.append(c - 50)

    def __init__(self, x, y, state, step):
        super().__init__(x, y, state, step)
        self.tick = 0
        self.expand = 1

    def update_f(self):
        self.h = (abs(self.x - MenuNode.FINISH[0]) + abs(self.y - MenuNode.FINISH[1]))**1.5
        self.f = self.h + self.step

    @classmethod
    def generate_menu_nodes(cls):
        cls.nodes = []
        for i in range(sw):
            temp = []
            for j in range(sh):
                if [i, j] == cls.START:
                    start = cls(i, j, 'start', 0)
                    temp.append(start)
                    cls.open_set.append(start)
                elif [i, j] == cls.FINISH:
                    fin = cls(i, j, 'finish', 0)
                    temp.append(fin)
                    cls.final_set.append(fin)
                elif i == 0 or j == 0 or i == sw - 1 or j == sh - 1:
                    temp.append(cls(i, j, 'wall', 0))
                elif random.choice((1, 0, 0, 0, 0, 0, 0)):
                    temp.append(cls(i, j, 'wall', 0))
                else:
                    temp.append(cls(i, j, '', 0))
                    # if random.choice((1, 0, 0, 0, 0, 0)):
                    #     temp[-1].weight = random.choice((2, 5, 10))
            cls.nodes.append(temp)

    @classmethod
    def solve(cls):
        if cls.open_set and not cls.done_with_closed:
            cls.add_to_closed()
            cls.create_open()
        elif not cls.done_with_final and cls.closed_set[-1].state == 'finish':
            if cls.wait == 100:
                if cls.final_set[-1].parent:
                    cls.create_final_set()
                elif cls.final_set[-1].state == 'finish':
                    cls.final_set[-1].parent = cls.closed_set[-2]
            else:
                cls.wait += 1
        else:
            if cls.wait == 150:
                cls.menu_reset()
            else:
                cls.wait += 1

    @classmethod
    def menu_reset(cls):
        for node in cls.open_set:
            node.state = ''
        for node in cls.closed_set:
            node.state = ''
        for node in cls.final_set:
            node.state = ''
        cls.START = [random.randint(1, sw - 2), random.randint(1, sh - 2)]
        cls.FINISH = [random.randint(1, sw - 2), random.randint(1, sh - 2)]
        cls.nodes[cls.START[0]][cls.START[1]].state = 'start'
        cls.nodes[cls.FINISH[0]][cls.FINISH[1]].state = 'finish'
        cls.open_set = [cls.nodes[cls.START[0]][cls.START[1]]]
        cls.closed_set = []
        cls.final_set = [cls.nodes[cls.FINISH[0]][cls.FINISH[1]]]
        cls.done_with_final = False
        cls.done_with_closed = False
        cls.closed_set_color = []
        cls.start_color = []
        for i in range(3):
            c = random.randint(50, 245)
            cls.closed_set_color.append(c)
            cls.start_color.append(c - 50)
        cls.wait = 0

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
                    py.draw.polygon(s, (30 + 10 * j.weight, 30, 30), (b1, b2, b3, b4, b5, b6, b7, b8))
                if j.state == 'start':
                    py.draw.circle(s, cls.start_color, (int(j.x * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 2))
                elif j.state == 'finish':
                    py.draw.circle(s, (255, 0, 0), (int(j.x * block + block / 2), int(j.y * block + block / 2)),
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
                    py.draw.polygon(s, (15, 15, 15), (b1, b2, b3, b4, b5, b6, b7, b8))
                elif j.state == 'final':
                    py.draw.circle(s, (255, 150, 150),
                                   (int(j.x * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 3 - 9 + j.tick))
                elif j.state == 'closed':
                    py.draw.circle(s, cls.closed_set_color,
                                   (int(j.x * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 3 - 10 + j.tick))
                elif j.state == 'open':
                    py.draw.circle(s, (150, 255, 150),
                                   (int(j.x * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 3 - 10 + j.tick))
                if j.tick < 10:
                    j.tick += 0.1
