from random import randint

import pygame
from pygame.math import Vector2

import utils


class Shower:
    def __init__(self, surface) -> None:
        self.temp = randint(-40, 120)
        self.surface = surface
        self.temp_change = 0

        self.MIN_TEMP = 0
        self.MAX_TEMP = 100

    def show(self):
        # temp, from -40 to 120 (160, and 800/160 == 5
        showed_value = utils.map(self.temp, -40, 120, 0, 800)
        rect_cold = pygame.Rect(0,0, showed_value, 100)
        rect_hot = pygame.Rect(showed_value, 0, 800 - showed_value, 100)
        pygame.draw.rect(self.surface, (30,30,120), rect_cold)
        pygame.draw.rect(self.surface, (120,30,30), rect_hot)

        good_min = utils.map(37, -40, 120, 0, 800)
        good_max = utils.map(39, -40, 120, 0, 800)
        rect_good = pygame.Rect(good_min, 100, good_max-good_min, 20)
        pygame.draw.rect(self.surface, (30, 120, 30), rect_good)


    def update(self):
        self.temp += self.temp_change
        self.temp_change = 0

    def get_temp(self):
        return self.temp

    def increase_temp(self):
        self.temp_change = 1

    def decrease_temp(self):
        self.temp_change = -1