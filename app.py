import pygame as pg
import sys
import os
import configparser
from letters_game import Letters
from numbers_game import Numbers
from character import Character
from utils import shadow_from_text


class Exit:
    game_name = "QUIT"
    main_menu_name = "EXIT"


class MainMenuBG:
    def __init__(self):
        self.image = pg.image.load(os.path.join("images", "BabySmashBG_static.png"))
        self.rect = pg.Rect(0, 0, 1920, 1080)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class MainMenuHeadline:
    def __init__(self, text="[insert header]"):
        font = pg.font.SysFont("ubuntumono", 120, 1)
        col = pg.color.Color("#466C5A")
        self.textsurf = font.render(text, True, col)

    def draw(self, screen):
        screen.blit(self.textsurf, (50, 50))


class MenuItem:
    def __init__(self, Item, pos):
        self.unsel_text_col = pg.color.Color(215, 220, 215)
        self.sel_text_col = pg.color.Color(255, 250, 255)
        self.selected_col = pg.color.Color(100, 170, 130)
        self.s_col_o = pg.color.Color(100, 170, 130)
        self.unselected_col = pg.color.Color("#365E53")
        self.font = pg.font.SysFont("ubuntumono", 45)
        self.unsel_text = self.font.render(
            Item.main_menu_name, True, self.unsel_text_col
        )
        self.sel_text = self.font.render(Item.main_menu_name, True, self.sel_text_col)
        self.shade_text = shadow_from_text(
            Item.main_menu_name, self.font, pg.color.Color("#333745"), 0.3
        )
        self.state = Item.state_name
        self.config_state_name = Item.config_state_name
        self._setup_rects(pos)
        self.cols = list(zip(range(70, 130, 4), range(140, 200, 4), range(100, 160, 4)))
        self.cols += reversed(self.cols)
        self.cols_i = 0

    def _setup_rects(self, pos):
        self.inner_rect_w = 0
        self.unsel_rect = pg.Rect(pos, (300, 65))
        self.sell_rect = pg.Rect(pos, (400, 65))
        self.sel_border_rect = self.sell_rect.inflate(16, 16)

    @property
    def usel_rect(self):
        return self.unsel_rect

    @property
    def sel_rect(self):
        return self.sel_border_rect

    def update(self):
        self.cols_i += 1
        self.cols_i %= len(self.cols)
        self.s_col_o.r, self.s_col_o.g, self.s_col_o.b = self.cols[self.cols_i]

    def draw(self, screen, selected):
        if selected:
            text_pos = self.sel_border_rect.left + 17, self.sel_border_rect.y + 12
            shade_pos = self.sel_border_rect.left + 15, self.sel_border_rect.y + 14
            pg.draw.rect(screen, self.s_col_o, self.sel_border_rect, 4)
            screen.fill(self.selected_col, self.sell_rect)
            text = self.sel_text
        else:
            text_pos = self.unsel_rect.left + 10, self.unsel_rect.y + 12
            shade_pos = self.unsel_rect.left + 10, self.unsel_rect.y + 12
            screen.fill(self.unselected_col, self.unsel_rect)
            text = self.unsel_text
        screen.blit(self.shade_text, shade_pos)
        screen.blit(text, text_pos)


class MainMenu:
    def __init__(self, screen, switch_state_func, menu_items):
        self.screen = screen
        self.switch_state = switch_state_func
        self.items = list()
        self.sel_idx = 0
        self.headline = MainMenuHeadline("Baby Smash!")
        self.bg = MainMenuBG()
        self.load_menu_items(menu_items)

    def load_menu_items(self, menu_items):
        menu_start_x = 50
        menu_start_y = 120
        item_spacing = 110
        for idx, item in enumerate(menu_items, 1):
            item_pos = menu_start_x, menu_start_y + (item_spacing * idx)
            self.items.append(MenuItem(item, item_pos))

    def up(self):
        self.sel_idx -= 1
        self.sel_idx %= len(self.items)

    def down(self):
        self.sel_idx += 1
        self.sel_idx %= len(self.items)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                print(f"{self.items[self.sel_idx].menu_text} Config")
            elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.down()
            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.up()
            elif event.type == pg.MOUSEMOTION:
                pos = pg.mouse.get_pos()
                for idx, item in enumerate(self.items):
                    if item.usel_rect.collidepoint(pos):
                        self.sel_idx = idx
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for idx, item in enumerate(self.items):
                    if item.sel_rect.collidepoint(pos) and idx == self.sel_idx:
                        self.switch_state(self.items[self.sel_idx].state)
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                self.switch_state(self.items[self.sel_idx].state)

    def update(self):
        self.handle_events()

    def draw(self):
        self.bg.draw(self.screen)
        self.headline.draw(self.screen)
        for idx, menu_item in enumerate(self.items):
            menu_item.draw(self.screen, idx == self.sel_idx)


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

        self.base_state = MainMenu(
            self.screen, self.switch_state, [Letters, Numbers, Exit]
        )
        self.current_state = self.base_state

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
            self.current_state = self.base_state

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
