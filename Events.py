#  Copyright (c) 2020.

from discord.ext import commands
from discord.ext.commands import Cog
from Embeds import Records
import sqlite3
import discord


class Event(Cog):
    def __init__(self, client: discord.Client):
        self.client = client
        self.r = Records
        self.conn = sqlite3.connect("main.sqlite")
        self.c = self.conn.cursor()

        self.c.execute(
            "CREATE TABLE IF NOT EXISTS nickname_record (id int PRIMARY KEY, user_id int, before_nick text, after_nick text)")
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS remove_role_record (id int PRIMARY KEY, user_id int, removed_role_id int)")
        self.c.execute("CREATE TABLE IF NOT EXISTS add_role_record (id int PRIMARY KEY, user_id int, add_role_id int)")

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        :Condition 1: Send Member Join Voice Channel Message
        :Condition 2: Send Member Leave Voice Channel Message and run :Condition 2.1:
        :Condition 2.1: Send a Stop Stream Message if stream stopped
        :Condition 3: Send Member Start AFK Message (Paused)
        :Condition 4: Send Member Stop AFK Message (Paused)
        :Condition 5: Send Member Move Voice Channel Message
        :Condition 6: Send Start Stream Message
        :Condition 7: Send Stop Stream Message
        """
        if before.channel is None and after is not None:
            await (self.client.get_channel(757097330557059092)).send(embed=self.r["join_channel"](member, before, after))
        elif before.channel is not None and after.channel is None:
            if before.self_stream: (self.client.get_channel(757097330557059092)).send(embed=self.r["stop_stream"](member, before, after))
            await (self.client.get_channel(757097330557059092)).send(embed=self.r["leave_channel"](member, before, after))
        elif after.afk:
            # await (self.client.get_channel(757097330557059092)).send(embed=self.r.start_afk(member, before, after))
            pass
        elif before.afk:
            # await (self.client.get_channel(757097330557059092)).send(embed=self.r.stop_afk(member, before, after))
            pass
        elif before.channel and after.channel and before.channel != after.channel:
            await (self.client.get_channel(757097330557059092)).send(embed=self.r["move_channel"](member, before, after))
        elif before.self_stream is False and after.self_stream:
            await (self.client.get_channel(757097330557059092)).send(embed=self.r["start_stream"](member, before, after))
        elif before.self_stream and after.self_stream is False:
            await (self.client.get_channel(757097330557059092)).send(embed=self.r["stop_stream"](member, before, after))

    @Cog.listener()
    async def on_member_update(self, before, after):
        """
        :Condition 1: Send Change Nickname Message
        :Condition 2: Send Removed Role Message
        :Condition 3: Send Add Role Message
        """
        if before.nick != after.nick:
            i = self.c.execute(f"SELECT * FROM nickname_record ORDER BY id DESC LIMIT 1").fetchone()
            await (self.client.get_channel(757154172054405127)).send(
                embed=self.r.change_nickname(int(i[0]) + 1, before, after))

            self.c.execute("INSERT INTO nickname_record (id, user_id, before_nick, after_nick) VALUES (?,?,?,?)",
                           (int(i[0]) + 1, before.id, before.nick, after.nick))
            self.conn.commit()

        elif len(before.roles) > len(after.roles):
            i = self.c.execute(f"SELECT * FROM remove_role_record ORDER BY id DESC LIMIT 1").fetchone()
            await (self.client.get_channel(757154172054405127)).send(
                embed=self.r.remove_role(int(i[0]) + 1, before, after))

            self.c.execute("INSERT INTO remove_role_record (id, user_id, changed_role_id) VALUES (?,?,?)",
                           (i[0] + 1, after.id, list(set(before.roles) - set(after.roles))[0].id))
            self.conn.commit()

        elif len(before.roles) < len(after.roles):
            i = self.c.execute("SELECT * FROM add_role_record ORDER BY id DESC LIMIT 1").fetchone()
            await (self.client.get_channel(757154172054405127)).send(
                embed=self.r.add_role(int(i[0]) + 1, before, after))
            self.c.execute("INSERT INTO add_role_record (id, user_id, add_role_id) VALUES (?,?,?)",
                           (i[0] + 1, after.id, list(set(after.roles) - set(before.roles))[0].id))
            self.conn.commit()
