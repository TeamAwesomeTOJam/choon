import pygame

from choon import datacache
from choon.constants import FONT_COLOUR, VALUES

class Menu(object):

    def __init__(self, rover):
        self.rover = rover
        self.options_text = ['Laser', 'Thruster', 'Engine', 'Capacity', 'Heat', 'Hull']
        self.icons = ['img/icon/laserIcon.png','img/icon/thrusterIcon.png','img/icon/wheelIcon.png','img/icon/backpackIcon.png','img/icon/batteryIcon.png','img/icon/hullIcon.png']
        self.costs = [13, 13, 13, 13, 13, 13]
        self.current = 0
        self.active = False

    def enter_menu(self):
        cheese = [
         0, 0, 0]
        for i in self.rover.cheese:
            self.rover.money += VALUES[i]
            self.rover.score += VALUES[i]
            cheese[i] += 1

        self.rover.cheese = []
        self.rover.heat = 0
        self.rover.hull = self.rover.max_hull
        self.active = True

    def leave_menu(self):
        self.active = False

    def draw(self, screen):
        font = datacache.get_font('VeraMoBd.ttf', 15)
        options = [font.render(x, 1, FONT_COLOUR) for x in self.options_text]
        surface = pygame.Surface((200, 200))
        heading = font.render('UPGRADE    PRICE', 1, (255, 0, 0))
        surface.blit(heading, (40, 5))
        for i in range(len(options)):
            option = options[i]
            icon = datacache.get_image(self.icons[i])
            cost = font.render(repr((self.costs[i])), 1, FONT_COLOUR)
            if i == self.current:
                pygame.draw.rect(surface, (255, 0, 0), (10, 40 + 20 * i, 190, 15))
            surface.blit(icon, (20, 40 + 20 * i))
            surface.blit(option, (40, 40 + 20 * i))
            surface.blit(cost, (150, 40 + 20 * i))

        surface.set_alpha(200)
        rect = surface.get_rect()
        rect.center = (320, 240)
        screen.blit(surface, rect)
        return [rect]

    def buy(self):
        if self.rover.money >= self.costs[self.current]:
            self.rover.money -= self.costs[self.current]
            self.costs[self.current] += 5
            if self.options_text[self.current] == 'Laser':
                self.rover.laser_strength += 1
            if self.options_text[self.current] == 'Thruster':
                self.rover.thruster_strength += 1
            if self.options_text[self.current] == 'Engine':
                self.rover.wheel_strength += 1
            if self.options_text[self.current] == 'Capacity':
                self.rover.max_cheese += 1
            if self.options_text[self.current] == 'Heat':
                self.rover.max_heat += 10
                self.rover.fuel = self.rover.max_heat
            if self.options_text[self.current] == 'Hull':
                self.rover.max_hull += 10
                self.rover.hull = self.rover.max_hull
