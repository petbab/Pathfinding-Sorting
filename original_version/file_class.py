import random
import time
import math
import pygame as py
from setup import block, sw, sh, screen


class File:

    files = []
    compared = []
    n = 128
    step = 0
    done = False
    color_modes = ["FADE", "RED", "GREEN", "BLUE"]
    color = 0

    def __init__(self, value):
        self.value = value
        self.h = int(((sh - 10) * self.value / File.n + 1) * block)
        self.y = (sh - 9) * block - self.h
        self.w = sw * block / File.n
        self.state = ''
        self.color = ()
        self.get_color()

    def get_color(self):
        t = self.value * 255 / File.n
        if File.color_modes[File.color] == "RED":
            self.color = (255, t/2, t)
        elif File.color_modes[File.color] == "GREEN":
            self.color = (t, 255, t/2)
        elif File.color_modes[File.color] == "BLUE":
            self.color = (t/2, t, 255)
        elif File.color_modes[File.color] == "FADE":
            if self.value <= File.n / 3:
                t = self.value * 765 / File.n
                self.color = (255, t, 255 - t)
            elif self.value <= 2 * File.n / 3:
                t = (self.value - File.n / 3) * 765 / File.n
                self.color = (255 - t, 255, t)
            else:
                t = (self.value - 2 * File.n / 3) * 765 / File.n
                self.color = (t, 255, 255 - t)

    @classmethod
    def reset(cls):
        cls.files = []
        cls.step = 0
        cls.done = False

    @classmethod
    def generate_files(cls):
        for i in range(cls.n):
            cls.files.append(cls(i))
        random.shuffle(cls.files)

    @classmethod
    def show_files(cls, highlight):
        for file in cls.files:
            a = (cls.files.index(file) * file.w, file.y)
            b = ((cls.files.index(file) + 1) * file.w - 1, file.y)
            c = ((cls.files.index(file) + 1) * file.w - 1, file.y - int(block * (sh - 10)/File.n) + 1)
            if highlight:
                if file.state == 'compared':
                    py.draw.rect(screen, (255, 0, 0),
                                 (cls.files.index(file) * file.w, file.y, file.w, file.h))
                    py.draw.polygon(screen, (255, 0, 0), (a, b, c))
                elif file.state == 'pivot':
                    py.draw.rect(screen, (0, 0, 255),
                                 (cls.files.index(file) * file.w, file.y, file.w, file.h))
                    py.draw.polygon(screen, (0, 0, 255), (a, b, c))
                elif file.state == 'closed':
                    py.draw.rect(screen, (0, 255, 0),
                                 (cls.files.index(file) * file.w, file.y, file.w, file.h))
                    py.draw.polygon(screen, (0, 255, 0), (a, b, c))
                else:
                    py.draw.rect(screen, file.color,
                                 (cls.files.index(file) * file.w, file.y, file.w, file.h))
                    py.draw.polygon(screen, file.color, (a, b, c))
            else:
                py.draw.rect(screen, file.color,
                             (cls.files.index(file) * file.w, file.y, file.w, file.h))
                py.draw.polygon(screen, file.color, (a, b, c))

    @classmethod
    def swap_files(cls, i, j):
        File.files[i], File.files[j] = File.files[j], File.files[i]


class BubbleSortClass(File):

    check_round = False
    closed = 0
    complexity = 'O(n2)'

    @classmethod
    def reset(cls):
        cls.files = []
        cls.step = 0
        cls.done = False
        cls.check_round = False
        cls.closed = 0
        for file in cls.compared:
            file.state = ''
        cls.compared = []

    @classmethod
    def sort(cls):
        for file in cls.compared:
            file.state = ''
        cls.compared = [File.files[cls.step], File.files[cls.step + 1]]
        for file in cls.compared:
            file.state = 'compared'
        if File.files[cls.step].value > File.files[cls.step + 1].value:
            cls.swap_files(cls.step, cls.step + 1)
            cls.check_round = True
        if cls.step < cls.n - cls.closed - 2:
            cls.step += 1
        else:
            if not cls.check_round:
                cls.done = True
            else:
                cls.check_round = False
                cls.closed += 1
            cls.step = 0


