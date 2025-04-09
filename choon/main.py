import os, sys
from random import uniform, choice


import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN, KEYUP, K_UP, K_DOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, K_f

from choon import highscore, datacache, world
from choon.hud import HUD
from choon.crosshair import Cross
from choon.particles import Particles
from choon.rover import Rover
from choon.menu import Menu
from choon.mouse import Mouse1, Mouse2, Mouse3, Mouse4
from choon.constants import MOUSE_P, SURFACE

if hasattr(sys, 'frozen'):
    datacache.data_directory = os.path.join(os.path.dirname(sys.executable), 'data')
else:
    datacache.data_directory = os.path.join(os.path.dirname(__file__), 'data')


class Cheesemine(object):

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 3072)
        pygame.init()
        datacache.get_sound('sounds/bgm.ogg').play(-1)
        self.w = 640
        self.h = 480
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.FULLSCREEN | pygame.SCALED)
        self.screen.fill((255, 255, 255))
        self.world = world.World()
        self.crosshair = Cross()
        self.old_rects = []
        self.particles = Particles(self.world)
        self.playing = True
        self.rover = Rover(self.world, self.particles)
        self.hud = HUD(self.rover, self.world)
        self.menu = Menu(self.rover)
        self.clock = pygame.time.Clock()
        pygame.display.flip()
        pygame.mouse.set_visible(False)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(1)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    scr = datacache.get_image('img/ESC.png')
                    self.screen.blit(scr, (200, 150))
                    pygame.display.flip()
                    paused = True
                    while paused:
                        pygame.time.wait(30)
                        for e in pygame.event.get():
                            if e.type == KEYDOWN:
                                if e.key == K_RETURN:
                                    paused = False
                                    self.world.dirty_screen()
                                elif e.key == K_ESCAPE:
                                    self.playing = False
                                    paused = False

            elif event.type == KEYUP:
                if event.key == K_f:
                    pygame.display.toggle_fullscreen()
                elif event.key == K_UP:
                    self.menu.current = (self.menu.current - 1) % len(self.menu.options_text)
                elif event.key == K_DOWN:
                    self.menu.current = (self.menu.current + 1) % len(self.menu.options_text)
                elif event.key == K_RETURN:
                    self.menu.buy()
            elif event.type == MOUSEBUTTONDOWN:
                self.rover.isFiring = True
            elif event.type == MOUSEBUTTONUP:
                self.rover.isFiring = False
            elif event.type == MOUSEMOTION:
                self.crosshair.update(event.pos)

    def draw(self):
        rects = self.world.draw(self.screen)
        rects += self.particles.draw(self.screen)
        rects += self.hud.draw(self.screen)
        if self.menu.active:
            rects += self.menu.draw(self.screen)
        rects += self.crosshair.draw(self.screen)
        pygame.display.update(rects + self.old_rects)
        self.old_rects = rects

    def make_mouse(self):
        l = self.world.get_border_tiles(7) + self.world.get_border_tiles(8)
        l = [i for i in l if i.hardness == 0]
        if l and uniform(0, 1) < MOUSE_P:
            mouset = choice(l)
            choice([Mouse1, Mouse2, Mouse3, Mouse4])(mouset.x, mouset.y, self.world, self.particles)

    def run(self):
        while self.playing:
            self.clock.tick(30)
            self.handle_input()
            self.particles.tick()
            self.world.tick()
            if self.rover.oy > SURFACE and self.rover.y <= SURFACE:
                self.menu.enter_menu()
            if self.rover.oy <= SURFACE and self.rover.y > SURFACE:
                self.menu.leave_menu()
            if self.rover.dead:
                hs = highscore.HighScore()
                hs.show(self.rover.score)
                self.playing = False
            self.draw()


if __name__ == '__main__':
    c = Cheesemine()
    c.run()
