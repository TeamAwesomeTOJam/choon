import pygame

from choon.vec2d import vec2d

class Cross:

    def __init__(self):
        self.cangle = 0
        self.mouse_pos = (0, 0)
        self.old_mouse_pos = (0, 0)

    def update(self, mp):
        self.old_mouse_pos = self.mouse_pos
        self.mouse_pos = mp

    def draw(self, screen):
        m = vec2d(self.mouse_pos)
        rects = pygame.draw.circle(screen, (255, 255, 255), self.mouse_pos, 15, 1)
        v1 = vec2d(0, 15)
        v1.rotate(self.cangle)
        pygame.draw.line(screen, (255, 255, 255), (m + v1).inttup(), (m - v1).inttup(), 1)
        v1.rotate(90)
        pygame.draw.line(screen, (255, 255, 255), (m + v1).inttup(), (m - v1).inttup(), 1)
        self.cangle += 10
        return [
         rects.inflate(2, 2)]
