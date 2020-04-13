import pygame as pg
import sys
import os
import configparser
import constants as cons
from letters_game import Letters
from numbers_game import Numbers
from character import Character


class Exit:
    game_name = "QUIT"
    main_menu_name = "EXIT"


class MainMenuHeadline:
    def __init__(self, text="[insert header]"):
        self.rect = pg.Rect(300, 50, (100 * len(text)), 212)
        self.header_buffer = self.generate_headline(text)

    def generate_headline(self, text):
        header_buffer = list()
        start_x = self.rect.left
        for letter in text:
            pos = (start_x, self.rect.top)
            size = 212
            start_x += 95
            color = pg.color.Color("#365E53")
            header_buffer.append(Character(letter, size, pos, color))
        return header_buffer

    def draw(self, screen):
        for char in self.header_buffer:
            char.draw(screen)


class MenuItem:
    def __init__(self, Item):
        self.unsel_text_col = pg.color.Color(215, 220, 215)
        self.sel_text_col = pg.color.Color(255, 250, 255)
        self.selected_col = pg.color.Color(46, 107, 50)
        self.unselected_col = pg.color.Color("#365E53")
        self.font = pg.font.SysFont("ubuntumono", 120, 1)
        self.textsurf = self.font.render(Item.main_menu_name, True, self.unsel_text_col)
        self.menu_text = Item.main_menu_name
        self.state = Item.game_name
        self.selected = False

    def flip_state(self):
        self.selected = not self.selected

    def draw(self, screen, pos):
        x, y = pos
        DI = 10
        HI = 130
        SEL_LEN = 800
        UNSEL_LEN = 600
        if self.selected:
            self.textsurf = self.font.render(self.menu_text, True, self.sel_text_col)
            pg.draw.rect(screen, self.selected_col, (x - DI, y, SEL_LEN, HI), 3)
            pg.draw.rect(
                screen, self.selected_col, (x, y + DI, SEL_LEN - DI - DI, HI - DI - DI)
            )
            pos = (x + DI + DI, y)
        if not self.selected:
            self.textsurf = self.font.render(self.menu_text, True, self.unsel_text_col)
            pg.draw.rect(screen, self.unselected_col, (x - DI, y, UNSEL_LEN, HI))
            pos = (x + DI, y)
        screen.blit(self.textsurf, pos)


class MainMenu:
    def __init__(self, screen, switch_state_func, menu_items):
        self.screen = screen
        self.switch_state = switch_state_func
        self.items = list()
        self.sel_idx = 0
        self.headline = MainMenuHeadline("Baby Smash!")
        self.load_menu_items(menu_items)

    def load_menu_items(self, menu_items):
        for item in menu_items:
            self.items.append(MenuItem(item))
        self.items[self.sel_idx].flip_state()

    def up(self):
        self.items[self.sel_idx].flip_state()
        self.sel_idx -= 1
        self.sel_idx %= len(self.items)
        self.items[self.sel_idx].flip_state()

    def down(self):
        self.items[self.sel_idx].flip_state()
        self.sel_idx += 1
        self.sel_idx %= len(self.items)
        self.items[self.sel_idx].flip_state()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.down()
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.up()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                current_menu_item = self.items[self.sel_idx]
                self.switch_state(current_menu_item.state)

    def update(self):
        self.handle_events()

    def draw(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        self.headline.draw(self.screen)
        menu_start_x = 300
        menu_start_y = 300
        for idx, menu_item in enumerate(self.items, 1):
            item_pos = (menu_start_x, menu_start_y * idx)
            menu_item.draw(self.screen, item_pos)


class Config:
    def __init__(self, config_file_name):
        self.config = configparser.ConfigParser()
        self.config.read(config_file_name)

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
                print("Cannot use")
                fixed_config[k] = v["default"]
        return fixed_config


class Application:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.set_icon_and_window_title()
        self.config = Config("baby_config.ini")

        self.screen = pg.display.set_mode((1920, 1080))
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
            self.current_state = MainMenu(
                self.screen, self.switch_state, [Letters, Numbers, Exit]
            )

    def exit_app(self):
        pg.quit()
        sys.exit()

    def loop(self):
        while not self.done:
            self.current_state.update()
            self.current_state.draw()
            pg.display.update()
            self.clock.tick(60)
        self.exit_app()


if __name__ == "__main__":
    application = Application()
    application.loop()
