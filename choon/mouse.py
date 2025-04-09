import random
from math import sqrt

import pygame

from choon import cheese, datacache
from choon.entity import Entity
from choon.constants import TILE_WIDTH, TILE_HEIGHT


class Mouse(Entity):
    """mouse, lol"""

    def __init__(self, x, y, animations, world, particles):
        Entity.__init__(self, x, y, 24, 24, animations, {}, world, particles)
        datacache.get_sound('sounds/mouse_01.ogg').play()
        self.play_animation('walk')

    def tick(self):
        (x, y) = self.world.world2screen(self.x, self.y)
        if x < 800 and x > -160 and y < 640 and y > -160:
            Entity.tick(self)
            i = random.random()
            if i < 0.002:
                datacache.get_sound('sounds/mouse_01.ogg').play()
            elif i < 0.004:
                datacache.get_sound('sounds/mouse_01.ogg').play()
            if self.hardness < 0:
                datacache.get_sound('sounds/squish.ogg').play()
                self.destroy()
            if self.on_ground:
                px, py = self.world.entities[0].x, self.world.entities[0].y
                x, y = self.x, self.y
                dy = y - py
                if dy > 0 and dy < 30 * self.vx and abs(x - px) < 30 * self.vx:
                    v1y = sqrt(dy)
                    dt = dy / (0.5 * v1y)
                    self.vy = -v1y
                    self.on_ground = False
                else:
                    dx = x - px
                    if abs(dy) < 10 and abs(dx) > abs(self.vx):
                        if px < x and self.vx > 0:
                            self.vx = -self.vx
                        if px > x and self.vx < 0:
                            self.vx = -self.vx
            else:
                px, py = self.world.entities[0].x, self.world.entities[0].y
                x, y = self.x, self.y
                if px < x and abs(x - px) > self.vx:
                    x -= self.vx
                if px > x and abs(x - px) > self.vx:
                    x += self.vx

    def resolve_collisions(self, tile_collisions, entity_collisions):
        on_ground = False
        for tile in tile_collisions:
            if tile.y - self.y > 0:
                on_ground = True
            x_penetration = abs(abs(self.x - tile.x) - abs(self.width / 2 + TILE_WIDTH / 2))
            y_penetration = abs(abs(self.y - tile.y) - abs(self.height / 2 + TILE_HEIGHT / 2))
            if y_penetration < 4 or y_penetration < x_penetration:
                self.y = self.oy
                self.vy = 0
            else:
                self.x = self.ox
                self.vx = -self.vx

        for entity in entity_collisions:
            if isinstance(entity, cheese.Cheese):
                entity.destroy()
            if hasattr(entity, 'hull'):
                entity.hull -= self.damage
                datacache.get_sound('sounds/mouse_attack.ogg').play()
                x, y = entity.x, entity.y
                self.particles.addEffect(x, y, (250, 250, 250), 30)

        self.on_ground = on_ground

    def draw(self):
        anchor = self.current_animation.frame.get_rect()
        anchor.center = self.world.world2screen(self.x, self.y)
        surf = self.current_animation.frame
        if self.vx > 0:
            surf = pygame.transform.flip(surf, True, False)
        return [
         pygame.display.get_surface().blit(surf, anchor)]


class Mouse1(Mouse):

    def __init__(self, x, y, world, particles):
        animations = {'default': (1, ['img/mouseWalk1.png']), 'walk': (
                  1, ["img/mouseWalk1.png", "img/mouseWalk1.png", "img/mouseWalk2.png", "img/mouseWalk3.png", "img/mouseWalk4.png", "img/mouseWalk5.png", "img/mouseWalk6.png", "img/mouseWalk7.png", "img/mouseWalk8.png", "img/mouseWalk9.png", "img/mouseWalk10.png", "img/mouseWalk11.png", "img/mouseWalk12.png"])}
        Mouse.__init__(self, x, y, animations, world, particles)
        self.vx = 4
        self.hardness = 200
        self.damage = 1


class Mouse2(Mouse):

    def __init__(self, x, y, world, particles):
        animations = {'default': (1, ['img/mouse2Walk1.png']), 'walk': (
                  0.8, ["img/mouse2Walk1.png", "img/mouse2Walk1.png", "img/mouse2Walk2.png", "img/mouse2Walk3.png", "img/mouse2Walk4.png", "img/mouse2Walk5.png", "img/mouse2Walk6.png", "img/mouse2Walk7.png", "img/mouse2Walk8.png", "img/mouse2Walk9.png", "img/mouse2Walk10.png", "img/mouse2Walk11.png", "img/mouse2Walk12.png"])}
        Mouse.__init__(self, x, y, animations, world, particles)
        self.vx = 6
        self.hardness = 400
        self.damage = 2


class Mouse3(Mouse):

    def __init__(self, x, y, world, particles):
        animations = {'default': (1, ['img/mouse3Walk1.png']), 'walk': (
                  0.7, ["img/mouse3Walk1.png", "img/mouse3Walk1.png", "img/mouse3Walk2.png", "img/mouse3Walk3.png", "img/mouse3Walk4.png", "img/mouse3Walk5.png", "img/mouse3Walk6.png", "img/mouse3Walk7.png", "img/mouse3Walk8.png", "img/mouse3Walk9.png", "img/mouse3Walk10.png", "img/mouse3Walk11.png", "img/mouse3Walk12.png"])}
        Mouse.__init__(self, x, y, animations, world, particles)
        self.vx = 8
        self.hardness = 800
        self.damage = 4


class Mouse4(Mouse):

    def __init__(self, x, y, world, particles):
        animations = {'default': (1, ['img/mouse4Walk1.png']), 'walk': (
                  0.6, ["img/mouse4Walk1.png", "img/mouse4Walk1.png", "img/mouse4Walk2.png", "img/mouse4Walk3.png", "img/mouse4Walk4.png", "img/mouse4Walk5.png", "img/mouse4Walk6.png", "img/mouse4Walk7.png", "img/mouse4Walk8.png", "img/mouse4Walk9.png", "img/mouse4Walk10.png", "img/mouse4Walk11.png", "img/mouse4Walk12.png"])}
        Mouse.__init__(self, x, y, animations, world, particles)
        self.vx = 10
        self.hardness = 1600
        self.damage = 8
