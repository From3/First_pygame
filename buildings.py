import pygame
import map_objects as mo

greenfood = mo.GreenFood()
g_food = greenfood.name


class Base:
    def __init__(self, faction):
        self.team_base = faction
        self.x = faction[0][0]
        self.y = faction[0][1]

    def draw(self, window, colour):
        pygame.draw.circle(window, colour, (self.x, self.y), 12)
