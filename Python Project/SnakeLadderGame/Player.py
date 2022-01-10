class Player:

    # init method or constructor
    def __init__(self, name, sym):
        self.name = name

        symbol = self.name.upper()[0:2] + sym
        self.symbol = symbol
        self.position = 1
        self.moves = {}
        self.positions = [0]
        self.snake_bites= 0
        self.ladder_moves = 0
        pass

    def move(self, value):
        self.position += value
        self.positions.append(self.position)
        count = self.moves.get(value, 0)
        self.moves[value] = count + 1

    def add_snake_bite(self):
        self.snake_bites += 1

    def add_ladder_moves(self):
        self.ladder_moves += 1
