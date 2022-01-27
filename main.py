import pygame as py

BLOCK_SIZE = 16
SCREEN_W, SCREEN_H = 1024, 800
SCREEN_COLOR = (60, 60, 60)
TEXT_COLOR = (255, 255, 255)
FPS = 30


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
