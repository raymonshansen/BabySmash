import pygame as pg
from pygame.locals import KEYDOWN
import os
from random import randint, uniform, choice
import constants as cons
from character import Character
from utils import rand_screen_pos


class Image:
    def __init__(self, pos, size, angle, filename):
        self.pos = pos
        orig_image = pg.image.load(filename)
        rotated = pg.transform.rotate(orig_image, angle)
        self.image = pg.transform.scale(rotated, (size, size))
        self.rect = self.image.get_rect().move(pos)


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
        self.number_char = Character()
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
                size = int(640 * uniform(0.1, 0.8))
                pos = rand_screen_pos(cons.WINDOW_WIDTH, cons.WINDOW_HEIGHT, size, size)
                test_rect = pg.Rect(pos, (size, size))
                index = test_rect.collidelist(
                    [thing.get_rect() for thing in self.image_buffer]
                )
                if index == -1:
                    lady = Image(
                        pos,
                        size,
                        rotate,
                        os.path.join("images", choice(["ladybug.png", "butterfly.png", "snail.png"])),
                    )
                    self.image_buffer.append(lady)
                    break
        self.image_buffer.remove(self.number_char)

    def draw_images(self):
        for img in self.image_buffer:
            img.draw(self.screen)

    def draw(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        self.number_char.draw(self.screen)
        self.draw_images()
