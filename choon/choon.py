import sys

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_f, K_UP, K_DOWN, K_RETURN

from choon import datacache
from choon.main import Cheesemine


class MainMenu(object):

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 3072)
        pygame.init()
        self.w = 640
        self.h = 480
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.FULLSCREEN | pygame.SCALED)
        #self.screen = pygame.display.set_mode((self.w, self.h))
        self.screen.fill((255,255,255))
        pygame.mouse.set_visible(False)

        self.scr = datacache.get_image('img/menu.png')
        self.screen.blit(self.scr,(0,0))
        pygame.display.flip()

        self.playRect = pygame.Rect(300, 335, 100, 40)
        self.quitRect = pygame.Rect(300, 375, 100, 40)
        self.sel = self.playRect #selected

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(1)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(1)
                elif event.key == K_f:
                    pygame.display.toggle_fullscreen()
                elif event.key == K_UP:
                    if self.sel == self.playRect:
                        self.sel = self.quitRect
                    else:
                        self.sel = self.playRect

                elif event.key == K_DOWN:
                    if self.sel == self.playRect:
                        self.sel = self.quitRect
                    else:
                        self.sel = self.playRect
                elif event.key == K_RETURN:
                    if self.sel == self.quitRect:
                        sys.exit(1)
                    else:
                        #start the game
                        c = Cheesemine()
                        c.run()
                        self.screen.blit(self.scr,(0,0))
                        pygame.display.flip()

    def draw(self):
        scr = datacache.get_image('img/menu.png')
        self.screen.blit(scr,(0,0))

        pygame.draw.rect(self.screen, (255,255,255), self.sel, 1)

        rects = self.playRect.union(self.quitRect)
        pygame.display.update(rects)

    def run(self):
        while 1:
            pygame.time.wait(50)

            self.handle_input()
            self.draw()

if __name__ == '__main__':
    c = MainMenu()
    c.run()