class InsertionSortClass(File):

    find_step = 1
    insert_step = 1
    on_unordered_file = False
    complexity = 'O(n2)'

    @classmethod
    def reset(cls):
        cls.files = []
        cls.find_step = 1
        cls.done = False
        cls.on_unordered_file = False
        for file in cls.compared:
            file.state = ''
        cls.compared = []

    @classmethod
    def sort(cls):
        if not cls.on_unordered_file:
            cls.find_unordered_file()
        else:
            cls.insert_file()
        if cls.find_step == len(File.files):
            cls.done = True

    @classmethod
    def find_unordered_file(cls):
        for file in cls.compared:
            file.state = ''
        cls.compared = [File.files[cls.find_step], File.files[cls.find_step - 1]]
        for file in cls.compared:
            file.state = 'compared'
        if File.files[cls.find_step].value > File.files[cls.find_step - 1].value:
            cls.find_step += 1
        else:
            cls.on_unordered_file = True
            cls.insert_step = cls.find_step
            if cls.find_step != cls.n - 1:
                cls.find_step += 1

    @classmethod
    def insert_file(cls):
        for file in cls.compared:
            file.state = ''
        if cls.insert_step != 0:
            cls.compared = [File.files[cls.insert_step], File.files[cls.insert_step - 1]]
            for file in cls.compared:
                file.state = 'compared'
            if File.files[cls.insert_step].value < File.files[cls.insert_step - 1].value:
                cls.swap_files(cls.insert_step - 1, cls.insert_step)
                cls.insert_step -= 1
            else:
                cls.on_unordered_file = False
        else:
            cls.on_unordered_file = False


class ShellSortClass(File):

    find_step = 0
    insert_step = 0
    step_size_array = [1, 4, 10, 23, 57]
    step_size = step_size_array[-1]
    on_unordered_file = False
    complexity = 'O(n2)'

    @classmethod
    def reset(cls):
        cls.files = []
        cls.find_step = 0
        cls.insert_step = 0
        cls.step_size = cls.step_size_array[-1]
        cls.done = False
        cls.on_unordered_file = False
        for file in cls.compared:
            file.state = ''
        cls.compared = []

    @classmethod
    def sort(cls):
        time.sleep(0.003)
        if not cls.on_unordered_file:
            cls.find_unordered_file()
        else:
            cls.insert_file()

    @classmethod
    def find_unordered_file(cls):
        for file in cls.compared:
            file.state = ''
        cls.compared = [File.files[cls.find_step], File.files[cls.find_step + cls.step_size]]
        for file in cls.compared:
            file.state = 'compared'
        if File.files[cls.find_step].value > File.files[cls.find_step + cls.step_size].value:
            cls.on_unordered_file = True
            cls.swap_files(cls.find_step, cls.find_step + cls.step_size)
            cls.insert_step = cls.find_step
            if cls.find_step + cls.step_size + 1 < cls.n:
                cls.find_step += 1
        else:
            if cls.find_step + 1 + cls.step_size < File.n:
                cls.find_step += 1
            else:
                cls.find_step = 0
                if cls.step_size != 1:
                    cls.step_size = cls.step_size_array[cls.step_size_array.index(cls.step_size) - 1]
                else:
                    cls.done = True

    @classmethod
    def insert_file(cls):
        for file in cls.compared:
            file.state = ''
        if cls.insert_step - cls.step_size >= 0:
            cls.compared = [File.files[cls.insert_step], File.files[cls.insert_step - cls.step_size]]
            for file in cls.compared:
                file.state = 'compared'
            if File.files[cls.insert_step].value < File.files[cls.insert_step - cls.step_size].value:
                cls.swap_files(cls.insert_step - cls.step_size, cls.insert_step)
                cls.insert_step -= cls.step_size
            else:
                cls.on_unordered_file = False
        else:
            cls.on_unordered_file = False


class MergeSortClass(File):

    merged = True
    start1, finish1, start2, finish2 = 0, 0, 0, 0
    length = 1
    complexity = 'O(nlogn)'

    @classmethod
    def reset(cls):
        cls.files = []
        cls.step = 0
        cls.length = 1
        cls.done = False
        cls.merged = True
        cls.start1, cls.finish1, cls.start2, cls.finish2 = 0, 0, 0, 0
        for file in cls.compared:
            file.state = ''
        cls.compared = []


    @classmethod
    def sort(cls):
        time.sleep(0.005)
        if not cls.merged:
            cls.merge_arrays()
        else:
            if 2 * cls.step * cls.length == cls.n:
                cls.length *= 2
                cls.step = 0
            else:
                cls.merged = False
                cls.start1 = 2 * cls.length * cls.step
                cls.start2 = cls.start1 + cls.length
                cls.finish1 = cls.start2 - 1
                cls.finish2 = cls.start2 + cls.length - 1
        if cls.length == cls.n:
            cls.done = True

    @classmethod
    def merge_arrays(cls):
        for file in cls.compared:
            file.state = ''
        if cls.start1 <= cls.finish1 and cls.start2 <= cls.finish2:
            cls.compared = [File.files[cls.start1], File.files[cls.start2]]
            for file in cls.compared:
                file.state = 'compared'
            if File.files[cls.start1].value < File.files[cls.start2].value:
                cls.start1 += 1
            else:
                File.files.insert(cls.start1, File.files.pop(cls.start2))
                cls.start1 += 1
                cls.finish1 += 1
                cls.start2 += 1
        else:
            cls.merged = True
            cls.step += 1


