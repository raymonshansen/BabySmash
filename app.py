import pygame as pg
import sys
import os
import json
from letters_game import Letters
from numbers_game import Numbers
from utils import shadow_from_text, wrap_text

# To fetch screen resolution
from Xlib.display import Display



class Exit:
    state_name = "QUIT"
    config_state_name = ""
    main_menu_name = "Exit"

    @classmethod
    def config_params(cls):
        return {
            "header": "Exit",
            "preview_file": "",
            "info": "Exit the game",
            "config_items": [],
        }

class ScreenRes:
    def __init__(self):
        # Default to 1024x768
        self.height = 768
        self.width = 1024
        self.height, self.width = self.get_resolution()

    def get_resolution(self):
        s = Display(':0').screen()
        return s.height_in_pixels, s.width_in_pixels

    def percent_of_height(self, p):
        return (self.height / 100) * p
    def percent_of_width(self, p):
        return (self.width / 100) * p



class MainMenuBG:
    def __init__(self):
        self.image = pg.image.load(os.path.join("images", "BabySmashBG_static.png"))
        sr = ScreenRes()

        self.rect = pg.Rect(0, 0, sr.height, sr.width)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class MainMenuHeadline:
    def __init__(self, text="[insert header]"):
        font = pg.font.SysFont("ubuntumono", 120, 1)
        col = pg.color.Color("#466C5A")
        self.textsurf = font.render(text, True, col)

    def draw(self, screen):
        screen.blit(self.textsurf, (50, 50))


class MenuItemInfobox:
    def __init__(self, Item, pos):
        self.font = pg.font.SysFont("ubuntumono", 25)
        self.empty = Item.main_menu_name == "Exit"
        self.rect = pg.Rect((457, pos[1] - 8), (500, 650))
        self.image = self._load_preview(Item.config_params()["preview_file"])
        self.border_col = pg.Color(100, 170, 130)
        self.text_color = pg.Color("#333745")
        info_text = wrap_text(Item.config_params()["info"], self.font, 500)
        self.textsurf = self.render_text_list(info_text)
        print(self.image)
        new_h = self.textsurf.get_height() + self.image.get_size()[1] + 50
        self.rect.h = new_h
        self.title_pos = (
            self.rect.x + 10,
            self.rect.y + 10,
        )

    def _load_preview(self, filename):
        img = pg.Surface((10, 10), pg.SRCALPHA)
        if not self.empty:
            img = pg.image.load(os.path.join("images", filename))
            width = self.rect.w - 40
            frac = width / 1920
            height = int(1080 * frac)
            img = pg.transform.scale(img, (width, height))
        return img

    def render_text_list(self, lines):
        rendered = [self.font.render(line, True, self.text_color) for line in lines]
        line_height = self.font.get_linesize()
        width = max(line.get_width() for line in rendered)
        tops = [int(round(i * line_height)) for i in range(len(rendered))]
        height = tops[-1] + self.font.get_height()

        surface = pg.Surface((width, height), pg.SRCALPHA)
        for y, line in zip(tops, rendered):
            surface.blit(line, (0, y))

        return surface

    def set_color(self, col):
        self.border_col = col

    def draw(self, screen):
        if not self.empty:
            screen.blit(self.textsurf, self.title_pos)
            prev_pos = self.rect.x + 20, self.textsurf.get_size()[1] + self.rect.y + 30
            pg.draw.rect(screen, self.border_col, self.rect, 3)
            screen.blit(self.image, prev_pos)


class MenuItem:
    def __init__(self, Item, pos):
        self.font = pg.font.SysFont("ubuntumono", 45)
        self.info = MenuItemInfobox(Item, pos)
        self.unsel_text_col = pg.color.Color(215, 220, 215)
        self.sel_text_col = pg.color.Color(255, 250, 255)
        self.selected_col = pg.color.Color(100, 170, 130)
        self.s_col_o = pg.color.Color(100, 170, 130)
        self.unselected_col = pg.color.Color("#365E53")
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
        self.info.set_color(self.s_col_o)

    def draw(self, screen, selected):
        if selected:
            self.info.draw(screen)
            text_pos = self.sel_border_rect.left + 17, self.sel_border_rect.y + 12
            shade_pos = self.sel_border_rect.left + 15, self.sel_border_rect.y + 14
            pg.draw.rect(screen, self.s_col_o, self.sel_border_rect, 3)
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
        self.screen_res = ScreenRes()
        self.switch_state = switch_state_func
        self.items = list()
        self.sel_idx = 0
        self.headline = MainMenuHeadline("Baby Smash!")
        self.bg = MainMenuBG()
        self.load_menu_items(menu_items)

    def load_menu_items(self, menu_items):
        menu_start_x = self.screen_res.percent_of_width(5)
        menu_start_y = self.screen_res.percent_of_height(5)
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
                self.switch_state(self.items[self.sel_idx].config_state_name)
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
        for menu_item in self.items:
            menu_item.update()

    def draw(self):
        self.bg.draw(self.screen)
        self.headline.draw(self.screen)
        for idx, menu_item in enumerate(self.items):
            menu_item.draw(self.screen, idx == self.sel_idx)


class Config:
    def __init__(self, config_file_name):
        self.file_name = config_file_name
        with open(config_file_name) as fp:
            self.config = json.load(fp)

    def get_game_config(self, game_class):
        return self.config[game_class.config_state_name]


class MenuConfig:
    def __init__(self, screen, quit_func, config_params):
        print(config_params)
        quit_func()


class Application:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.set_icon_and_window_title()
        self.config = Config("baby_config.json")
        self.screen_res = ScreenRes()
        self.screen = pg.display.set_mode((self.screen_res.width, self.screen_res.height))
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
        if state == "NUMBERS_CONFIG":
            self.current_state = MenuConfig(
                self.screen, lambda: self.switch_state(), Numbers.config_params()
            )
        if state == "LETTERS_CONFIG":
            self.current_state = MenuConfig(
                self.screen, lambda: self.switch_state(), Letters.config_params()
            )
        if state == "LETTERS":
            config = self.config.get_game_config(Letters)
            self.current_state = Letters(
                self.screen, lambda: self.switch_state(), config
            )
        elif state == "NUMBERS":
            config = self.config.get_game_config(Numbers)
            self.current_state = Numbers(
                self.screen, lambda: self.switch_state(), config
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
