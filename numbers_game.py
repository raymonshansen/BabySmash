import pygame as pg
from pygame.locals import KEYDOWN
import os
from random import randint, uniform
import constants as cons
from character import Character
from utils import rand_screen_pos


class Image:
    def __init__(self, rotation, pos, size, filename):
        self.pos = pos
        self.size = size
        self.orig_image = pg.image.load(os.path.join("images", filename))
        self.image = self._rotate(rotation)
        self.image = self._scale((size, size))
        self.rect = pg.Rect(pos, (size, size))

    def _rotate(self, angle):
        return pg.transform.rotate(self.orig_image, angle)

    def _scale(self, size):
        return pg.transform.scale(self.image, size)

    def get_rect(self):
        return self.rect

    def draw(self, screen):
        screen.blit(self.image, self.pos)


class Numbers:
    def __init__(self, screen, switch_state_func):
        pg.init()
        pg.font.init()
        self.switch_state = switch_state_func
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        self.number_char = Character(" ", (0, 0), 3)
        self.number_of_images = 0
        self.image_buffer = list()

    def update(self):
        for event in pg.event.get():
            if event.type == KEYDOWN:
                key_str = pg.key.name(event.key)
                if key_str in [str(x) for x in range(10)]:
                    number_size = randint(cons.MIN_LETTER_SIZE, cons.MAX_LETTER_SIZE)
                    self.number_char = Character(key_str, (100, 100), number_size)
                    self.number_of_images = int(key_str)
                    self.update_image_buffer()
                if key_str == "q":
                    self.switch_state("MAINMENU")

    def update_image_buffer(self):
        self.image_buffer.clear()
        self.image_buffer = [self.number_char]
        for _ in range(self.number_of_images):
            while True:
                # TODO: This loop might never terminate!
                rotate = randint(0, 360)
                size = int(640 * uniform(0.5, 1.0))
                pos = rand_screen_pos(cons.WINDOW_WIDTH, cons.WINDOW_HEIGHT, size, size)
                test_rect = pg.Rect(pos, (size, size))
                index = test_rect.collidelist(
                    [thing.get_rect() for thing in self.image_buffer]
                )
                if index == -1:
                    lady = Image(rotate, pos, size, "ladybug.png")
                    self.image_buffer.append(lady)
                    break
                else:
                    print("overlap")
        self.image_buffer.remove(self.number_char)

    def draw_images(self):
        for img in self.image_buffer:
            img.draw(self.screen)
            pg.draw.rect(self.screen, (200, 200, 200), img.get_rect(), 1)

    def draw(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        self.number_char.draw(self.screen)
        self.draw_images()
