import random
from sys import maxsize

import pygame

from choon import datacache, cheese, mouse
from choon.constants import TILE_WIDTH, TILE_HEIGHT, CHEESE_CHANCE, DEPTH_COEF, MOUSE_CHANCE


class Tile(object):

    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        self.drop = None
        self.entities = []
        self.dirty = True
        self.temp = False
        return

    def get_rect(self):
        rect = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        rect.center = (self.x, self.y)
        return rect

    def draw(self):
        cheese = datacache.get_image(self.source_image)
        cheese_rect = cheese.get_rect()
        x = self.x % cheese_rect.width
        y = self.y % cheese_rect.height
        source_rect = (x, y, TILE_WIDTH, TILE_HEIGHT)
        anchor = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        anchor.center = self.world.world2screen(self.x, self.y)
        return [pygame.display.get_surface().blit(cheese, anchor, source_rect)]


class RockTile(Tile):

    def __init__(self, x, y, world):
        Tile.__init__(self, x, y, world)
        self.hardness = maxsize
        self.source_image = 'img/rockt.png'


class CheeseTile(Tile):

    def __init__(self, x, y, world):
        Tile.__init__(self, x, y, world)
        self.hardness = 40 + int(40 * y / 1000.0)
        self.source_image = 'img/cheese.png'
        i = random.random()
        if i < CHEESE_CHANCE:
            if y < DEPTH_COEF:
                a = 0.9
                b = 0.1
                c = 0.0
            elif y < 2 * DEPTH_COEF:
                a = 0.5
                b = 0.5
                c = 0.0
            elif y < 3 * DEPTH_COEF:
                a = 0.2
                b = 0.6
                c = 0.2
            elif y < 4 * DEPTH_COEF:
                a = 0.1
                b = 0.5
                c = 0.4
            elif y < 5 * DEPTH_COEF:
                a = 0.0
                b = 0.4
                c = 0.6
            else:
                a = 0.0
                b = 0.2
                c = 0.8
            j = random.random()
            if j < a:
                self.drop = cheese.BlueCheese
            elif j >= a and j < a + b:
                self.drop = cheese.GreenCheese
            elif j >= a + b and j < a + b + c:
                self.drop = cheese.RedCheese
        elif i >= CHEESE_CHANCE and i < CHEESE_CHANCE + MOUSE_CHANCE:
            if y < DEPTH_COEF:
                a = 0.8
                b = 0.2
                c = 0.0
                d = 0.0
            elif y < 2 * DEPTH_COEF:
                a = 0.5
                b = 0.4
                c = 0.1
                d = 0.0
            elif y < 3 * DEPTH_COEF:
                a = 0.3
                b = 0.5
                c = 0.2
                d = 0.0
            elif y < 4 * DEPTH_COEF:
                a = 0.1
                b = 0.3
                c = 0.5
                d = 0.1
            elif y < 5 * DEPTH_COEF:
                a = 0.0
                b = 0.2
                c = 0.3
                d = 0.5
            else:
                a = 0.0
                b = 0.0
                c = 0.2
                d = 0.8
            j = random.random()
            if j < a:
                self.drop = mouse.Mouse1
            elif j >= a and j < a + b:
                self.drop = mouse.Mouse2
            elif j >= a + b and j < a + b + c:
                self.drop = mouse.Mouse3
            elif j >= a + b + c and j < a + b + c + d:
                self.drop = mouse.Mouse4


class EmptyTile(Tile):

    def __init__(self, x, y, world):
        Tile.__init__(self, x, y, world)
        self.hardness = 0
        self.source_image = 'img/cheese-back.png'

    def draw(self):
        cheese = datacache.get_image(self.source_image)
        cheese_rect = cheese.get_rect()
        x = (self.x - self.world.x_offset / 2) % (cheese_rect.width - TILE_WIDTH)
        y = (self.y - self.world.y_offset / 2) % (cheese_rect.height - TILE_HEIGHT)
        source_rect = (x, y, TILE_WIDTH, TILE_HEIGHT)
        anchor = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        anchor.center = self.world.world2screen(self.x, self.y)
        return [pygame.display.get_surface().blit(cheese, anchor, source_rect)]


class SpaceTile(Tile):

    def __init__(self, x, y, world):
        Tile.__init__(self, x, y, world)
        self.source_image = 'img/space.png'
        self.hardness = 0

    def draw(self):
        cheese = datacache.get_image(self.source_image)
        cheese_rect = cheese.get_rect()
        x = (self.x - self.world.x_offset / 2) % (cheese_rect.width - TILE_WIDTH)
        y = (self.y - self.world.y_offset / 2) % (cheese_rect.height - TILE_HEIGHT)
        source_rect = (x, y, TILE_WIDTH, TILE_HEIGHT)
        anchor = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT)
        anchor.center = self.world.world2screen(self.x, self.y)
        return [pygame.display.get_surface().blit(cheese, anchor, source_rect)]


TILE_TYPES = [
 RockTile, CheeseTile, EmptyTile, SpaceTile]

def random_tile(x, y, world):
    return random.choice(TILE_TYPES)(x, y, world)
