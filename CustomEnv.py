import sys

import numpy as np
import pygame
from gym import Env
from gym.spaces import Box, Discrete
import random

from Action import Action
from shower import Shower



class CustomEnv(Env):
    def __init__(self):
        self.action_space = Discrete(3)
        self.observation_space = Box(low=np.array([0]),high=np.array([100]))

        self.running = True
        self.screen = None
        self.game_surface = pygame.Surface((800, 600))
        self.shower = Shower(self.game_surface)

        self.state = self.shower.get_temp()
        self.remain_steps = 100

    def create_screen(self):
        self.screen = pygame.display.set_mode((800, 600))

    def step(self, action):
        if action == 0:
            self.shower.decrease_temp()
        elif action == 2:
            self.shower.increase_temp()
        self.shower.update()
        self.state = self.shower.get_temp()
        self.remain_steps -= 1

        if self.state >= 37 and self.state <= 39:
            reward = 1
        else:
            reward = -1

        done = (self.remain_steps <= 0)
        info = {}

        return self.state, reward, done, info

    def render(self, mode):
        # print(f"RENDERING : state : {self.state}")
        self.show()
        pygame.display.update()

    def reset(self):
        self.shower = Shower(self.game_surface)
        self.state = self.shower.get_temp()
        self.remain_steps = 100
        return self.state

    def action(self, action:Action):
        if action == Action.INCREASE:
            self.shower.increase_temp()
        elif action == Action.DECREASE:
            self.shower.decrease_temp()

    def update(self):
        self.shower.update()

    def show(self):
        self.screen.fill(pygame.Color("BLACK"))
        self.game_surface.fill((200, 200, 200))
        self.shower.show()
        self.screen.blit(self.game_surface, (0, 0))

    def get_observations(self):
        return np.array([self.shower.get_temp()])