import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from Board import Board
from Dice import Dice
from Player import Player


def has_duplicate_or_invalid_values(lst):
    """ Check if given list contains any duplicates """
    for elem in lst:
        if lst.count(elem) > 1 or elem <= 0 or elem > 8:
            return False
    return True


class Game:

    # init method or constructor
    def __init__(self, file_name):
        self.board = None
        self.dice = None
        self.file_name = file_name
        self.init()

    def play(self, player1_name, player2_name):
        players = [Player(player1_name, Board.PLAYER_1_SYMBOL), Player(player2_name, Board.PLAYER_2_SYMBOL)]
        self.board.set_players(players)
        while not self.board.game_over():
            self.print()
            choice = ''
            for player in players:
                choice = self.play_move(player)
                if choice == 'q':
                    break

            if choice == 'q':
                break
        self.write_csv()
        self.print_stats()

    def write_csv(self):
        player1 = self.board.players[0]
        player2 = self.board.players[1]
        self.equalize_positions()
        player1_moves, player2_moves = self.get_moves_array()
        moves_data = {
            player1.name: player1_moves,
            player2.name: player2_moves
        }
        snake_ladder_data = {
            player1.name: [player1.snake_bites, player1.ladder_moves],
            player2.name: [player2.snake_bites, player2.ladder_moves],
        }

        positions_data = {
            player1.name: player1.positions,
            player2.name: player2.positions,
        }

        moves_df = pd.DataFrame(moves_data, index=self.dice.sides)
        stats_df = pd.DataFrame(snake_ladder_data, index=['snakes', 'ladders'])
        positions_df = pd.DataFrame(positions_data, index=list(range(1,
                                    max(len(player1.positions), len(player2.positions)) + 1)))
        moves_df.to_json('moves.json')
        stats_df.to_json('stats.json')
        positions_df.to_json('positions.json')

        print("\n\nMoves, Stats and Position dataframes saved to 'moves.json', 'stats.json' and 'positions.json' respectively.")

    def equalize_positions(self):
        player1 = self.board.players[0]
        player2 = self.board.players[1]
        if len(player1.positions) > len(player2.positions):
            max_ele = player2.positions[len(player2.positions) - 1]
            diff = len(player1.positions) - len(player2.positions)
            player2.positions.extend([max_ele] * diff)
        elif len(player2.positions) > len(player1.positions):
            max_ele = player1.positions[len(player1.positions) - 1]
            diff = len(player2.positions) - len(player1.positions)
            player1.positions.extend([max_ele] * diff)

    def get_moves_array(self):
        player1 = self.board.players[0]
        player2 = self.board.players[1]
        player1_moves = [0] * len(self.dice.sides)
        player2_moves = [0] * len(self.dice.sides)

        for i in range(0, len(self.dice.sides)):
            player1_moves[i] = player1.moves.get(self.dice.sides[i], 0)
            player2_moves[i] = player2.moves.get(self.dice.sides[i], 0)

        return player1_moves, player2_moves

    def print_stats(self):

        moves_df = pd.read_json('moves.json')
        stats_df = pd.read_json('stats.json')
        positions_df = pd.read_json('positions.json')

        print("Data frame loaded from 'moves.json' file\n", moves_df)
        print("Data frame loaded from 'stats.json' file\n", stats_df)
        print("Data frame loaded from 'positions.json' file\n", positions_df)

        self.print_moves_bar(moves_df)
        self.print_positions_histogram(positions_df)
        self.print_snakes_ladders(stats_df)

    def print_positions_histogram(self, positions_df):
        players = positions_df.keys()
        index = np.array(positions_df.index)
        plt.plot(index, positions_df[players[0]], label=players[0])
        plt.plot(index, positions_df[players[1]], label=players[1])
        plt.xlabel('Moves')
        plt.ylabel('Position')
        plt.title('Position of players with respect to moves')
        plt.legend()
        plt.show()

    def print_snakes_ladders(self, snakes_df):
        try:
            players = snakes_df.keys()

            fig, (ax1, ax2) = plt.subplots(1, 2)
            pie_labels1 = ['snakes: ' + str(snakes_df[players[0]].values[0]),
                           'ladders: ' + str(snakes_df[players[0]].values[1])]
            pie_labels2 = ['snakes: ' + str(snakes_df[players[1]].values[0]),
                           'ladders: ' + str(snakes_df[players[1]].values[1])]
            # Creating plot

            ax1.pie(snakes_df[players[0]], labels=pie_labels1, autopct=lambda p: '{:.0f} %'.format(p), startangle=50)
            ax1.title.set_text(players[0])
            ax2.title.set_text(players[1])
            ax2.pie(snakes_df[players[1]], labels=pie_labels2, autopct=lambda p: '{:.0f} %'.format(p), startangle=50)
            fig.suptitle('Snakes and ladders count ')

            # show plot
            plt.show()
        except:
            pass

    def print_moves_bar(self, moves_df):
        players = moves_df.keys()
        plt.style.use('ggplot')
        fig, ax = plt.subplots()
        bar_width = 0.35
        opacity = 0.9
        index = np.array(moves_df.index)
        ax.bar(index, moves_df[players[0]], bar_width, alpha=opacity, color='r',
               label=players[0])
        ax.bar(index + bar_width, moves_df[players[1]], bar_width, alpha=opacity, color='b',
               label=players[1])
        ax.set_ylabel('Count')
        ax.set_xlabel('Dice Value')
        ax.legend()
        plt.title('Dice values for the two players')
        plt.show()

    def play_move(self, player):
        choice = input(
            'Enter "q" to quit or any other key for rolling the dice {0}: '.format(player.name)).strip().lower()
        if choice == 'q':
            print(player.name + " decided to quit. Terminating game...!!!")
            return choice
        move = self.dice.roll()
        print('You got a ' + str(move))
        self.board.move(player, move)

        if player.position == self.board.target():
            return 'q'
        if move == 6:
            print('Yay... Free turn on getting 6.')
            self.play_move(player)

    def print(self):
        print("Current Games status: ")
        print(self.board)

    def init(self):
        f = open(self.file_name)
        try:
            data = json.load(f)
            self.parse_board(data)
            self.parse_snakes(data)
            self.parse_ladders(data)
            self.parse_dice(data)
        except Exception as e:
            print(e)
            print("Invalid file '{0}'.".format(self.file_name))
            print("Terminating application")
        finally:
            f.close()

    def parse_board(self, data):
        side = int(data['board']['side'])
        if side < 5 or side > 15:
            print("Invalid board. Side of board can't be less than 5 or greater than 15")
            raise Exception()
        self.board = Board(side)

    def parse_snakes(self, data):
        snakes = data['snakes']

        for snake in snakes:
            try:
                if snake['tail'] <= 0 or snake['head'] >= self.board.target() or snake['head'] < snake['tail']:
                    raise Exception()
                else:
                    valid = True
                    for sn in self.board.snakes:
                        if sn.head + 1 == snake['head']:
                            print('Invalid snake config:', snake, ';A snake with this start position already exists.')
                            valid = False
                    if valid:
                        self.board.add_snake(snake['head'] - 1, snake['tail'] - 1)
            except Exception as e:
                print(e)
                print('Invalid snake config:', snake)

    def parse_ladders(self, data):
        ladders = data['ladders']

        for ladder in ladders:
            try:
                if ladder['start'] <= 0 or ladder['end'] >= self.board.target() or ladder['start'] > ladder['end']:
                    raise Exception()
                else:
                    valid = True
                    for ld in self.board.ladders:
                        if ld.start + 1 == ladder['start']:
                            print('Invalid ladder config:', ladder,
                                  ';A ladder with this start position already exists.')
                            valid = False
                    for sn in self.board.snakes:
                        if sn.head + 1 == ladder['start'] or sn.head + 1 == ladder['end'] or sn.tail + 1 == ladder[
                                    'start'] or sn.tail + 1 == ladder['end']:
                            print('Invalid ladder config:', ladder, '; It is contradictory to snake', sn)
                            valid = False
                    if valid:
                        self.board.add_ladder(ladder['start'] - 1, ladder['end'] - 1)
            except Exception as e:
                print(e)
                print('Invalid ladder config:', ladder)

    def parse_dice(self, data):
        sides = data['dice']
        if len(sides) < 4:
            print("The dice should have at least 4 sides.")
            raise Exception()
        if not has_duplicate_or_invalid_values(sides):
            print("The dice values are invalid.")
            raise Exception()
        self.dice = Dice(sides)
