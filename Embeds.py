#  Copyright (c) 2020.
import datetime
import discord

Records = {
    "join_channel": lambda member, before, after: discord.Embed(description=f":white_check_mark: [{datetime.datetime.now()}] **{member.display_name}** joined voice channel `{after.channel}`.", color=discord.Color.green()),
    "leave_channel": lambda member, before, after: discord.Embed(description=f":small_red_triangle_down: [{datetime.datetime.now()}] **{member.display_name}** left voice channel `{before.channel}`.", color=discord.Color.red()),
    "start_afk": lambda member, before, after: discord.Embed(description=f"<:BOT_IDLE:757214065679663144> [{datetime.datetime.now()}] **{member.display_name}** started afk."),
    "stop_afk": lambda member, before, after: discord.Embed(description=f":green_circle: [{datetime.datetime.now()}] **{member.display_name}** stopped afk and went to channel {after.channel}"),
    "move_channel": lambda member, before, after: discord.Embed(description=f":arrow_right: [{datetime.datetime.now()}] **{member.display_name}** went from `{before.channel}` to `{after.channel}`", color=discord.Color.blue()),
    "start_stream": lambda member, before, after: discord.Embed(description=f":desktop: [{datetime.datetime.now()}] **{member.display_name}** started streaming in channel `{after.channel}`.", color=discord.Color.green()),
    "stop_stream": lambda member, before, after: discord.Embed(description=f":desktop: [{datetime.datetime.now()}] **{member.display_name}** stopped streaming in channel `{before.channel}`.", color=discord.Color.red()),
    "change_nickname": lambda id, before, after: discord.Embed(title=f":information_source: Nickname Change | #{id}", description=f"The User **{before.name}** has changed his nickname to {before.nick} to {after.nick}", color=discord.Color.blue()),
    "add_role": lambda id, before, after: discord.Embed(title=f":information_source: Role added | #{id}", description=f"The user **{after.display_name}** was added to role **{list(set(after.roles) - set(before.roles))[0]}**", color=discord.Color.green()),
    "remove_role": lambda id, before, after: discord.Embed(title=f":information_source: Role removed | #{id}", description=f"The user **{after.display_name}** was removed role **{list(set(before.roles) - set(after.roles))[0]}**", color=discord.Color.red()) ,
}


