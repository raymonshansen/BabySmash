import pygame as pg
import os
import random
from pygame.locals import KEYDOWN

from utils import rand_screen_pos, rand_color
from character import Character


BALLON_SHEETS = [
    "blue",
    "darkblue",
    "darkgreen",
    "gray",
    "green",
    "lightyellow",
    "orange",
    "pink",
    "purple",
    "red",
    "turquoise",
    "yellow"
    ]

def load_balloon_sprites(filename):
    sheet = pg.image.load(filename).convert_alpha()
    return [sheet.subsurface(0, (idx * 500), 500, 500) for idx in range(10)]


class InGameBallon:
    def __init__(self, char="", size=500, pos=(0, 0), color="blue"):
        print(pos)
        self.character = Character(char, size//2, pos, rand_color())
        path = os.path.join("images\\balloon", f"balloon_{color}.png")
        self.pop_imgs = load_balloon_sprites(path)
        self.image = self.pop_imgs[0]
        self.popping = False
        self.dead = False
        self.img_index = 0
        self.pos = pos

    def update(self):
        pass

    def draw(self, screen):
        self.image = self.pop_imgs[0]
        if self.popping:
            self.image = self.pop_imgs[self.img_index]
            self.img_index += 1
            self.dead = self.img_index == len(self.pop_imgs)
        screen.blit(self.image, self.pos)
        self.character.draw(screen)

class Balloons:
    state_name = "BALLOONS"
    config_state_name = "BALLONS_CONFIG"
    main_menu_name = "Balloons"

    def __init__(self, screen, quit_func, config):
        pg.init()
        pg.font.init()
        self.screen = screen
        self.quit = quit_func
        self.config = config
        self.balloons = self.generate_balloons()
    
    def generate_balloons(self):
        ret = list()
        for i in range(20):
            char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ")
            size = random.randint(50, 501)
            pos = rand_screen_pos(self.screen.get_width(), self.screen.get_height(), size, size)
            color = random.choice(BALLON_SHEETS)
            ret.append(InGameBallon(char, size, pos, color))
        return ret

    def update(self):
        for balloon in self.balloons:
            balloon.update()
            if balloon.dead:
                self.balloons.remove(balloon)

        for event in pg.event.get():
            if event.type == KEYDOWN:
                key_str = pg.key.name(event.key).upper()
                print(key_str)
                if key_str == "" or key_str not in "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ":
                    continue
                # Do balloons
                if key_str == "Q":
                    self.quit()
                if key_str == "P":
                    self.balloons[0].popping = True

    def draw(self):
        self.screen.fill(pg.color.Color("gray98"))
        for balloon in self.balloons:
            balloon.draw(self.screen)

