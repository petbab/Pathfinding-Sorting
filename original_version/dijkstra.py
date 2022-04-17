from operator import attrgetter
import pygame as py
from node_class import Node
from setup import block, sw, screen


class DijNode(Node):

    def __init__(self, x, y, state, step):
        super().__init__(x, y, state, step)
        self.algo = 'dijkstra'

    @classmethod
    def show_nodes(cls):
        for i in cls.nodes:
            for j in i:
                if j.weight != 1:
                    b1 = ((sw / 2 + j.x) * block + int(block / 4 - j.tick) + 9, j.y * block)
                    b2 = ((sw / 2 + j.x) * block + int(3 * block / 4 + j.tick) - 9, j.y * block)
                    b3 = ((sw / 2 + j.x) * block + block, j.y * block + int(block / 4 - j.tick) + 9)
                    b4 = ((sw / 2 + j.x) * block + block, j.y * block + int(3 * block / 4 + j.tick) - 9)
                    b5 = ((sw / 2 + j.x) * block + int(3 * block / 4 + j.tick) - 9, j.y * block + block)
                    b6 = ((sw / 2 + j.x) * block + int(block / 4 - j.tick) + 9, j.y * block + block)
                    b7 = ((sw / 2 + j.x) * block, j.y * block + int(3 * block / 4 + j.tick) - 9)
                    b8 = ((sw / 2 + j.x) * block, j.y * block + int(block / 4 - j.tick) + 9)
                    py.draw.polygon(screen, (30 + 10 * j.weight, 30, 30), (b1, b2, b3, b4, b5, b6, b7, b8))
                if j.state == 'start':
                    py.draw.circle(screen, (0, 255, 0), (int((sw / 2 + j.x) * block + block / 2),
                                                         int(j.y * block + block / 2)), int(block / 2))
                elif j.state == 'finish':
                    py.draw.circle(screen, (255, 0, 0), (int((sw / 2 + j.x) * block + block / 2),
                                                         int(j.y * block + block / 2)), int(block / 2))
                elif j.state == 'wall':
                    b1 = ((sw / 2 + j.x) * block + int(block / 4 - j.tick) + 9, j.y * block)
                    b2 = ((sw / 2 + j.x) * block + int(3 * block / 4 + j.tick) - 9, j.y * block)
                    b3 = ((sw / 2 + j.x) * block + block, j.y * block + int(block / 4 - j.tick) + 9)
                    b4 = ((sw / 2 + j.x) * block + block, j.y * block + int(3 * block / 4 + j.tick) - 9)
                    b5 = ((sw / 2 + j.x) * block + int(3 * block / 4 + j.tick) - 9, j.y * block + block)
                    b6 = ((sw / 2 + j.x) * block + int(block / 4 - j.tick) + 9, j.y * block + block)
                    b7 = ((sw / 2 + j.x) * block, j.y * block + int(3 * block / 4 + j.tick) - 9)
                    b8 = ((sw / 2 + j.x) * block, j.y * block + int(block / 4 - j.tick) + 9)
                    py.draw.polygon(screen, (15, 15, 15), (b1, b2, b3, b4, b5, b6, b7, b8))
                elif j.state == 'final':
                    py.draw.circle(screen, (255, 150, 150),
                                   (int((sw / 2 + j.x) * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 3 - 9 + j.tick))
                elif j.state == 'closed':
                    py.draw.circle(screen, (150, 150, 255),
                                   (int((sw / 2 + j.x) * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 3 - 10 + j.tick))
                elif j.state == 'open':
                    py.draw.circle(screen, (150, 255, 150),
                                   (int((sw / 2 + j.x) * block + block / 2), int(j.y * block + block / 2)),
                                   int(block / 3 - 10 + j.tick))
                if j.tick < 10:
                    j.tick += 0.1

    @classmethod
    def solve(cls):
        if cls.open_set and not cls.done_with_closed:
            cls.add_to_closed()
            cls.create_open()
        elif not cls.done_with_final and cls.closed_set[-1].state == 'finish':
            if cls.wait == 100:
                cls.create_final_set()
            else:
                cls.wait += 1

    @classmethod
    def create_open(cls):
        x = cls.closed_set[-1].x
        y = cls.closed_set[-1].y
        z = cls.closed_set[-1].step
        if x - 1 >= 0:
            if cls.nodes[x - 1][y].state == '' or \
                    (cls.nodes[x - 1][y].state == 'open' and cls.nodes[x - 1][y].step > z + cls.nodes[x - 1][y].weight):
                cls.nodes[x - 1][y].tick = 0
                cls.nodes[x - 1][y].state = 'open'
                cls.nodes[x - 1][y].step = z + cls.nodes[x - 1][y].weight
                cls.nodes[x - 1][y].parent = cls.closed_set[-1]
                cls.open_set.append(cls.nodes[x - 1][y])
            elif cls.nodes[x - 1][y].state == 'finish':
                cls.nodes[x - 1][y].parent = cls.closed_set[-1]
                cls.nodes[x - 1][y].step = z + 1
                cls.closed_set.append(cls.nodes[x - 1][y])
                cls.done_with_closed = True
        if x + 1 < len(cls.nodes):
            if cls.nodes[x + 1][y].state == '' or \
                    (cls.nodes[x + 1][y].state == 'open' and cls.nodes[x + 1][y].step > z + cls.nodes[x + 1][y].weight):
                cls.nodes[x + 1][y].tick = 0
                cls.nodes[x + 1][y].state = 'open'
                cls.nodes[x + 1][y].step = z + cls.nodes[x + 1][y].weight
                cls.nodes[x + 1][y].parent = cls.closed_set[-1]
                cls.open_set.append(cls.nodes[x + 1][y])
            elif cls.nodes[x + 1][y].state == 'finish':
                cls.nodes[x + 1][y].parent = cls.closed_set[-1]
                cls.nodes[x + 1][y].step = z + 1
                cls.closed_set.append(cls.nodes[x + 1][y])
                cls.done_with_closed = True
        if y - 1 >= 0:
            if cls.nodes[x][y - 1].state == '' or \
                    (cls.nodes[x][y - 1].state == 'open' and cls.nodes[x][y - 1].step > z + cls.nodes[x][y - 1].weight):
                cls.nodes[x][y - 1].tick = 0
                cls.nodes[x][y - 1].state = 'open'
                cls.nodes[x][y - 1].step = z + cls.nodes[x][y - 1].weight
                cls.nodes[x][y - 1].parent = cls.closed_set[-1]
                cls.open_set.append(cls.nodes[x][y - 1])
            elif cls.nodes[x][y - 1].state == 'finish':
                cls.nodes[x][y - 1].parent = cls.closed_set[-1]
                cls.nodes[x][y - 1].step = z + 1
                cls.closed_set.append(cls.nodes[x][y - 1])
                cls.done_with_closed = True
        if y + 1 < len(cls.nodes[x]):
            if cls.nodes[x][y + 1].state == '' or \
                    (cls.nodes[x][y + 1].state == 'open' and cls.nodes[x][y + 1].step > z + cls.nodes[x][y + 1].weight):
                cls.nodes[x][y + 1].tick = 0
                cls.nodes[x][y + 1].state = 'open'
                cls.nodes[x][y + 1].step = z + cls.nodes[x][y + 1].weight
                cls.nodes[x][y + 1].parent = cls.closed_set[-1]
                cls.open_set.append(cls.nodes[x][y + 1])
            elif cls.nodes[x][y + 1].state == 'finish':
                cls.nodes[x][y + 1].parent = cls.closed_set[-1]
                cls.nodes[x][y + 1].step = z + 1
                cls.closed_set.append(cls.nodes[x][y + 1])
                cls.done_with_closed = True

    @classmethod
    def add_to_closed(cls):
        temp = min(cls.open_set, key=attrgetter('step'))
        cls.open_set.remove(temp)
        if temp.state != 'start' and temp.state != 'finish':
            temp.state = 'closed'
        cls.closed_set.append(temp)

    @classmethod
    def create_final_set(cls):
        cls.final_set.append(cls.final_set[-1].parent)
        if cls.final_set[-1].state == 'start':
            cls.done_with_final = True
        else:
            cls.final_set[-1].state = 'final'


if __name__ == '__main__':
    node = DijNode(1, 1, '', 0)
    print(node.parent)
