import pygame as pg
from pygame.locals import KEYDOWN
import os
from config import ConfigWidget
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
    state_name = "NUMBERS"
    config_state_name = "NUMBERS_CONFIG"
    main_menu_name = "Numbers"

    def __init__(self, screen, quit_func, config):
        pg.init()
        pg.font.init()
        self.config = config
        self.quit = quit_func
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        self.number_char = Character()
        self.image_buffer = list()

    @property
    def number_size(self):
        return (self.config["number_size"][0], self.config["number_size"][1])

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
                    self.update_image_buffer(int(key_str))
                if key_str == "q":
                    self.quit()

    def update_image_buffer(self, num):
        self.image_buffer.clear()
        self.image_buffer = [self.number_char]
        for _ in range(num):
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