class QuickSortClass(File):

    complexity = 'O(nlogn)'
    pivot_value = 0
    pivot_index = 0
    i = 0
    j = File.n - 1
    found_interval = True

    @classmethod
    def reset(cls):
        cls.step = 0
        cls.files = []
        cls.done = False
        cls.i = 0
        cls.j = cls.n - 1
        cls.pivot_value = 0
        cls.pivot_index = 0
        cls.found_interval = False
        for file in cls.compared:
            file.state = ''
        cls.compared = []

    @classmethod
    def sort(cls):
        time.sleep(0.005)
        if not cls.found_interval:
            cls.find_interval()
        else:
            cls.partition()

    @classmethod
    def find_interval(cls):
        cls.i = 0
        while cls.i < cls.n - 1 and File.files[cls.i].state == 'closed':
            cls.i += 1
        cls.j = cls.i
        while cls.j < cls.n - 1 and File.files[cls.j + 1].state != 'closed':
            cls.j += 1
        if cls.i == cls.j:
            if cls.i == cls.n - 1:
                cls.done = True
            else:
                File.files[cls.i].state = 'closed'
                cls.find_interval()
        else:
            File.files[cls.i].state = 'pivot'
            cls.pivot_value = File.files[cls.i].value
            cls.pivot_index = cls.i
            cls.pivot_set = True
            cls.i += 1
            cls.found_interval = True

    @classmethod
    def partition(cls):
        for file in cls.compared:
            file.state = ''
        if cls.i <= cls.j:
            cls.compared = [File.files[cls.i], File.files[cls.j]]
            for file in cls.compared:
                file.state = 'compared'
            if File.files[cls.i].value < cls.pivot_value or File.files[cls.j].value > cls.pivot_value:
                if File.files[cls.i].value < cls.pivot_value:
                    cls.i += 1
                if File.files[cls.j].value > cls.pivot_value:
                    cls.j -= 1
            else:
                cls.swap_files(cls.i, cls.j)
        else:
            File.files[cls.pivot_index].state = 'closed'
            cls.swap_files(cls.pivot_index, cls.j)
            cls.pivot_set = False
            cls.found_interval = False


class HeapSortClass(File):

    complexity = 'O(nlogn)'
    heap_length = 1
    first_maxheap_built = False
    maxheap = True
    check_index = 0

    @classmethod
    def reset(cls):
        cls.files = []
        cls.step = 0
        cls.done = False
        cls.heap_length = 1
        cls.first_maxheap_built = False
        cls.maxheap = True
        cls.check_index = 0
        for file in cls.compared:
            file.state = ''
        cls.compared = []

    @classmethod
    def sort(cls):
        time.sleep(0.005)
        if not cls.first_maxheap_built:
            cls.build_first_maxheap()
        elif cls.maxheap:
            if cls.heap_length == 1:
                cls.done = True
            else:
                cls.swap_files(0, cls.heap_length - 1)
                cls.heap_length -= 1
                cls.maxheap = False
                cls.check_index = 0
        else:
            cls.heapify()

    @classmethod
    def heapify(cls):
        if cls.swap_at_check_index(False)[0]:
            cls.check_index = cls.swap_at_check_index(True)[1]
        else:
            cls.maxheap = True

    @classmethod
    def build_first_maxheap(cls):
        if cls.maxheap and cls.heap_length <= cls.n:
            cls.heap_length += 1
            cls.maxheap = False
            cls.check_index = cls.get_parent(cls.heap_length - 1)[1]
        elif not cls.maxheap and cls.heap_length <= cls.n:
            if cls.swap_at_check_index(True)[0]:
                if cls.get_parent(cls.check_index)[0]:
                    cls.check_index = cls.get_parent(cls.check_index)[1]
                else:
                    cls.maxheap = True
            else:
                cls.maxheap = True
        else:
            cls.heap_length = cls.n
            cls.maxheap = True
            cls.first_maxheap_built = True

    @classmethod
    def swap_at_check_index(cls, swap):
        for file in cls.compared:
            file.state = ''
        largest = cls.check_index
        cls.compared = [File.files[largest]]
        if cls.check_index * 2 + 1 < cls.heap_length:
            cls.compared.append(File.files[cls.check_index * 2 + 1])
            if File.files[cls.check_index * 2 + 1].value > File.files[largest].value:
                largest = cls.check_index * 2 + 1
        if cls.check_index * 2 + 2 < cls.heap_length:
            cls.compared.append(File.files[cls.check_index * 2 + 2])
            if File.files[cls.check_index * 2 + 2].value > File.files[largest].value:
                largest = cls.check_index * 2 + 2
        for file in cls.compared:
            file.state = 'compared'
        if largest != cls.check_index:
            if swap:
                cls.swap_files(cls.check_index, largest)
            return [True, largest]
        else:
            return [False]

    @classmethod
    def get_parent(cls, i):
        if i == 0:
            return [False]
        else:
            return [True, math.ceil(i / 2) - 1]


