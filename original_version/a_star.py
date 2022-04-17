from operator import attrgetter
from node_class import Node


class ASNode(Node):
    methods = ['Manhattan', 'Euclidean', 'Overestimated']  # 'Underestimated'
    heuristic_method = 'Manhattan'

    def __init__(self, x, y, state, step):
        super().__init__(x, y, state, step)
        self.h = 0
        self.f = self.h + self.step
        self.algo = 'a_star'

    def update_f(self):
        if ASNode.heuristic_method == 'Euclidean':
            self.h = ((self.x - ASNode.final_set[0].x) ** 2 + (self.y - ASNode.final_set[0].y) ** 2) ** 0.5
        elif ASNode.heuristic_method == 'Manhattan':
            self.h = abs(self.x - ASNode.final_set[0].x) + abs(self.y - ASNode.final_set[0].y)
        elif ASNode.heuristic_method == 'Overestimated':
            # self.h = ((self.x - ASNode.final_set[0].x) ** 2 + (self.y - ASNode.final_set[0].y) ** 2) ** 0.75
            self.h = (abs(self.x - ASNode.final_set[0].x) + abs(self.y - ASNode.final_set[0].y)) ** 1.5
        elif ASNode.heuristic_method == 'Underestimated':
            self.h = ((self.x - ASNode.final_set[0].x) ** 2 + (self.y - ASNode.final_set[0].y) ** 2) ** (1 / 3)

        self.f = self.h + self.step

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
                cls.nodes[x - 1][y].update_f()
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
                cls.nodes[x + 1][y].update_f()
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
                cls.nodes[x][y - 1].update_f()
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
                cls.nodes[x][y + 1].update_f()
                cls.nodes[x][y + 1].parent = cls.closed_set[-1]
                cls.open_set.append(cls.nodes[x][y + 1])
            elif cls.nodes[x][y + 1].state == 'finish':
                cls.nodes[x][y + 1].parent = cls.closed_set[-1]
                cls.nodes[x][y + 1].step = z + 1
                cls.closed_set.append(cls.nodes[x][y + 1])
                cls.done_with_closed = True

    @classmethod
    def add_to_closed(cls):
        temp = min(cls.open_set, key=attrgetter('f'))
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

    @classmethod
    def change_heuristic(cls):
        cls.heuristic_method = cls.methods[(cls.methods.index(cls.heuristic_method) + 1) % len(cls.methods)]
