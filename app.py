import pygame as pg
from random import randint, choice
import sys
import os
import configparser
import constants as cons
from letters_game import Letters
from numbers_game import Numbers
from character import Character
from utils import rand_screen_pos


class MainMenuBackground:
    def __init__(self, screen):
        self.characters = list()
        self.screen = screen

    def spawn_letter(self):
        size = randint(100, 150)
        w, h = self.screen.get_size()
        pos = tuple(pg.Vector2(rand_screen_pos(w, h, size, size)))
        alpha = randint(25, 40)
        char = choice("ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ")
        new_letter = Character(char, size, pos)
        new_letter.set_fade_speed(0)
        new_letter.set_alpha(alpha)
        direction = pg.Vector2(1, 1).rotate(float(randint(1, 360))).normalize()
        direction *= randint(1, 2)
        return new_letter, direction

    def update(self):
        for tup in self.characters:
            letter, direction = tup
            letterpos = pg.Vector2(letter.get_rect().topleft)
            new_pos = letterpos + direction
            letter.move(tuple(new_pos))
            notonscreen = letter.get_rect().colliderect(self.screen.get_rect()) == 0
            invisible = letter.alpha == 0
            if notonscreen or invisible:
                self.characters.remove(tup)

        if len(self.characters) < 10:
            self.characters.append(self.spawn_letter())

    def draw(self):
        for tup in self.characters:
            letter, direction = tup
            letter.draw(self.screen)


class MenuItem:
    def __init__(self, text, info, state):
        self.text = text
        self.color = pg.color.Color(cons.MENU_TEXT_COLOR)
        self.line_color = pg.color.Color(cons.BACKGROUND_COLOR)
        self.font = pg.font.SysFont("ubuntumono", cons.MENU_TEXT_SIZE, 1)
        self.textsurf = self.font.render(text, True, self.color)
        self.info = info
        self.state = state

    def set_selected(self, selected):
        if selected:
            self.font = pg.font.SysFont("ubuntumono", cons.MENU_SELECTED_TEXT_SIZE, 1)
            self.color = pg.color.Color(cons.MENU_SELECTED_COLOR)
            self.line_color = self.color
        else:
            self.font = pg.font.SysFont("ubuntumono", cons.MENU_TEXT_SIZE, 1)
            self.color = pg.color.Color(cons.MENU_TEXT_COLOR)
            self.line_color = pg.color.Color(cons.BACKGROUND_COLOR)
        self.textsurf = self.font.render(self.text, True, self.color)

    def draw(self, screen, pos):
        screen.blit(self.textsurf, pos)
        x, y = pos
        linestart = x - cons.MENU_LINE_PAD, y + cons.MENU_TEXT_SIZE + cons.MENU_LINE_PAD
        lineend = (
            x + cons.MENU_LINE_LENGTH,
            y + cons.MENU_TEXT_SIZE + cons.MENU_LINE_PAD,
        )
        pg.draw.line(screen, self.line_color, linestart, lineend, 2)


class MainMenu:
    def __init__(self, screen, switch_state_func):
        self.bg = MainMenuBackground(screen)
        self.screen = screen
        self.switch_state = switch_state_func
        self.items = list()
        self.selected = 0
        self.headline = self.generate_headline()
        self.load_menu_items()

    def load_menu_items(self):
        for menu_text, menu_info, state in cons.MENU_ITEM_TEXTS:
            self.items.append(MenuItem(menu_text, menu_info, state))
        self.items[self.selected].set_selected(True)

    def up(self):
        self.items[self.selected].set_selected(False)
        self.selected -= 1
        self.selected %= len(self.items)
        self.items[self.selected].set_selected(True)

    def down(self):
        self.items[self.selected].set_selected(False)
        self.selected += 1 % len(self.items)
        self.selected %= len(self.items)
        self.items[self.selected].set_selected(True)

    def generate_headline(self):
        header_buffer = list()
        header_text = "BabySmash"
        total_length = cons.WINDOW_WIDTH - 600
        space_per_letter = total_length // len(header_text)
        start_x = 300
        for letter in header_text:
            pos = (start_x, 50)
            size = randint(100, 200)
            start_x += space_per_letter
            header_buffer.append(Character(letter, size, pos))
        return header_buffer

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.down()
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.up()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                current_menu_item = self.items[self.selected]
                self.switch_state(current_menu_item.state)

    def update(self):
        self.handle_events()
        self.bg.update()

    def draw(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        self.bg.draw()
        for letter in self.headline:
            letter.draw(self.screen)
            pg.draw.line(
                self.screen,
                pg.color.Color(cons.MENU_TEXT_COLOR),
                (200, 250),
                (cons.WINDOW_WIDTH - 200, 250),
                3,
            )
        menu_start_x = 300
        menu_start_y = 300
        for idx, menu_item in enumerate(self.items, 1):
            item_pos = (menu_start_x, menu_start_y * idx)
            menu_item.draw(self.screen, item_pos)


class Config:
    def __init__(self, config_file_name):
        self.config = configparser.ConfigParser()
        self.config.read(config_file_name)
        self.global_config = self._get_global_config()

    def _get_global_config(self):
        return dict([("screen_w", 1920), ("screen_h", 1080), ("fps", 30)])

    def get_game_config(self, game_class):
        config_definition = game_class.config_params()
        from_file = self.config[game_class.game_name]
        fixed_config = dict()
        for k, v in config_definition.items():
            converter = v["type"]
            stored_string_value = from_file[k]
            try:
                converted = converter(stored_string_value)
                if v["validator"](converted):
                    fixed_config[k] = converted
            except ValueError:
                # TODO: Notify user likely set incompatible config values!
                fixed_config[k] = v["default"]
        return fixed_config


class Application:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.set_icon_and_window_title()
        self.config = Config("baby_config.ini")
        w = self.config.global_config["screen_w"]
        h = self.config.global_config["screen_h"]
        self.screen = pg.display.set_mode((w, h))
        self.clock = pg.time.Clock()
        self.done = False
        self.switch_state()

    def set_icon_and_window_title(self):
        icon = pg.image.load(os.path.join("images", "BabySmashIcon.png"))
        pg.display.set_icon(icon)
        pg.display.set_caption("BabySmash")

    def switch_state(self, state=None):
        if state == "LETTERS":
            fixed_config = self.config.get_game_config(Letters)
            self.current_state = Letters(
                self.screen, lambda: self.switch_state(), fixed_config
            )
        elif state == "NUMBERS":
            fixed_config = self.config.get_game_config(Numbers)
            self.current_state = Numbers(
                self.screen, lambda: self.switch_state(), fixed_config
            )
        elif state == "QUIT":
            self.done = True
        else:
            self.current_state = MainMenu(self.screen, self.switch_state)

    def exit_app(self):
        pg.quit()
        sys.exit()

    def loop(self):
        while not self.done:
            self.current_state.update()
            self.current_state.draw()
            pg.display.update()
            self.clock.tick(self.config.global_config["fps"])
        self.exit_app()


if __name__ == "__main__":
    application = Application()
    application.loop()
