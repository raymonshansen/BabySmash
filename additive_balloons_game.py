import pygame as pg
import random
from pathlib import Path
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
        path = Path.cwd() / "images" / "balloon" / f"balloon_{color}.png"
        self.char_surf = get_balloon_char(char, size//8)
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


class AdditiveBalloons:
    state_name = "ADDITIVEBALLOONS"
    config_state_name = "ADDITIVE_BALLONS_CONFIG"
    main_menu_name = "Additive Balloons"

    def __init__(self, screen, quit_func, config):
        pg.init()
        pg.font.init()
        self.screen = screen
        self.quit = quit_func
        self.config = config
        self.buffer = []
        num = random.randint(self.config['min_balloons'], self.config['max_balloons'])
        self.balloons = self.generate_balloons(num)
        path = Path.cwd() / "sounds" / "balloon" / "balloon-pop.wav"
        self.pop_sound = pg.mixer.Sound(path)

    @property
    def balloon_size_range(self):
        return self.config['balloon_size'][0], self.config['balloon_size'][1]
    
    def update_buffer(self,number):
        if len(self.buffer)>3:
            self.buffer.pop(0)
        self.buffer.append(number)

    def new_balloon(self, char):
        size = random.randint(*self.balloon_size_range)
        pos = rand_screen_pos(self.screen.get_width(), self.screen.get_height(), size, size)
        color = random.choice(BALLON_SHEETS)
        return InGameBallon(char, size, pos, color)

    def generate_balloons(self, num):
        sums=[]
        largestSum= self.config["largest_sum"]
        for n in range(0,num):
            firstNumber = random.randint(1,largestSum)
            secondNumber = random.randint(0,largestSum-firstNumber)
            sums.append('%d+%d' % (firstNumber,secondNumber))
        ret = list()
        for i in range(num):
            ba = self.new_balloon(sums[i])
            # import pdb; pdb.set_trace()
            while (ba.get_small_rect().collidelist([b.get_small_rect() for b in ret]) != -1):
                ba = self.new_balloon(sums[i])
            ret.append(ba)
        return ret

    def update(self):
        for balloon in self.balloons:
            balloon.update()
            if balloon.dead:
                self.balloons.remove(balloon)
        if len(self.balloons) < 1:
            self.balloons = self.generate_balloons(5)

        for event in pg.event.get():
            if event.type == KEYDOWN:
                key_str = pg.key.name(event.key).upper()

                # Do balloons
                if key_str == "ESCAPE":
                    self.quit()
                if key_str.isnumeric():
                    self.update_buffer(key_str)

                    for balloon in self.balloons:
                        #print(str(eval(balloon.char)))
                        #print("".join(self.buffer))
                        if str(eval(balloon.char)) in "".join(self.buffer):
                            balloon.popping = True
                            self.pop_sound.play()
                if key_str == "SPACE":
                    self.balloons = self.generate_balloons(5)

    def draw(self):
        self.screen.fill(pg.color.Color("skyblue"))
        for balloon in self.balloons:
            balloon.draw(self.screen)
