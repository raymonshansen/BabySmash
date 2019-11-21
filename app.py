import pygame as pg
from random import randint
import sys
import constants as cons
from letters import Letters
from character import Character


class MenuItem():
    def __init__(self, text, info, state):
        self.text = text
        self.color = pg.color.Color(cons.MENU_TEXT_COLOR)
        self.line_color = pg.color.Color(cons.BACKGROUND_COLOR)
        self.font = pg.font.SysFont('ubuntumono', cons.MENU_TEXT_SIZE, 1)
        self.textsurf = self.font.render(text, True, self.color)
        self.info = info
        self.state = state

    def set_selected(self, selected):
        if selected:
            self.font = pg.font.SysFont('ubuntumono', cons.MENU_SELECTED_TEXT_SIZE, 1)
            self.color = pg.color.Color(cons.MENU_SELECTED_COLOR)
            self.line_color = self.color
        else:
            self.font = pg.font.SysFont('ubuntumono', cons.MENU_TEXT_SIZE, 1)
            self.color = pg.color.Color(cons.MENU_TEXT_COLOR)
            self.line_color = pg.color.Color(cons.BACKGROUND_COLOR)
        self.textsurf = self.font.render(self.text, True, self.color)

    def draw(self, screen, pos):
        screen.blit(self.textsurf, pos)
        x, y = pos
        linestart = x - cons.MENU_LINE_PAD, y + cons.MENU_TEXT_SIZE + cons.MENU_LINE_PAD
        lineend = x + cons.MENU_LINE_LENGTH, y + cons.MENU_TEXT_SIZE + cons.MENU_LINE_PAD
        pg.draw.line(screen, self.line_color, linestart, lineend, 2)


class MainMenu():
    def __init__(self, screen, switch_state_func):
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
        header_text = cons.APP_NAME
        total_length = cons.WINDOW_WIDTH - 600
        space_per_letter = total_length // len(header_text)
        start_x = 300
        for letter in header_text:
            pos = (start_x, 50)
            size = randint(100, 200)
            start_x += space_per_letter
            header_buffer.append(Character(letter, pos, size))
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

    def draw(self):
        self.screen.fill(pg.color.Color(cons.BACKGROUND_COLOR))
        for letter in self.headline:
            letter.draw(self.screen)
            pg.draw.line(self.screen, pg.color.Color(cons.MENU_TEXT_COLOR), (200, 250), (cons.WINDOW_WIDTH - 200, 250), 3)
        menu_start_x = 300
        menu_start_y = 300
        for idx, menu_item in enumerate(self.items, 1):
            item_pos = (menu_start_x, menu_start_y * idx)
            menu_item.draw(self.screen, item_pos)


class Application():
    def __init__(self):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode(cons.SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.load_menu()
        self.load_games()
        self.done = False

    def load_menu(self):
        self.main_menu = MainMenu(self.screen, self.switch_state)
        self.current_state = self.main_menu

    def load_games(self):
        self.letters_game = Letters(self.screen, self.switch_state)

    def switch_state(self, state):
        if state == 'MAINMENU':
            self.current_state = self.main_menu
        elif state == 'LETTERS':
            self.current_state = self.letters_game
        elif state == 'QUIT':
            self.done = True

    def exit_app(self):
        pg.quit()
        sys.exit()

    def loop(self):
        while not self.done:
            self.current_state.update()
            self.current_state.draw()
            pg.display.update()
            self.clock.tick(cons.FPS)
        self.exit_app()


if __name__ == "__main__":
    application = Application()
    application.loop()
