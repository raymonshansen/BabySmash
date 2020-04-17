import pygame as pg
from random import choice, randint


def shadow_from_text(text, font, color):
    shadow = font.render(text, True, color)
    width, height = shadow.get_size()
    small_size = int(width * 0.2), int(height * 0.2)
    small = pg.transform.smoothscale(shadow, small_size)
    shadow = pg.transform.smoothscale(small, (width, height))
    return shadow


def rand_color():
    color_string = choice(list(pg.colordict.THECOLORS.keys()))
    return pg.color.Color(color_string)


def rand_screen_pos(screen_width, screen_height, w, h):
    """Given a screen width and height, and object width and height
    return a random position(topleft) that puts the object within
    screen boundaries."""
    return (randint(0, screen_width - w), randint(0, screen_height - h))
