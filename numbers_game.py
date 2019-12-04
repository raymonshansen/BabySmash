import pygame as pg
from pygame.locals import KEYDOWN
import os
from random import randint, uniform
import constants as cons
from character import Character

class Image():
    def __init__(self, rotation, pos, filename):
        self.rotation = rotation
        self.pos = pos
        self.orig_image = pg.image.load(os.path.join('images', filename))
        self.image = self._rotate(rotation)

    def _rotate(self, angle):
        return pg.transform.rotate(self.orig_image, angle)

    def scale(self, percent):
        current_size = self.image.get_rect().size
        new_size = int(current_size[0] * percent), int(current_size[1] * percent)
        self.image = pg.transform.scale(self.image, new_size)
    
    def get_rect(self):
        return self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.pos)


class Numbers():
    def __init__(self, screen, switch_state_func):
        pg.init()
        pg.font.init()
        self.switch_state = switch_state_func
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        self.number_char = Character(' ', (0, 0), 3)
        self.number_of_images = 0
        self.image_buffer = []

    def update(self):
        for event in pg.event.get():
            if event.type == KEYDOWN:
                key_str = pg.key.name(event.key)
                if key_str in [str(x) for x in range(10)]:
                    number_size = randint(cons.MIN_LETTER_SIZE, cons.MAX_LETTER_SIZE)
                    self.number_char = Character(key_str, (100, 100), number_size)
                    self.number_of_images = int(key_str)
                if key_str == 'q':
                    self.switch_state('MAINMENU')

    def get_non_overlapping_images(self):
        self.image_buffer = [self.number_char]
        for _ in range(self.number_of_images):
            while True:
                # TODO: This loop might never terminate!
                rotate = randint(0, 360)
                pos = randint(0, cons.WINDOW_WIDTH), randint(0, cons.WINDOW_HEIGHT)
                lady = Image(rotate, pos, 'ladybug.png')
                scale = uniform(0.1, 0.3)
                lady.scale(scale)
                # Check for overlapp
                #index = lady.get_rect().collidelist([thing.get_rect() for thing in image_buffer])
                #if index == -1:
                self.image_buffer.append(lady)
                break
        # All images placed without overlapp
        self.image_buffer.remove(self.number_char)
                    
    def draw_images(self):
        self.get_non_overlapping_images()
        for img in self.image_buffer:
            img.draw(self.screen)

    def draw(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        self.number_char.draw(self.screen)
        self.draw_images()
        pg.display.update()
