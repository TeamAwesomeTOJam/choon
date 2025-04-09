from choon.entity import Entity


class Cheese(Entity):

    def __init__(self, type, x, y, animations, world, particle):
        Entity.__init__(self, x, y, 28, 20, animations, {}, world, particle)
        self.type = type

    def tick(self):
        Entity.tick(self)
        self.vy += 0.5
        self.ox = self.x
        self.oy = self.y
        self.x += self.vx
        self.y += self.vy
        (tiles, entities) = self.detect_collisions()
        self.resolve_collisions(tiles, entities)

    def resolve_collisions(self, tile_collisions, entity_collisions):
        Entity.resolve_collisions(self, tile_collisions, entity_collisions)
        for entity in entity_collisions:
            if isinstance(entity, Cheese):
                self.y = self.oy
                self.vy = 0
                self.x = self.ox
                self.vx = 0


class BlueCheese(Cheese):

    def __init__(self, x, y, world, particle):
        animations = {'default': (1, ['img/cheeseBlue.png'])}
        Cheese.__init__(self, 0, x, y, animations, world, particle)


class GreenCheese(Cheese):

    def __init__(self, x, y, world, particle):
        animations = {'default': (1, ['img/cheeseGreen.png'])}
        Cheese.__init__(self, 1, x, y, animations, world, particle)


class RedCheese(Cheese):

    def __init__(self, x, y, world, particle):
        animations = {'default': (1, ['img/cheeseRed.png'])}
        Cheese.__init__(self, 2, x, y, animations, world, particle)
