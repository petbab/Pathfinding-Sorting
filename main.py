import pygame as py
from constants import *


def main() -> None:
    py.init()
    text_font = py.font.SysFont('times new roman', int(BLOCK_SIZE * 1.5))
    screen = py.display.set_mode((SCREEN_W, SCREEN_H))
    clock = py.time.Clock()
    while True:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                return

        screen.fill(SCREEN_COLOR)
        py.display.update()


if __name__ == '__main__':
    main()
