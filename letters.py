import pygame as pg
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP
import sys
from random import randint

import constants as cons
from utils import rand_color
from particles import ParticleGenerator


def get_character(event_key):
    character = pg.key.name(event_key)
    # Æ, Ø and Å have weird key-names.
    if character == 'world 70':
        character = 'æ'
    if character == 'world 88':
        character = 'ø'
    if character == 'world 69':
        character = 'å'
    if character in cons.ALPHABET:
        return character.upper()
    else:
        return ' '


class Character():
    def __init__(self, char):
        self.char = char
        self.font = pg.font.SysFont('ubuntumono', randint(540, 700), 1)
        self.color = rand_color()
        self.textsurf = self.font.render(self.char, True, rand_color())
        self.pos = self.random_screen_pos()

    def get_rect(self):
        return pg.Rect(self.pos, self.textsurf.get_size())

    def __str__(self):
        return self.char

    def draw(self, screen):
        if self.char == ' ':
            return
        screen.blit(self.textsurf, self.pos)

    def random_screen_pos(self):
        max_width, max_height = self.textsurf.get_size()
        w = cons.WINDOW_WIDTH - max_width
        h = cons.WINDOW_HEIGHT - max_height
        return (randint(0, w), randint(0, h))


class Game():
    def __init__(self):
        pg.init()
        pg.font.init()
        self.width = cons.WINDOW_WIDTH
        self.height = cons.WINDOW_HEIGHT
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.running = True
        self.char_buffer = [Character(' ')] * 4

        # Is this a separate game?? :)
        self.particle_generator = ParticleGenerator(0, 0, 1, self.screen, rand_color())

    def run(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        pg.display.update()
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(cons.FPS)
        pg.quit()
        sys.exit(0)

    def update(self):
        x, y = pg.mouse.get_pos()
        self.particle_generator.reposition(x, y)
        for event in pg.event.get():
            if event.type == KEYDOWN:
                char = get_character(event.key)
                self.update_char_buffer(Character(char))
            if event.type == MOUSEBUTTONDOWN:
                self.particle_generator.active = True
                self.particle_generator.set_color(rand_color())
            if event.type == MOUSEBUTTONUP:
                self.particle_generator.active = False
                self.particle_generator.clear()
        self.running = self.check_quit()
        self.particle_generator.update()

    def draw(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        latest_letter = self.char_buffer[-1]
        latest_letter.draw(self.screen)
        self.particle_generator.draw()
        pg.display.update()

    def buffer_to_string(self):
        return ''.join([str(char) for char in self.char_buffer])

    def update_char_buffer(self, new_char):
        self.char_buffer.append(new_char)
        self.char_buffer.pop(0)

    def check_quit(self):
        return self.buffer_to_string() != 'QUIT'


if __name__ == "__main__":
    game = Game()
    game.run()
