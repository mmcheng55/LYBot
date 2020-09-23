#  Copyright (c) 2020.
import random


class Gamble(object):
    def __init__(self):
        pass

    @staticmethod
    def flip_coin():
        return random.choice(["Heads", "Tails"])

    @staticmethod
    def dice():
        return random.randint(1, 6)