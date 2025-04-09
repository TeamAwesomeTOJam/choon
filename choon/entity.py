import pygame

from choon import animation, datacache
from choon.constants import TILE_WIDTH, TILE_HEIGHT


class Entity(object):
    """The main entity class. Something on a map
    """

    def __init__(self, x, y, width, height, animations, sounds, world, particles):
        """Input: Real x,y position, sprite pointer
        """
        self.x = x
        self.y = y
        self.ox = x
        self.oy = y
        self.width = width
        self.height = height
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.world = world
        self.world.add_entity(self)
        self.particles = particles
        self.animations = {}
        for (name, data) in animations.items():
            self.animations[name] = animation.Animation(*data)

        self.play_animation('default')
        self.sounds = {}
        for (name, path) in sounds.items():
            self.sounds[name] = datacache.get_sound(path)

        self.current_sound = None

    def destroy(self):
        if self in self.world.entities:
            self.world.entities.remove(self)
        for t in list(self.world.tiles.values()):
            while self in t.entities:
                t.entities.remove(self)

        for tile in self.world.get_tiles(self.ox, self.oy, self.width, self.height):
            if self in tile.entities:
                tile.entities.remove(self)

        for tile in self.world.get_tiles(self.x, self.y, self.width, self.height):
            if self in tile.entities:
                tile.entities.remove(self)

    def get_rect(self):
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = (self.x, self.y)
        return rect

    def detect_collisions(self):
        """Input: All entities
        Returns: List of entities this entity collides with
        """
        tile_collisions = []
        entity_collisions = []
        tiles = self.world.get_tiles(self.x, self.y, self.width, self.height)
        for tile in tiles:
            if tile.hardness > 0 and self.get_rect().colliderect(tile.get_rect()):
                tile_collisions.append(tile)
            for entity in tile.entities:
                if entity != self and entity not in entity_collisions and self.get_rect().colliderect(entity.get_rect()):
                    entity_collisions.append(entity)

        return (
         tile_collisions, entity_collisions)

    def resolve_collisions(self, tile_collisions, entity_collisions):
        """Input: List of entities this one collides with
        """
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
                self.vx = 0

        self.on_ground = on_ground

    def tick(self):
        """Updates this entity
        """
        self.current_animation.update(0.03333333333333333)
        self.vy += 0.5
        self.oy = self.y
        self.y += self.vy
        self.y = max(self.y, -500)
        if self.y == -500:
            self.vy = 0
        self.ox = self.x
        self.x += self.vx
        (tiles, entities) = self.detect_collisions()
        self.resolve_collisions(tiles, entities)
        self.set_tiles()

    def set_tiles(self):
        for tile in self.world.get_tiles(self.ox, self.oy, self.width, self.height):
            if self in tile.entities:
                tile.entities.remove(self)

        for tile in self.world.get_tiles(self.x, self.y, self.width, self.height):
            tile.entities.append(self)

    def draw(self):
        anchor = self.current_animation.frame.get_rect()
        anchor.center = self.world.world2screen(self.x, self.y)
        return [pygame.display.get_surface().blit(self.current_animation.frame, anchor)]

    def play_animation(self, name, loops=-1, callback=None):
        self.current_animation = self.animations[name]
        self.current_animation.play(loops, callback)

    def play_sound(self, name, loops=-1):
        if name and self.current_sound == self.sounds[name]:
            return
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None
        if name:
            self.current_sound = self.sounds[name]
            self.current_sound.play(loops)
        return