class TimSortClass(File):

    merged = True
    start1, finish1, start2, finish2 = 0, 0, 0, 0
    merge_boundary = 16
    length = merge_boundary
    complexity = 'O(nlogn)'
    find_step = 1
    insert_step = 1
    on_unordered_file = False
    done_with_insertion = False

    @classmethod
    def reset(cls):
        cls.files = []
        cls.find_step = 1
        cls.done = False
        cls.on_unordered_file = False
        cls.length = cls.merge_boundary
        cls.merged = True
        cls.start1, cls.finish1, cls.start2, cls.finish2 = 0, 0, 0, 0
        cls.done_with_insertion = False
        for file in cls.compared:
            file.state = ''
        cls.compared = []

    @classmethod
    def sort(cls):
        if not cls.done_with_insertion:
            if not cls.on_unordered_file:
                cls.find_unordered_file()
            else:
                cls.insert_file()
            if cls.find_step == len(File.files):
                cls.done_with_insertion = True
        else:
            time.sleep(0.005)
            if not cls.merged:
                cls.merge_arrays()
            else:
                if 2 * cls.step * cls.length == cls.n:
                    cls.length *= 2
                    cls.step = 0
                else:
                    cls.merged = False
                    cls.start1 = 2 * cls.length * cls.step
                    cls.start2 = cls.start1 + cls.length
                    cls.finish1 = cls.start2 - 1
                    cls.finish2 = cls.start2 + cls.length - 1
            if cls.length == cls.n:
                cls.done = True

    @classmethod
    def find_unordered_file(cls):
        for file in cls.compared:
            file.state = ''
        cls.compared = [File.files[cls.find_step], File.files[cls.find_step - 1]]
        for file in cls.compared:
            file.state = 'compared'
        if cls.find_step % cls.merge_boundary == 0:
            cls.find_step += 1
        if File.files[cls.find_step].value > File.files[cls.find_step - 1].value:
            cls.find_step += 1
        else:
            cls.on_unordered_file = True
            cls.insert_step = cls.find_step

    @classmethod
    def insert_file(cls):
        for file in cls.compared:
            file.state = ''
        if cls.insert_step % cls.merge_boundary != 0:
            cls.compared = [File.files[cls.insert_step], File.files[cls.insert_step - 1]]
            for file in cls.compared:
                file.state = 'compared'
            if File.files[cls.insert_step].value < File.files[cls.insert_step - 1].value:
                cls.swap_files(cls.insert_step - 1, cls.insert_step)
                cls.insert_step -= 1
            else:
                cls.on_unordered_file = False
        else:
            cls.on_unordered_file = False

    @classmethod
    def merge_arrays(cls):
        for file in cls.compared:
            file.state = ''
        if cls.start1 <= cls.finish1 and cls.start2 <= cls.finish2:
            cls.compared = [File.files[cls.start1], File.files[cls.start2]]
            for file in cls.compared:
                file.state = 'compared'
            if File.files[cls.start1].value < File.files[cls.start2].value:
                cls.start1 += 1
            else:
                File.files.insert(cls.start1, File.files.pop(cls.start2))
                cls.start1 += 1
                cls.finish1 += 1
                cls.start2 += 1
        else:
            cls.merged = True
            cls.step += 1


algorithms_cycle = ['bubble', 'insertion', 'shell', 'merge', 'quick', 'heap', 'tim']

# hash map for algorithms and their classes
algorithms = {
    'bubble': BubbleSortClass,
    'insertion': InsertionSortClass,
    'shell': ShellSortClass,
    'merge': MergeSortClass,
    'quick': QuickSortClass,
    'heap': HeapSortClass,
    'tim': TimSortClass
}


if __name__ == '__main__':
    HeapSortClass.generate_files()
    while HeapSortClass.heap_length < HeapSortClass.n:
        HeapSortClass.build_first_maxheap()
        for file in range(HeapSortClass.heap_length):
            print(HeapSortClass.files[file].value)
        print('------')
