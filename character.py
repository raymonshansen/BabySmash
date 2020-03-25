import pygame as pg
from utils import rand_color


class Character:
    def __init__(self, char=" ", size=3, pos=(0, 0)):
        self.char = char[0]
        self.font = pg.font.SysFont("ubuntumono", size, 1)
        self.origsurf = self.font.render(self.char, True, rand_color())
        self.textsurf = self.origsurf.copy()
        self.alphasurf = pg.Surface(self.textsurf.get_size(), pg.SRCALPHA)
        self.alpha = 255
        self.fading = False
        self.pos = pos

    def get_rect(self):
        return pg.Rect(self.pos, self.textsurf.get_size())

    def __str__(self):
        return self.char

    def draw(self, screen):
        if self.fading:
            self.textsurf = self.origsurf.copy()
            self.alphasurf.fill((255, 255, 255, self.alpha))
            self.textsurf.blit(self.alphasurf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
            self.alpha = max(self.alpha - 10, 0)
        screen.blit(self.textsurf, self.pos)

    def fade_out(self):
        self.fading = True
