from random import uniform, randint, choice

from choon.tile import CheeseTile, EmptyTile, SpaceTile, TILE_TYPES
from choon.constants import NUM_TILE_Y, NUM_TILE_X, TILE_WIDTH, TILE_HEIGHT, SURFACE, CAVITY_P, MENU_HEIGHT


class World(object):

    def __init__(self):
        self.entities = []
        self.tiles = {}
        self.x_offset = 0
        self.y_offset = 0
        self.total_y = 0
        self.total_x = 0
        for x in range(-15, NUM_TILE_X + 16):
            for y in range(-15, NUM_TILE_Y + 16):
                self.add_tile((x, y), CheeseTile(x * TILE_WIDTH, y * TILE_HEIGHT, self))

    def add_entity(self, entity):
        self.entities.append(entity)

    def tick(self):
        for entity in self.entities:
            entity.tick()

    def get_tiles(self, x, y, width, height):
        max_x = int((x + width + 1) / TILE_WIDTH)
        min_x = int((x - 1) / TILE_WIDTH)
        max_y = int((y + height + 1) / TILE_HEIGHT)
        min_y = int((y - 1) / TILE_HEIGHT)
        tiles = []
        for y_i in range(min_y, max_y + 2):
            for x_i in range(min_x, max_x + 2):
                tiles.append(self.tiles[(x_i, y_i)])

        return tiles

    def draw(self, screen):
        screen.fill((0, 0, 0))
        update_rects = []
        for x in range(int(self.x_offset // TILE_WIDTH), int(self.x_offset // TILE_WIDTH + NUM_TILE_X + 2)):
            for y in range(int(self.y_offset // TILE_HEIGHT), int(self.y_offset // TILE_HEIGHT + NUM_TILE_Y + 2)):
                rect = self.tiles[(x, y)].draw()
                if self.tiles[(x, y)].dirty:
                    update_rects += rect
                    self.tiles[(x, y)].dirty = False

        for entity in self.entities:
            update_rects += entity.draw()

        return update_rects

    def add_row(self, x, y):
        for diff in range(-15, NUM_TILE_X + 15):
            self.add_tile((x + diff, y), CheeseTile((x + diff) * TILE_WIDTH, y * TILE_HEIGHT, self))

    def add_col(self, x, y):
        for diff in range(-15, NUM_TILE_Y + 15):
            self.add_tile((x, y + diff), CheeseTile(x * TILE_WIDTH, (y + diff) * TILE_HEIGHT, self))

    def flood(self, x, y, type, depth=7, minx=3, miny=3, came_from=0):
        """ flood tile of type type around x,y """
        if depth == 0:
            newt = TILE_TYPES[1](x * TILE_WIDTH, y * TILE_HEIGHT, self)
            newt.temp = True
            self.add_tile((x, y), newt)
            newt = TILE_TYPES[1]((x + 1) * TILE_WIDTH, y * TILE_HEIGHT, self)
            newt.temp = True
            self.add_tile((x + 1, y), newt)
            newt = TILE_TYPES[1]((x + 1) * TILE_WIDTH, (y + 1) * TILE_HEIGHT, self)
            newt.temp = True
            self.add_tile((x + 1, y + 1), newt)
            newt = TILE_TYPES[1](x * TILE_WIDTH, (y + 1) * TILE_HEIGHT, self)
            newt.temp = True
            self.add_tile((x, y + 1), newt)
            newt = TILE_TYPES[1]((x - 1) * TILE_WIDTH, (y + 1) * TILE_HEIGHT, self)
            newt.temp = True
            self.add_tile((x - 1, y + 1), newt)
            newt = TILE_TYPES[1]((x - 1) * TILE_WIDTH, y * TILE_HEIGHT, self)
            newt.temp = True
            self.add_tile((x - 1, y), newt)
            newt = TILE_TYPES[1]((x - 1) * TILE_WIDTH, (y - 1) * TILE_HEIGHT, self)
            newt.temp = True
            self.add_tile((x - 1, y - 1), newt)
            newt = TILE_TYPES[1](x * TILE_WIDTH, (y - 1) * TILE_HEIGHT, self)
            newt.temp = True
            self.add_tile((x, y - 1), newt)
            newt = TILE_TYPES[1]((x + 1) * TILE_WIDTH, (y - 1) * TILE_HEIGHT, self)
            newt.temp = True
            self.add_tile((x + 1, y - 1), newt)
        if depth > 1:
            self.add_tile((x, y), TILE_TYPES[type](x * TILE_WIDTH, y * TILE_HEIGHT, self))
            p = 0.4
            if not came_from == 2:
                if uniform(0, 1) < p or depth > minx:
                    self.flood(x - 1, y, type, depth - 1, minx, miny, 1)
                else:
                    self.flood(x - 1, y, type, 0, minx, miny, 1)
            if not came_from == 1:
                if uniform(0, 1) < p or depth > minx:
                    self.flood(x + 1, y, type, depth - 1, minx, miny, 2)
                else:
                    self.flood(x + 1, y, type, 0, minx, miny, 2)
            if not came_from == 4:
                if uniform(0, 1) < p or depth > miny:
                    self.flood(x, y - 1, type, depth - 1, minx, miny, 3)
                else:
                    self.flood(x, y - 1, type, 0, minx, miny, 3)
            if not came_from == 3:
                if uniform(0, 1) < p or depth > miny:
                    self.flood(x, y + 1, type, depth - 1, minx, miny, 4)
                else:
                    self.flood(x, y + 1, type, 0, minx, miny, 4)

    def add_tile(self, p, tile):
        (x, y) = p
        if p not in self.tiles or self.tiles[p].temp:
            if y < SURFACE // TILE_HEIGHT:
                self.tiles[p] = SpaceTile(x * TILE_WIDTH, y * TILE_HEIGHT, self)
            else:
                self.tiles[p] = tile

    def dirty_screen(self):
        for x in range(int(self.x_offset // TILE_WIDTH), int(self.x_offset // TILE_WIDTH + NUM_TILE_X + 2)):
            for y in range(int(self.y_offset // TILE_HEIGHT), int(self.y_offset // TILE_HEIGHT + NUM_TILE_Y + 2)):
                try:
                    self.tiles[(x, y)].dirty = True
                except KeyError:
                    self.add_tile((x, y), EmptyTile(x * TILE_WIDTH, y * TILE_HEIGHT, self))

    def shift_up(self, amount):
        self.total_y -= amount
        i = 15
        while self.total_y <= -1 * TILE_HEIGHT:
            self.total_y += TILE_HEIGHT
            self.add_row(self.x_offset // TILE_WIDTH, self.y_offset // TILE_HEIGHT - i)
            i += 1

        if uniform(0, 1) < CAVITY_P:
            x = randint(int(self.x_offset // TILE_WIDTH - 15), int(self.x_offset // TILE_WIDTH + NUM_TILE_X + 15))
            y = self.y_offset // TILE_HEIGHT - 20
            type = choice([0, 2])
            self.flood(x, y, type)
        self.y_offset -= amount
        self.dirty_screen()

    def shift_down(self, amount):
        self.total_y += amount
        i = 15
        while self.total_y >= TILE_HEIGHT:
            self.total_y -= TILE_HEIGHT
            self.add_row(self.x_offset // TILE_WIDTH, self.y_offset // TILE_HEIGHT + i + NUM_TILE_Y)
            i += 1

        if uniform(0, 1) < CAVITY_P:
            x = randint(int(self.x_offset // TILE_WIDTH - 15), int(self.x_offset // TILE_WIDTH + NUM_TILE_X + 15))
            y = self.y_offset // TILE_HEIGHT + NUM_TILE_Y + 20
            type = choice([0, 2])
            self.flood(x, y, type)
        self.y_offset += amount
        self.dirty_screen()

    def shift_left(self, amount):
        self.total_x -= amount
        i = 15
        while self.total_x <= -1 * TILE_WIDTH:
            self.total_x += TILE_WIDTH
            self.add_col(self.x_offset // TILE_WIDTH - i, self.y_offset // TILE_WIDTH)
            i += 1

        if uniform(0, 1) < CAVITY_P:
            y = randint(int(self.y_offset // TILE_HEIGHT - 15), int(self.y_offset // TILE_HEIGHT + NUM_TILE_Y + 15))
            x = self.x_offset // TILE_HEIGHT - 20
            type = choice([0, 2])
            self.flood(x, y, type)
        self.x_offset -= amount
        self.dirty_screen()

    def shift_right(self, amount):
        self.total_x += amount
        i = 15
        while self.total_x >= TILE_WIDTH:
            self.total_x -= TILE_WIDTH
            self.add_col(self.x_offset // TILE_WIDTH + i + NUM_TILE_X, self.y_offset // TILE_WIDTH)
            i += 1

        if uniform(0, 1) < CAVITY_P:
            y = randint(int(self.y_offset // TILE_HEIGHT - 15), int(self.y_offset // TILE_HEIGHT + NUM_TILE_Y + 15))
            x = self.x_offset // TILE_HEIGHT + NUM_TILE_X + 20
            type = choice([0, 2])
            self.flood(x, y, type)
        self.x_offset += amount
        self.dirty_screen()

    def world2screen(self, x, y):
        new_x = x - self.x_offset
        new_y = y - self.y_offset + MENU_HEIGHT
        return (new_x, new_y)

    def screen2world(self, x, y):
        new_x = self.x_offset + x
        new_y = y + self.y_offset - MENU_HEIGHT
        return (new_x, new_y)

    def get_border_tiles(self, n):
        t = []
        for x in range(self.x_offset // TILE_WIDTH - n, self.x_offset // TILE_WIDTH + NUM_TILE_X + n):
            t.append(self.tiles[(x, self.y_offset // TILE_HEIGHT - n)])
            t.append(self.tiles[(x, self.y_offset // TILE_HEIGHT + NUM_TILE_Y + n)])

        for y in range(self.y_offset // TILE_HEIGHT - n, self.y_offset // TILE_WIDTH + NUM_TILE_Y + n):
            t.append(self.tiles[(self.x_offset // TILE_WIDTH - n, y)])
            t.append(self.tiles[(self.x_offset // TILE_WIDTH + NUM_TILE_X + n, y)])

        return t

    def get_tile_square(self, x, y, len):
        x = x - len // 2
        y = y - len // 2
        l = []
        for i in range(int(x // TILE_WIDTH), int(x // TILE_WIDTH + len // TILE_WIDTH)):
            for j in range(int(y // TILE_HEIGHT), int(y // TILE_HEIGHT + len // TILE_HEIGHT)):
                l.append(self.tiles[(i, j)])

        return l
