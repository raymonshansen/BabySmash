import pygame as pg
from pygame.locals import KEYDOWN
import os
from random import randint, uniform, choice
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
    game_name = "NUMBERS"

    @classmethod
    def config_params(cls):
        return {
            "min_number_size": {
                "type": int,
                "validator": lambda num: 16 <= num <= 256,
                "default": 64,
            },
            "max_number_size": {
                "type": int,
                "validator": lambda num: 512 <= num <= 1024,
                "default": 800,
            },
            "random_rotate": {
                "type": lambda x: x.upper() in ["TRUE", "YES", "ON", "1"],
                "validator": lambda x: True,
                "default": False,
            },
        }

    def __init__(self, screen, quit_func, config, g_config):
        pg.init()
        pg.font.init()
        self.config = config
        self.global_config = g_config
        self.quit = quit_func
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        self.number_char = Character()
        self.number_of_images = 0
        self.image_buffer = list()

    @property
    def number_size(self):
        return (self.config["min_number_size"], self.config["max_number_size"])

    @property
    def rotate_angle(self):
        angle = 0
        if self.config["random_rotate"]:
            angle = randint(0, 360)
        return angle

    def update(self):
        for event in pg.event.get():
            if event.type == KEYDOWN:
                key_str = pg.key.name(event.key)
                if key_str in [str(x) for x in range(10)]:
                    size = randint(*self.number_size)
                    self.number_char = Character(key_str, size, (100, 100))
                    self.number_of_images = int(key_str)
                    self.update_image_buffer()
                if key_str == "q":
                    self.quit()

    def update_image_buffer(self):
        self.image_buffer.clear()
        self.image_buffer = [self.number_char]
        for _ in range(self.number_of_images):
            while True:
                # TODO: This loop might never terminate!
                size = int(640 * uniform(0.1, 0.8))
                w, h = self.screen.get_size()
                pos = rand_screen_pos(w, h, size, size)
                test_rect = pg.Rect(pos, (size, size))
                index = test_rect.collidelist(
                    [thing.get_rect() for thing in self.image_buffer]
                )
                if index == -1:
                    lady = Image(
                        pos,
                        size,
                        self.rotate_angle,
                        os.path.join(
                            "images",
                            choice(["ladybug.png", "butterfly.png", "snail.png"]),
                        ),
                    )
                    self.image_buffer.append(lady)
                    break
        self.image_buffer.remove(self.number_char)

    def draw(self):
        self.screen.fill(pg.color.Color("gray98"))
        self.number_char.draw(self.screen)
        for img in self.image_buffer:
            img.draw(self.screen)
