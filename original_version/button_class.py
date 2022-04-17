from operator import attrgetter
import pygame as py
from setup import screen, button_font


class Button:

    def __init__(self, text='', outline=0):
        self.x = 0
        self.y = 0
        self.text = text
        self.w = button_font.render(self.text, True, (0, 0, 0)).get_width() + 75
        self.h = button_font.render(self.text, True, (0, 0, 0)).get_height() + 10
        self.outline = outline

    def show(self, color):
        py.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h))
        py.draw.rect(screen, color, (self.x + self.outline, self.y + self.outline, self.w - 2 * self.outline,
                                     self.h - 2 * self.outline))
        if self.text != '':
            text = button_font.render(self.text, True, (0, 0, 0))
            screen.blit(text, (self.x + (self.w - text.get_width()) / 2,
                               self.y + (self.h - text.get_height()) / 2 + 2))

    @staticmethod
    def align_buttons(buttons, screen_rect):
        if buttons:
            max_w = max(buttons, key=attrgetter('w')).w
            h = buttons[0].h
            gap_size = (screen_rect[3] - len(buttons) * h) / (3 + len(buttons))
            for i in range(len(buttons)):
                buttons[i].w = max_w
                buttons[i].x = int(screen_rect[0] + (screen_rect[2] - max_w) / 2)
                if i == 0:
                    buttons[i].y = screen_rect[1] + 2 * gap_size
                else:
                    buttons[i].y = buttons[i - 1].y + buttons[i - 1].h + gap_size

    def in_button(self, mouse):
        if self.x < mouse[0] < self.x + self.w \
                and self.y < mouse[1] < self.y + self.h:
            return True
        else:
            return False
