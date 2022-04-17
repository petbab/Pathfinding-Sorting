import pygame as py

py.init()

block = 16
sw, sh = 64, 50
# block = 20
# sw, sh = 80, 50
screen = py.display.set_mode((sw * block, sh * block))
START = [int(sw / 4) - 1, 5]
FINISH = [int(sw / 4) - 1, sh - 16]
font = py.font.SysFont('times new roman', int(block * 1.5))
button_font = py.font.Font('freesansbold.ttf', int(block * 1.5))
s = py.Surface((sw * block, sh * block))
screen_color = (60, 60, 60)
text_color = (255, 255, 255)
clock = py.time.Clock()
fps = 120
