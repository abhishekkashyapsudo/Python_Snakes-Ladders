import numpy
from matplotlib import pyplot as plt


from Ladder import Ladder
from Snake import Snake

from termcolor import colored


class Board:
    PLAYER_1_SYMBOL = '★'
    PLAYER_2_SYMBOL = '♥'

    # init method or constructor
    def __init__(self, side):
        self.side = side
        self.board = numpy.arange(1, side * side + 1, dtype=object)
        self.snakes = []
        self.ladders = []
        self.players = []

    def target(self):
        return self.board[-1]

    def set_players(self, players):
        self.players = players

    def add_snake(self, head, tail):
        self.snakes.append(Snake(head, tail))

    def add_ladder(self, start, end):
        self.ladders.append(Ladder(start, end))

    def get_ladders_snakes(self):
        array = ["{0: <15} {1: <15}".format('Ladders', 'Snakes')]
        length = min(len(self.ladders), len(self.snakes))

        for i in range(0, length):
            array.append(
                "{0: <15} {1: <15}".format(str(self.ladders[i].start + 1) + ' -> ' + str(self.ladders[i].end + 1),
                                           str(self.snakes[i].head + 1) + ' -> ' + str(self.snakes[i].tail + 1)))

        if length < len(self.ladders):
            for i in range(length, len(self.ladders)):
                array.append(
                    "{0: <15} {1: <15}".format(str(self.ladders[i].start + 1) + ' -> ' + str(self.ladders[i].end + 1),
                                               ''))

        if length < len(self.snakes):
            for i in range(length, len(self.snakes)):
                array.append("{0: <15} {1: <15}".format('',
                                                        str(self.snakes[i].head + 1) + ' -> ' + str(
                                                            self.snakes[i].tail + 1)))

        return array[::-1]

    def game_over(self):
        return self.players[0].position == self.target() or self.players[1].position == self.target()

    def add_snakes_to_board(self):
        snake_index = 1
        for snake in self.snakes:
            self.board[snake.head] = ' ' + colored('S' + '{0:>3}'.format(str(snake_index)
                                                                         + 'H'), 'red',
                                                   attrs=["underline"])
            self.board[snake.tail] = ' ' + colored('S' + '{0:>3}'.format(str(snake_index) +
                                                                         'T'), 'yellow')
            snake_index += 1

    def add_ladders_to_board(self):
        ladder_index = 1
        for ladder in self.ladders:
            self.board[ladder.start] = ' ' + colored('L' + '{0:>3}'.format(str(ladder_index) + 'S'), 'green',
                                                     attrs=["underline"])
            self.board[ladder.end] = ' ' + colored('L' + '{0:>3}'.format(str(ladder_index) + 'E'), 'cyan')
            ladder_index += 1

    def __str__(self):
        self.add_snakes_to_board()
        self.add_ladders_to_board()
        snakes_ladders = self.get_ladders_snakes()
        res = ''
        final_result = ' ' * 31 + '#' + '------#' * self.side
        element = 0
        to_right = True
        s_l_index = 0
        line_num = 0
        for ii in range(0, len(self.board)):
            i = self.board[ii]
            symbol = self.get_player(ii + 1)
            element += 1
            if to_right:
                res += symbol + '|' if not symbol.strip() == '' else '{0: >5}'.format(i) + ' |'
            else:
                res = (symbol + '|' if not symbol.strip() == '' else '{0: >5}'.format(i) + ' |') + res
            if element == self.side:

                if s_l_index < len(snakes_ladders):
                    final_result = snakes_ladders[s_l_index] + '#' + res[:-1] + '#' + self.add_player_details(
                        line_num) + '\n' + final_result
                    line_num += 1
                    s_l_index += 1
                else:
                    final_result = '{0:<31}'.format('') + '#' + res[:-1] + '#\n' + final_result
                res = ''
                element = 0
                to_right = not to_right
        final_result = ' ' * 31 + '#------' * self.side + '#\n' + final_result
        return final_result

    def get_player(self, index):
        res = ''
        player1 = self.players[0]
        player2 = self.players[1]
        if self.players_at_same_position() and player1.position == index:
            res += player1.symbol + player2.symbol
        elif player1.position == index:
            res += player1.symbol
        elif player2.position == index:
            res += player2.symbol
        return '{:^6s}'.format(res)

    def players_at_same_position(self):
        return self.players[0].position == self.players[1].position

    def move(self, player, value):

        if player.position + value > self.target():
            print("Oops... You need a lower move to win.")
        else:
            player.move(value)
            # you won
            if player.position == self.target():
                print("Yay... Congrats " + player.name + '. You have won the game.')
            ladder = self.get_ladder_at(player.position)
            snake = self.get_snake_at(player.position)

            if ladder is not None:
                print("Yay... You got a ladder. Moving you to position " + str(ladder.end + 1))
                player.position = ladder.end + 1
                player.add_ladder_moves()
            elif snake is not None:
                print("Oops... You got a snake. Moving you to position " + str(snake.tail + 1))
                player.position = snake.tail + 1
                player.add_snake_bite()
            else:
                print(player.name + ' moved to position ' + str(player.position) + '.')

    def get_ladder_at(self, position):

        for ladder in self.ladders:
            if ladder.start + 1 == position:
                return ladder
        return None

    def get_snake_at(self, position):

        for snake in self.snakes:
            if snake.head + 1 == position:
                return snake
        return None

    def add_player_details(self, index):
        player1 = self.players[0]
        player2 = self.players[1]
        array = ["     {0:1} -> {1: <25}".format(player1.symbol, player1.name + "'s symbol."),
                 "     {0:1} -> {1: <25}".format(player2.symbol, player2.name + "'s symbol."),
                 "     Player symbols: "]
        if index < len(array):
            return array[index]
        return ''
