import pygame as pg
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP
import sys
from random import randint

import constants as cons
from utils import rand_color, rand_screen_pos
from particles import ParticleGenerator
from character import Character


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


class Letters():
    def __init__(self, screen, switch_state_func):
        pg.init()
        pg.font.init()
        self.switch_state = switch_state_func
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        self.char_buffer = [Character(' ', (0, 0), 1)] * 5

        # Is this a separate game?? :)
        self.part_gen = ParticleGenerator(0, 0, 1, self.screen, rand_color())

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
        self.part_gen.update()
        self.check_quit()

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
        if self.buffer_to_string()[-4:] == 'QUIT':
            self.switch_state('MAINMENU')
