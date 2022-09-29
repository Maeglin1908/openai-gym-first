import keras.models
import numpy as np
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy

from utils import TRAINED_DIR_NAME


class Agent:

    def __init__(self, actions, states=None, filepath=None):
        policy = BoltzmannQPolicy()
        memory = SequentialMemory(limit=50000, window_length=1)
        model = None
        if filepath != None:
            model = keras.models.load_model(filepath=filepath)
        elif states != None and actions != None:
            model = Sequential()
            model.add(Dense(24, activation="relu", input_shape=states))
            model.add(Dense(24, activation="relu"))
            model.add(Dense(actions, activation="linear"))

        if model == None:
            print("ERROR DURING AGENT INITIALIZATION")
            return

        self.model = model
        self.model.summary()

        self.dqn = DQNAgent(model=self.model, memory=memory, policy=policy,
                            nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)

        self.dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    def summary(self):
        self.model.summary()

    def save(self):
        self.model.save(filepath=TRAINED_DIR_NAME)

    def predict(self, observations):
        best = np.argmax(self.model.predict(observations)[0])
        return best


    def train(self, env):
        return self.dqn.fit(env, nb_steps=100000, visualize=False, verbose=1)

    def test(self, env):
        self.dqn.test(env=env, nb_episodes=100, visualize=True )