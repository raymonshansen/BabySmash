import pygame as pg
from random import choice, randint


def blur_surface(surface, down, up=1.0):
    width, height = surface.get_size()
    small_size = int(width * down), int(height * down)
    new_size = int(width * up), int(height * up)
    small_surface = pg.transform.smoothscale(surface, small_size)
    surface = pg.transform.smoothscale(small_surface, new_size)
    return surface


def shadow_from_text(text, font, color, down, up=1.0):
    shadow = font.render(text, True, color)
    return blur_surface(shadow, down, up)


def rand_color():
    color_string = choice(list(pg.colordict.THECOLORS.keys()))
    return pg.color.Color(color_string)


def rand_screen_pos(screen_width, screen_height, w, h):
    """Given a screen width and height, and object width and height
    return a random position(topleft) that puts the object within
    screen boundaries."""
    return (randint(0, screen_width - w), randint(0, screen_height - h))


def wrap_text(text, font, width):
    """Wrap text to fit inside a given width when rendered."""
    text_lines = text.replace("\t", "    ").split("\n")

    wrapped_lines = []
    for line in text_lines:
        line = line.rstrip() + " "
        if line == " ":
            wrapped_lines.append(line)
            continue

        # Get the leftmost space ignoring leading whitespace
        start = len(line) - len(line.lstrip())
        start = line.index(" ", start)
        while start + 1 < len(line):
            # Get the next potential splitting point
            next = line.index(" ", start + 1)
            if font.size(line[:next])[0] <= width:
                start = next
            else:
                wrapped_lines.append(line[:start])
                line = line[start + 1 :]
                start = line.index(" ")
        line = line[:-1]
        if line:
            wrapped_lines.append(line)
    return wrapped_lines
