import pygame as pg
import os
import random
from pygame.locals import KEYDOWN

from utils import rand_screen_pos


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ"

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


def load_balloon_sprites(filename, size):
    ret = list()
    sheet = pg.image.load(filename).convert_alpha()
    for idx in range(10):
        ret.append(pg.transform.scale(sheet.subsurface(0, (idx * 500), 500, 500), (size, size)))
    return ret


def get_balloon_char(char, size):
    font = pg.font.SysFont("ubuntumono", size)
    col = pg.color.Color("blue")
    text = font.render(char, True, col)
    alphasurf = pg.Surface(text.get_size(), pg.SRCALPHA)
    text.blit(alphasurf, (0, 0), special_flags=pg.BLEND_RGB_MULT)
    return text


class InGameBallon:
    def __init__(self, char="", size=500, pos=(0, 0), color="blue"):
        self.char = char
        self.rect = pg.Rect(pos, (size, size))
        path = os.path.join("images","balloon", f"balloon_{color}.png")
        self.char_surf = get_balloon_char(char, size//4)
        self.char_rect = pg.Rect(pos, self.char_surf.get_size())
        self.pop_imgs = load_balloon_sprites(path, size)
        self.image = self.pop_imgs[0]
        self.popping = False
        self.dead = False
        self.img_index = 0
        self.char_rect.center = self.rect.center

    def get_rect(self):
        return self.rect

    def get_small_rect(self):
        inflate = int(self.rect.w // 2)
        return self.rect.inflate(-inflate, -inflate)

    def get_mask(self):
        return pg.mask.from_surface(self.image)

    def update(self):
        pass

    def draw(self, screen):
        self.image = self.pop_imgs[0]
        if self.popping:
            self.image = self.pop_imgs[self.img_index]
            self.img_index += 1
            self.dead = self.img_index == len(self.pop_imgs)
        screen.blit(self.image, self.rect.topleft)
        # pg.draw.rect(screen, pg.color.Color("black"), self.get_rect(), 2)
        # pg.draw.rect(screen, pg.color.Color("blue"), self.get_small_rect(), 1)
        if not self.popping:
            screen.blit(self.char_surf, self.char_rect)
            # pg.draw.rect(screen, pg.color.Color("blue"), self.char_rect, 1)


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
        num = random.randint(self.config['min_balloons'], self.config['max_balloons'])
        self.balloons = self.generate_balloons(num)
        path = os.path.join("sounds","balloon", "balloon-pop.wav")
        self.pop_sound = pg.mixer.Sound(path)

    @property
    def balloon_size_range(self):
        return self.config['balloon_size'][0], self.config['balloon_size'][1]

    def new_balloon(self, char):
        size = random.randint(*self.balloon_size_range)
        pos = rand_screen_pos(self.screen.get_width(), self.screen.get_height(), size, size)
        color = random.choice(BALLON_SHEETS)
        return InGameBallon(char, size, pos, color)

    def generate_balloons(self, num):
        letters = random.sample(self.config['alphabet'], num)
        ret = list()
        for i in range(num):
            ba = self.new_balloon(letters[i])
            # import pdb; pdb.set_trace()
            while (ba.get_small_rect().collidelist([b.get_small_rect() for b in ret]) != -1):
                ba = self.new_balloon(letters[i])
            ret.append(ba)
        return ret

    def update(self):
        for balloon in self.balloons:
            balloon.update()
            if balloon.dead:
                self.balloons.remove(balloon)

        for event in pg.event.get():
            if event.type == KEYDOWN:
                key_str = pg.key.name(event.key).upper()
                if key_str == "" or key_str not in self.config['alphabet']:
                    pass
                # Do balloons
                if key_str == "ESCAPE":
                    self.quit()
                for balloon in self.balloons:
                    if key_str == balloon.char:
                        balloon.popping = True
                        self.pop_sound.play()
                if key_str == "SPACE":
                    self.balloons = self.generate_balloons(5)

    def draw(self):
        self.screen.fill(pg.color.Color("skyblue"))
        for balloon in self.balloons:
            balloon.draw(self.screen)
