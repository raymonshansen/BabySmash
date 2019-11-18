import pygame as pg
from random import choice, randint
import constants as cons


def rand_color():
    color_string = choice(cons.THECOLORS)
    return pg.color.Color(color_string)


def rand_screen_pos(screen_width, screen_height, w, h):
    """Given a screen width and height, and object width and height
    return a random position(topleft) that puts the object within
    screen boundaries."""
    return (randint(0, screen_width - w), randint(0, screen_height - h))
