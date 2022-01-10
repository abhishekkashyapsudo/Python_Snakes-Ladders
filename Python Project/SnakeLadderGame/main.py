from Game import Game
from os.path import exists

from InputUtil import read_string

import pandas as pd


def main():

    positions_df = pd.read_json('stats.json')

    file = get_file_name()
    game = Game(file)
    player1 = read_string("Enter the name for player 1: ")
    player2 = read_string("Enter the name for player 2: ")
    game.play(player1, player2)


def get_file_name():
    valid_file = False
    file = None
    while not valid_file:
        file = read_string("Enter the name of the configuration file: ")
        if exists(file):
            valid_file = True
        else:
            print("No such file", file, "exists.")
    return file


# https://m.media-amazon.com/images/I/51wju4a7HYL.jpg
# current game screen
if __name__ == '__main__':
    main()

