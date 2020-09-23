#  Copyright (c) 2020.
import discord
import sqlite3


class Player(object):
    def __init__(self, player_id):
        self.player_id = player_id
        self.get_records()

    @classmethod
    def create_and_load_player(cls, db, player: discord.Member):
        cls.conn = sqlite3.connect(db)
        cls.c = cls.conn.cursor()
        cls.c.execute("CREATE TABLE IF NOT EXISTS player (player_id int PRIMARY KEY)")

        if not cls.c.execute(f"SELECT * FROM player (player_id={player.id})").fetchone():
            cls.conn = sqlite3.connect(db)
            cls.c.execute(f"INSERT INTO player (player_id={player.id})")
            cls.conn.commit()
            return cls(player.id)

        return cls(player.id)