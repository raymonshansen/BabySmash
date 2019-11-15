import pygame as pg
from random import choice
import constants as cons


def rand_color():
    color_string = choice(cons.THECOLORS)
    return pg.color.Color(color_string)
