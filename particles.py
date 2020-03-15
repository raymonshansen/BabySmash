import pygame as pg
from random import uniform, randint

import constants as cons


def random_vector(start, stop):
    return pg.Vector2(1, 1).rotate(uniform(start, stop)).normalize()


class Particle():
    def __init__(self, x, y, size, color, speed, ttl):
        self.pos = pg.Vector2(x, y)
        self.size = (size, size)
        self.color = color
        self.speed = speed
        self.velocity = random_vector(0, 360)
        self.rect = pg.Rect(self.pos, self.size)
        self.ttl = ttl

    def update(self):
        self.rect.center = tuple(self.pos)
        self.pos += self.velocity * self.speed
        self.shrink()

    def shrink(self):
        if self.rect.width < 3:
            self.ttl = 0
        else:
            self.rect = self.rect.inflate(-1, -1)

    @property
    def dead(self):
        return self.ttl <= 0

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)


class NullGenerator:
    def update(self, *args):
        pass
    def draw(self):
        pass

class ParticleGenerator():
    def __init__(self, x, y, rate, screen, color):
        self.pos = pg.Vector2(x, y)
        self.particles = list()
        self.rate = rate
        self.ticker = 0
        self.screen = screen
        self.color = color

    @property
    def time_to_spawn(self):
        if self.ticker >= self.rate:
            self.ticker = 0
            return True
        return False

    def generate_particle(self):
        x = self.pos.x
        y = self.pos.y
        size = randint(cons.PARTICLE_MIN, cons.PARTICLE_MAX)
        speed = 10
        ttl = randint(60, 180)
        return Particle(x, y, size, self.color, speed, ttl)

    def update(self, new_x, new_y):
        self.pos = pg.Vector2(new_x, new_y)
        self.ticker += 1
        if self.time_to_spawn:
            self.particles.append(self.generate_particle())
        for particle in self.particles:
            if particle.dead:
                self.particles.remove(particle)
            else:
                particle.update()

    def draw(self):
        for particle in self.particles:
            particle.draw(self.screen)
