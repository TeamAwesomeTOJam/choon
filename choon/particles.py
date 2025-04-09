from random import uniform

import pygame

from choon.constants import TILE_WIDTH


class pp:

    def __init__(self, x, y, vx, vy, t, c):
        self.x = x
        self.y = y
        self.ox = x
        self.oy = y
        self.vx = vx
        self.vy = vy
        self.t = t
        self.c = c


class Particles:

    def __init__(self, world, gravity=0.5):
        self.CELLSIZE = TILE_WIDTH
        self.PSIZE = 3
        self.pps = []
        self.gravity = gravity
        self.world = world

    def rc(self, c, rand):
        if rand == False:
            return c
        return (
         max(min(c[0] + uniform(-50, 50), 255), 0),
         max(min(c[1] + uniform(-50, 50), 255), 0),
         max(min(c[2] + uniform(-50, 50), 255), 0))

    def addEffect(self, x, y, c, STEP=4, rand=True):
        for i in range(0, self.CELLSIZE, STEP):
            for j in range(0, self.CELLSIZE, STEP):
                self.pps.append(pp(x + i, y + j, uniform(-6, 6), uniform(-12, 3), uniform(30, 50), self.rc(c, rand)))

    def tick(self):
        for p in self.pps:
            p.ox = p.x
            p.oy = p.y
            p.y += p.vy
            p.x += p.vx
            p.vy += self.gravity
            p.t -= 1

        self.pps = [x for x in self.pps if x.t > 0]

    def draw(self, screen):
        rects = []
        for p in self.pps:
            self.PSIZE = 5 * p.t / 50
            (x1, y1) = self.world.world2screen(p.x, p.y)
            (x2, y2) = self.world.world2screen(p.ox, p.oy)
            r = pygame.draw.line(screen, p.c, (x1, y1), (x2, y2), int(self.PSIZE))
            r.inflate_ip(self.PSIZE * 2, self.PSIZE * 2)
            rects.append(r)

        return rects
