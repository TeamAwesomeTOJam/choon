from random import uniform
from math import sin

import pygame
from pygame.locals import K_a, K_d, K_w, K_SPACE

from choon import datacache
from choon.vec2d import vec2d
from choon.entity import Entity
from choon.cheese import Cheese
from choon.mouse import Mouse
from choon.tile import RockTile, CheeseTile, EmptyTile, SpaceTile
from choon.constants import TILE_WIDTH, TILE_HEIGHT, Y_SLIDE, X_SLIDE, MENU_HEIGHT, SURFACE

class Rover(Entity):
    """main rover, controlled by the player!
    """

    def __init__(self, world, particles):
        animations = {'default': (1, ['img/body.png']), 'hover': (
                   0.17, ["img/body_hover1.png", "img/body_hover2.png", "img/body_hover3.png", "img/body_hover4.png", "img/body_hover5.png"])}
        sounds = {'drive': 'sounds/drive.ogg', 'hover': 'sounds/thruster.ogg',
           'emergency': 'sounds/emergency.ogg'}
        Entity.__init__(self, 320, 240, 32, 24, animations, sounds, world, particles)
        self.current_sound = None
        self.laser_sound = datacache.get_sound('sounds/laser.ogg')
        self.laser_sound_on = False
        self.wheel_sprite = datacache.get_image('img/wheel.png')
        self.wheel_angle = 0
        self.gun_sprite = datacache.get_image('img/gun.png')
        self.total_cheese0 = 0
        self.total_cheese1 = 0
        self.total_cheese2 = 0
        self.money = 0
        self.laser_strength = 10
        self.thruster_strength = 1
        self.wheel_strength = 1
        self.cheese = []
        self.max_cheese = 10
        self.heat = 0
        self.max_heat = 100
        self.overheated = False
        self.hull = 100
        self.max_hull = 100
        self.score = 0
        self.c = 0
        self.isFiring = False
        self.firingAt = None
        self.firingAtPos = None
        self.dead = False
        self.death_frames = 0
        return

    def destroyed(self):
        if self.death_frames == 0:
            self.particles.addEffect(self.x, self.y, self.rc((200, 200, 200)), 1)
            self.laser_sound.stop()
            if self.current_sound:
                self.current_sound.stop()
            datacache.get_sound('sounds/death.ogg').play()
        if self.death_frames == 30:
            self.dead = True
        self.death_frames += 1

    def rc(self, c):
        return (
         c[0] + uniform(-30, 80), c[1] + uniform(-30, 80), c[2] + uniform(0, 50))

    def tick(self):
        if self.hull <= 0:
            self.destroyed()
            return
        if self.isFiring:
            if not self.laser_sound_on:
                self.laser_sound.play(-1)
                self.laser_sound_on = True
            me = vec2d(self.x, self.y - 9)
            p = vec2d(self.x, self.y - 9)
            m = vec2d(self.world.screen2world(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            dir = m - p
            dir.length = 2
            if dir.length == 0:
                dir = vec2d(0, 2)
            laserHits = 0
            t = None
            mouseHit = None
            while laserHits == 0:
                p += dir
                self.firingAtPos = p.inttup()
                t = self.world.tiles[(int((p.x + 16) // TILE_WIDTH), int((p.y + 16) // TILE_HEIGHT))]
                if (p - me).length > 480:
                    laserHits = 3
                if isinstance(t, CheeseTile):
                    laserHits = 1
                if isinstance(t, RockTile):
                    laserHits = 4
                miceHere = [x for x in t.entities if isinstance(x, Mouse)]
                for mouse in miceHere:
                    mousePos = vec2d(mouse.x, mouse.y)
                    if p.get_distance(mousePos) < 20:
                        laserHits = 2
                        mouseHit = mouse

            if laserHits == 1:
                self.firingAt = t
                self.firingAt.hardness -= self.laser_strength
                (x, y) = self.world.world2screen(self.firingAt.x, self.firingAt.y)
                if isinstance(t, CheeseTile):
                    self.particles.addEffect(self.firingAt.x, self.firingAt.y, self.rc((200,
                                                                                        80,
                                                                                        0)), 30)
                elif isinstance(t, RockTile):
                    self.particles.addEffect(self.firingAt.x, self.firingAt.y, self.rc((50,
                                                                                        50,
                                                                                        50)), 30)
                if self.firingAt.hardness < 0:
                    datacache.get_sound('sounds/explode.ogg').play()
                    self.firingAt.hardness = 0
                    self.particles.addEffect(self.firingAt.x, self.firingAt.y, self.rc((255,
                                                                                        255,
                                                                                        0)), 3)
                    self.world.tiles[(int(self.firingAt.x / TILE_WIDTH), int(self.firingAt.y / TILE_HEIGHT))] = EmptyTile(self.firingAt.x, self.firingAt.y, self.world)
                    if self.firingAt.drop:
                        cheese = self.firingAt.drop(self.firingAt.x, self.firingAt.y, self.world, self.particles)
            elif laserHits == 2:
                mouseHit.hardness -= self.laser_strength
                x, y = mouseHit.x, mouseHit.y
                self.particles.addEffect(x, y, (150, 150, 150), 8)
                if mouseHit.hardness < 0:
                    self.particles.addEffect(x, y, self.rc((255, 0, 0)), 2)
        elif self.laser_sound_on:
            self.laser_sound.stop()
            self.laser_sound_on = False
        pygame.event.pump()
        buttons = pygame.key.get_pressed()
        if buttons[K_a]:
            if self.on_ground:
                self.vx += -0.4 - 0.1 * self.wheel_strength
                self.play_animation('default')
                self.play_sound('drive')
            elif not self.overheated:
                self.heat += 0.4
                self.vx += -0.2 - 0.05 * self.thruster_strength
                self.play_sound('hover')
                if self.current_animation != self.animations['hover']:
                    self.play_animation('hover')
        if buttons[K_d]:
            if self.on_ground:
                self.vx += 0.4 + 0.1 * self.wheel_strength
                self.play_animation('default')
                self.play_sound('drive')
            elif not self.overheated:
                self.heat += 0.4
                self.vx += 0.2 + 0.05 * self.thruster_strength
                self.play_sound('hover')
                if self.current_animation != self.animations['hover']:
                    self.play_animation('hover')
        if self.on_ground:
            self.vx *= 0.95
            self.wheel_angle += self.vx * -10
        if buttons[K_w] and not self.overheated:
            self.heat += 0.8
            self.vy += -1 - 0.1 * self.thruster_strength
            self.play_sound('hover')
            if self.current_animation != self.animations['hover']:
                self.play_animation('hover')
        if self.overheated and self.heat <= 0:
            self.overheated = False
        elif not self.overheated and self.heat >= self.max_heat:
            self.overheated = True
        Entity.tick(self)
        if buttons[K_SPACE] and self.y > SURFACE - 200 and self.heat == 0:
            self.play_sound('emergency', 1)
            self.play_animation('hover')
            x, y = round(self.x / TILE_WIDTH) * TILE_WIDTH, (round(self.y / TILE_WIDTH) - 1) * TILE_HEIGHT
            t = self.world.tiles[(int(x / TILE_WIDTH), int(y / TILE_HEIGHT))]
            if not isinstance(t, EmptyTile):
                if not isinstance(t, SpaceTile):
                    self.world.tiles[(int(x / TILE_WIDTH), int(y / TILE_HEIGHT))] = EmptyTile(x, y, self.world)
                    self.particles.addEffect(x - 10, y - 45, (255, 255, 0), 4)
            self.ox = self.x
            self.oy = self.y
            self.x = x
            self.y = y
            self.vy = 0
        if not (buttons[K_a] or buttons[K_d] or buttons[K_w] or buttons[K_SPACE]) or self.overheated:
            self.heat = max(0, self.heat - 1)
            self.play_sound(None)
            if self.current_animation == self.animations['hover']:
                self.play_animation('default')
        (x, y) = self.world.world2screen(self.x, self.y)
        if x < X_SLIDE:
            self.world.shift_left(X_SLIDE - x)
        if x > 640 - X_SLIDE:
            self.world.shift_right(x - (640 - X_SLIDE))
        if y > 480 - Y_SLIDE:
            self.world.shift_down(y - (480 - Y_SLIDE))
        if y < Y_SLIDE + MENU_HEIGHT:
            self.world.shift_up(Y_SLIDE + MENU_HEIGHT - y)
        return

    def resolve_collisions(self, tile_collisions, entity_collisions):
        Entity.resolve_collisions(self, tile_collisions, entity_collisions)
        for entity in entity_collisions:
            if len(self.cheese) < self.max_cheese and isinstance(entity, Cheese):
                self.cheese.append(entity.type)
                datacache.get_sound('sounds/chime.ogg').play()
                entity.destroy()

    def draw(self):
        rects = []
        anchor = self.current_animation.frame.get_rect()
        anchor.center = self.world.world2screen(self.x, self.y)
        rotated_wheel_sprite = pygame.transform.rotate(self.wheel_sprite, self.wheel_angle)
        left_wheel_anchor = rotated_wheel_sprite.get_rect()
        left_wheel_anchor.center = anchor.move(-14, 6).center
        right_wheel_anchor = rotated_wheel_sprite.get_rect()
        right_wheel_anchor.center = anchor.move(14, 6).center
        screen = pygame.display.get_surface()
        gun_anchor = self.gun_sprite.get_rect()
        mouse_vec = vec2d(pygame.mouse.get_pos())
        gun_vec = vec2d(anchor.center) + vec2d(1, -8)
        dir_vec = mouse_vec - gun_vec
        gun_sprite = pygame.transform.rotate(self.gun_sprite, -1 * dir_vec.angle - 90)
        gun_anchor = gun_sprite.get_rect()
        a = vec2d(-1, -6)
        a.angle = dir_vec.angle
        gun_anchor.center = (a + vec2d(anchor.center) + vec2d(0, -9)).tup()
        if self.isFiring:
            self.c += 1
            m = 1 + 0.7 * sin(self.c / 4.0)
            a.length = 14
            (x1, y1) = (vec2d(self.world.world2screen(self.x, self.y)) + vec2d(0, -9) + a).tup()
            (x2, y2) = self.world.world2screen(self.firingAtPos[0], self.firingAtPos[1])
            for i in range(6, 0, -1):
                if i == 6:
                    r = pygame.draw.line(screen, (255, 255 - i * 40, 255 - i * 40), (x1, y1), (x2, y2), int(i * m))
                    r.inflate_ip(i * 2, i * 2)
                    rects.append(r)
                else:
                    pygame.draw.line(screen, (255, 255 - i * 40, 255 - i * 40), (x1, y1), (x2, y2), int(i * m))

            m = 1.5 + 0.5 * sin(self.c / 4.0 + 1.5)
            for i in range(4, 1, -1):
                pygame.draw.circle(screen, (255, 255 - i * 50, 255 - i * 50), (x1, y1), m * i)

            rects.append(pygame.Rect(x1, y1, 40, 40))
        rects.append(screen.blit(self.current_animation.frame, anchor))
        rects.append(screen.blit(gun_sprite, gun_anchor))
        rects.append(screen.blit(rotated_wheel_sprite, left_wheel_anchor))
        rects.append(screen.blit(rotated_wheel_sprite, right_wheel_anchor))
        (x, y) = self.world.world2screen(self.x, self.y)
        return rects
