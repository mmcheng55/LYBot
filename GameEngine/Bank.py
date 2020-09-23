#  Copyright (c) 2020.
from .Player import Player

import sqlite3


class Bank(object):
    def __init__(self, player: Player):
        self.player = player
        self.conn = player.conn
        self.c = player.c
        self.create()

    def create(self): pass