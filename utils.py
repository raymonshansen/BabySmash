import pygame as pg
from random import choice, randint


def blur_surface(surface, down, up=0.0):
    width, height = surface.get_size()
    small_size = int(width * down), int(height * down)
    new_size = int(width * up), int(height * up)
    small_surface = pg.transform.smoothscale(surface, small_size)
    surface = pg.transform.smoothscale(small_surface, new_size)
    return surface


def shadow_from_text(text, font, color):
    shadow = font.render(text, True, color)
    return blur_surface(shadow, 0.2)


def rand_color():
    color_string = choice(list(pg.colordict.THECOLORS.keys()))
    return pg.color.Color(color_string)


def rand_screen_pos(screen_width, screen_height, w, h):
    """Given a screen width and height, and object width and height
    return a random position(topleft) that puts the object within
    screen boundaries."""
    return (randint(0, screen_width - w), randint(0, screen_height - h))
