import random
import numpy as np
class Dice:

    # init method or constructor
    def __init__(self, sides):
        self.sides = np.array(sides, dtype=int)

    def roll(self):
        rand_idx = random.randrange(len(self.sides))
        return self.sides[rand_idx]

