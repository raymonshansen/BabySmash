import pygame as pg
from pygame.locals import KEYDOWN
import os
from random import randint
import constants as cons
from character import Character


class Numbers():
    def __init__(self, screen, switch_state_func):
        pg.init()
        pg.font.init()
        self.switch_state = switch_state_func
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        self.number_char = Character(' ', (0, 0), 3)
        self.image = pg.image.load(os.path.join('images', 'ladybug.png'))

    def update(self):
        for event in pg.event.get():
            if event.type == KEYDOWN:
                key_str = pg.key.name(event.key)
                if key_str in [str(x) for x in range(10)]:
                    number_size = randint(cons.MIN_LETTER_SIZE, cons.MAX_LETTER_SIZE)
                    self.number_char = Character(key_str, (100, 100), number_size)
                if key_str == 'q':
                    self.switch_state('MAINMENU')

    def draw_images(self):
        pass

    def draw(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        self.number_char.draw(self.screen)
        self.draw_images()
        pg.display.update()
