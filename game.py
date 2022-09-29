import sys

import numpy as np
import pygame
from keras import Sequential
from keras.optimizers import Adam
from tensorflow import keras

from Action import Action
from Agent import Agent
from CustomEnv import CustomEnv
from shower import Shower
from utils import TRAINED_DIR_NAME

SCREEN_UPDATE = pygame.USEREVENT

class Game:
    def __init__(self):
        self.running = True
        self.env = CustomEnv()
        self.timer = pygame.time.Clock()


        # res = agent.predict(np.array([30]))
        # print(np.argmax(res[0]))

    def create_agent(self, trained=False):
        actions = self.env.action_space.n
        filepath = None
        states = None

        if trained:
            filepath = TRAINED_DIR_NAME
        else:
            states = self.env.observation_space.shape

        self.agent = Agent(actions=actions, states=states, filepath=filepath)

    def train_agent(self):
        history = self.agent.train(self.env )
        print(history.history.keys())

    def test_agent(self):
        self.env.create_screen()
        self.agent.test(self.env)

    def save_agent(self):
        self.agent.save()

    def run(self):
        pygame.init()
        pygame.time.set_timer(SCREEN_UPDATE, 100)
        self.env.create_screen()


        keyUpEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=pygame.KMOD_NONE)
        keyDowmEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=pygame.KMOD_NONE)
        count_done_base = 100
        count_done = count_done_base
        while self.running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.cleanup()

                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_UP:
                        self.env.action(Action.INCREASE)
                    elif ev.key == pygame.K_DOWN:
                        self.env.action(Action.DECREASE)

                if ev.type == SCREEN_UPDATE or True:
                    self.env.update()
                    self.env.show()

            observations = self.env.get_observations()
            decision = self.agent.predict(observations)

            if decision == 0:
                pygame.event.post(keyDowmEvent)
            elif decision == 2:
                pygame.event.post(keyUpEvent)

            pygame.display.update()

            self.timer.tick(60)

            if self.env.shower.get_temp() >= 37 and self.env.shower.get_temp() <= 39:
                count_done -= 1
            if count_done <= 0:
                count_done = count_done_base
                self.env.reset()



    def cleanup(self):
        pygame.quit()
        sys.exit(0)