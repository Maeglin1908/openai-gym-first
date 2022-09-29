import os

from game import Game
from utils import TRAINED_DIR_NAME


def app():

    game = Game()

    # if not os.path.exists(TRAINED_DIR_NAME):
    #     game.create_agent()
    #     game.train_agent()
    #     game.save_agent()
    #
    # game.create_agent(True)
    # game.test_agent()

    game.create_agent(trained=True)
    game.run()

if __name__ == '__main__':
    app()