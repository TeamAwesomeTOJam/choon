import pygame

from choon import datacache
from choon.constants import FONT_COLOUR, BKG_COLOUR, CHEESE_UNIT, CHEESE_COLOURS, CHEESE_BAR_COLOUR, FUEL_BAR_COLOUR, FUEL_BAR_FULL_COLOUR, HULL_BAR_COLOUR, HULL_BAR_FULL_COLOUR

class HUD(object):

    def __init__(self, rover, world):
        self.rover = rover
        self.world = world

    def draw(self, screen):
        font = datacache.get_font('VeraMoBd.ttf', 15)
        cargo_font = font.render('CARGO', 1, FONT_COLOUR)
        fuel_font = font.render('HEAT', 1, FONT_COLOUR)
        hull_font = font.render('HULL', 1, FONT_COLOUR)
        money_font = font.render('CASH', 1, FONT_COLOUR)
        money_amount_font = font.render('%s' % self.rover.money, 1, FONT_COLOUR)
        score_font = font.render('SCORE', 1, FONT_COLOUR)
        score_amount_font = font.render('%s' % self.rover.score, 1, FONT_COLOUR)
        laser_font = font.render('%s' % self.rover.laser_strength, 1, FONT_COLOUR)
        thruster_font = font.render('%s' % self.rover.thruster_strength, 1, FONT_COLOUR)
        wheel_font = font.render('%s' % self.rover.wheel_strength, 1, FONT_COLOUR)
        pos_font = font.render('X %i m' % (self.rover.x / 10), 1, FONT_COLOUR)
        depth_font = font.render('Y %i m' % (self.rover.y / 10), 1, FONT_COLOUR)
        speed = (self.rover.vx ** 2 + self.rover.vy ** 2) ** 0.5 / 10000 * 30 * 60 * 60
        speed_font = font.render('%i km/h' % speed, 1, FONT_COLOUR)
        laser_icon = datacache.get_image('img/icon/laserIcon.png')
        thruster_icon = datacache.get_image('img/icon/thrusterIcon.png')
        wheel_icon = datacache.get_image('img/icon/wheelIcon.png')
        radar = datacache.get_image('img/radar.png')
        rects = []
        rects.append(pygame.draw.rect(screen, BKG_COLOUR, (0, 0, 640, 64)))
        rects.append(screen.blit(radar, (5, 5)))
        p = self.world.entities[0]
        tilesd = self.world.get_tile_square(p.x, p.y, 400)
        for t in tilesd:
            if t.drop:
                dx = t.x - p.x
                dy = t.y - p.y
                dx = 27 * dx / 200.0
                dy = 27 * dy / 200.0
                if abs(dy) < 27 and abs(dx) < 27:
                    pygame.draw.circle(screen, (0, 255, 255), (dx + 32, dy + 32), 2)

        rects.append(screen.blit(money_font, (70, 5)))
        rects.append(screen.blit(money_amount_font, (70, 25)))
        rects.append(screen.blit(score_font, (120, 5)))
        rects.append(screen.blit(score_amount_font, (120, 25)))
        rects.append(screen.blit(laser_icon, (200, 5)))
        rects.append(screen.blit(thruster_icon, (200, 25)))
        rects.append(screen.blit(wheel_icon, (200, 45)))
        rects.append(screen.blit(laser_font, (220, 5)))
        rects.append(screen.blit(thruster_font, (220, 25)))
        rects.append(screen.blit(wheel_font, (220, 45)))
        rects.append(screen.blit(cargo_font, (250, 5)))
        rects.append(screen.blit(fuel_font, (250, 25)))
        rects.append(screen.blit(hull_font, (250, 45)))
        rects.append(pygame.draw.rect(screen, CHEESE_BAR_COLOUR, (300, 5, self.rover.max_cheese * CHEESE_UNIT, 16)))
        for i in range(len(self.rover.cheese)):
            pygame.draw.rect(screen, CHEESE_COLOURS[self.rover.cheese[i]], (300 + i * CHEESE_UNIT, 5, CHEESE_UNIT, 16))

        for i in range(self.rover.max_cheese):
            pygame.draw.rect(screen, (0, 0, 0), (300 + i * CHEESE_UNIT, 5, CHEESE_UNIT, 16), 1)

        rects.append(pygame.draw.rect(screen, FUEL_BAR_COLOUR, (300, 25, self.rover.max_heat, 16)))
        if self.rover.heat > 1:
            rects.append(pygame.draw.rect(screen, FUEL_BAR_FULL_COLOUR, (300, 25, self.rover.heat, 16)))
        rects.append(pygame.draw.rect(screen, HULL_BAR_COLOUR, (300, 45, self.rover.max_hull, 16)))
        if self.rover.hull > 1:
            rects.append(pygame.draw.rect(screen, HULL_BAR_FULL_COLOUR, (300, 45, self.rover.hull, 16)))
        for i in range(0, len(self.rover.cheese), CHEESE_UNIT):
            pygame.draw.line(screen, (0, 0, 0), (300 + i, 5), (300 + i * CHEESE_UNIT, 21), 1)

        pos_rect = pos_font.get_rect()
        pos_rect.topleft = (560, 5)
        rects.append(screen.blit(pos_font, pos_rect))
        depth_rect = depth_font.get_rect()
        depth_rect.topleft = (560, 25)
        rects.append(screen.blit(depth_font, depth_rect))
        speed_rect = depth_font.get_rect()
        speed_rect.topleft = (560, 45)
        rects.append(screen.blit(speed_font, speed_rect))
        return rects
