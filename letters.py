import pygame as pg
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP
import sys
from random import randint

import constants as cons
from utils import rand_color, rand_screen_pos
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
    def __init__(self, char, pos, size):
        self.char = char
        self.font = pg.font.SysFont('ubuntumono', size, 1)
        self.color = rand_color()
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
        if self.char == ' ':
            return
        if self.fading:
            self.textsurf = self.origsurf.copy()
            self.alphasurf.fill((255, 255, 255, self.alpha))
            self.textsurf.blit(self.alphasurf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
            self.alpha = max(self.alpha - 10, 0)
        screen.blit(self.textsurf, self.pos)

    def fade_out(self):
        self.fading = True


class Game():
    def __init__(self):
        pg.init()
        pg.font.init()
        self.width = cons.WINDOW_WIDTH
        self.height = cons.WINDOW_HEIGHT
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.running = True
        self.char_buffer = [Character(' ', (0, 0), 1)] * 5

        # Is this a separate game?? :)
        self.part_gen = ParticleGenerator(0, 0, 1, self.screen, rand_color())

    def run(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        pg.display.update()
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(cons.FPS)
        pg.quit()
        sys.exit(0)

    def non_overlapping_character(self, char):
        """Return a character_object that does not overlap
        with any of the ones currently in the buffer."""
        while True:
            # TODO: This loop might never terminate!
            size = randint(cons.MIN_LETTER_SIZE, cons.MAX_LETTER_SIZE)
            # Get a random position within the confines of the screen
            pos = rand_screen_pos(cons.WINDOW_WIDTH, cons.WINDOW_HEIGHT, size, size)
            new_char_object = Character(char, pos, size)
            # Chekc for overlapp
            index = new_char_object.get_rect().collidelist(self.buffer_to_rects())
            if index == -1:
                break
        return new_char_object

    def update(self):
        x, y = pg.mouse.get_pos()
        self.part_gen.reposition(x, y)
        for event in pg.event.get():
            if event.type == KEYDOWN:
                char = get_character(event.key)
                new_char = self.non_overlapping_character(char)
                self.update_char_buffer(new_char)
                self.char_buffer[0].fade_out()
            if event.type == MOUSEBUTTONDOWN:
                self.part_gen.active = True
                self.part_gen.set_color(rand_color())
            if event.type == MOUSEBUTTONUP:
                self.part_gen.active = False
                self.part_gen.clear()
        self.running = self.check_quit()
        self.part_gen.update()

    def draw(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        for letter in self.char_buffer:
            letter.draw(self.screen)
        self.part_gen.draw()
        pg.display.update()

    def buffer_to_string(self):
        return ''.join(str(char) for char in self.char_buffer)
    
    def buffer_to_rects(self):
        return [char.get_rect() for char in self.char_buffer]

    def update_char_buffer(self, new_char):
        self.char_buffer.append(new_char)
        self.char_buffer.pop(0)

    def check_quit(self):
        return self.buffer_to_string()[-4:] != 'QUIT'


if __name__ == "__main__":
    game = Game()
    game.run()
