import pygame as pg
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from random import randint

from utils import rand_color, rand_screen_pos
from particles import ParticleGenerator, NullGenerator
from character import Character

QUIT_WORD = "QUIT"


class Letters:
    state_name = "LETTERS"
    config_state_name = "LETTERS_CONFIG"
    main_menu_name = "Letters"

    def __init__(self, screen, quit_func, config):
        pg.init()
        pg.font.init()
        self.screen = screen
        self.quit = quit_func
        self.config = config
        self.clock = pg.time.Clock()
        self.running = True
        self.char_buffer = [Character()] * config["buffer_size"]
        self.fading_buffer = []

        # Is this a separate game?? :)
        self.part_gen = NullGenerator()

    @property
    def letter_size(self):
        return self.config["letter_size"][0], self.config["letter_size"][1]

    def non_overlapping_character(self, char):
        """Return a character_object that does not overlap
        with any of the ones currently in the buffer."""
        while True:
            # TODO: This loop might never terminate!
            size = randint(*self.letter_size)
            w, h = self.screen.get_size()
            pos = rand_screen_pos(w, h, size, size)
            new_char_object = Character(char, size, pos)
            index = new_char_object.get_rect().collidelist(self.buffer_to_rects())
            if index == -1:
                break
        return new_char_object

    def update(self):
        x, y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == KEYDOWN:
                char = event.unicode.upper()
                if char == "" or char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ":
                    continue
                new_char = self.non_overlapping_character(char)
                self.update_char_buffer(new_char)
            if event.type == MOUSEBUTTONDOWN:
                self.part_gen = ParticleGenerator(x, y, 1, self.screen, rand_color())
            if event.type == MOUSEBUTTONUP:
                self.part_gen = NullGenerator()
        self.fading_buffer = [c for c in self.fading_buffer if c.alpha]
        self.part_gen.update(x, y)
        self.check_quit()

    def draw(self):
        self.screen.fill(pg.color.Color("gray98"))
        for letter in self.char_buffer + self.fading_buffer:
            letter.draw(self.screen)
        self.part_gen.draw()
        pg.display.update()

    def buffer_to_string(self):
        return "".join(str(c) for c in self.char_buffer)

    def buffer_to_rects(self):
        return [char.get_rect() for char in self.char_buffer]

    def update_char_buffer(self, new_char):
        self.char_buffer.append(new_char)
        ejected_char = self.char_buffer.pop(0)
        ejected_char.fade_speed = 10
        self.fading_buffer.append(ejected_char)

    def check_quit(self):
        if QUIT_WORD in self.buffer_to_string():
            self.quit()
