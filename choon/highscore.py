import os, sys

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN, K_BACKSPACE

from choon import datacache
from choon.constants import FONT_COLOUR

class HighScore(object):

    def __init__(self):
        self.name = ''

    def show(self, score):
        screen = pygame.display.get_surface()
        showing = True
        bkground = datacache.get_image('img/highscores.png')
        font = datacache.get_font('VeraMoBd.ttf', 15)
        (names, scores) = self.read_scores()
        name_fonts = [font.render(x, 1, FONT_COLOUR) for x in names]
        score_fonts = [font.render(str(x), 1, FONT_COLOUR) for x in scores]
        score_font = font.render('%s' % score, 1, FONT_COLOUR)
        while showing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(1)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit(1)
                    elif event.key == K_BACKSPACE:
                        if self.name:
                            self.name = self.name[:-1]
                    elif event.key == K_RETURN:
                        if self.name:
                            showing = False
                    else:
                        self.name += event.str

            screen.blit(bkground, (0, 0))
            for i in range(len(name_fonts)):
                screen.blit(name_fonts[i], (170, 120 + i * 20))
                rect = score_fonts[i].get_rect()
                rect.topright = (420, 120 + i * 20)
                screen.blit(score_fonts[i], rect)

            name_font = font.render(self.name, 1, FONT_COLOUR)
            rect = score_font.get_rect()
            rect.topright = (420, 400)
            screen.blit(score_font, rect)
            screen.blit(name_font, (170, 400))
            pygame.display.flip()

        self.save_scores(names, scores, self.name, score)

    def read_scores(self):
        ifile = open(os.path.join(os.path.dirname(__file__), 'data', 'scores.txt'), 'r')
        line = ifile.readline()[:-1]
        names, scores = [], []
        while line:
            (name, score) = line.split('|')
            names.append(name)
            scores.append(score)
            line = ifile.readline()[:-1]

        ifile.close()
        return (names, scores)

    def save_scores(self, names, scores, name, score):
        for i in range(len(scores)):
            if score > int(scores[i]):
                scores[i:i] = [
                 score]
                names[i:i] = [name]
                scores = scores[:-1]
                names = names[:-1]
                break

        ofile = open(os.path.join(os.path.dirname(__file__), 'data', 'scores.txt'), 'w')
        for i in range(len(scores)):
            ofile.write(names[i] + '|' + '%s' % scores[i] + '\n')

        ofile.close()
