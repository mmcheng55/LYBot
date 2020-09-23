#  Copyright (c) 2020.
import quart.flask_patch

from quart import Quart, render_template, redirect, url_for, send_from_directory, request, abort, send_file
from flask_discord import DiscordOAuth2Session, requires_authorization
from socket import gethostbyname, gethostname
from discord.ext import commands
from Events import Event

import flask_discord
import GameEngine
import discord
import asyncio
import sqlite3
import random
import string
import json
import os

os.chdir(r"E:\Projects\LightYear")

l = asyncio.get_event_loop()
client = commands.Bot(command_prefix=commands.when_mentioned_or(";"), loop=l, help_command=None)
app = Quart(__name__)

with open("secured/info.json", "r", encoding="utf8") as file:
    data = json.load(file)

app.config["SECRET_KEY"] = data["KEY"].encode("unicode-escape")
app.config["DISCORD_CLIENT_ID"] = data["ID"]
app.config["DISCORD_CLIENT_SECRET"] = data["SECRET"]
app.config["DISCORD_BOT_TOKEN"] = data["TOKEN"]
app.config["DISCORD_REDIRECT_URI"] = f"http://{gethostbyname(gethostname())}/callback" if gethostbyname(
    gethostname()) != "192.168.128.136" else "http://r6.themichael-cheng.com/callback"
app.config["UPLOAD_FOLDER"] = "/static/upload/"

dc = DiscordOAuth2Session(app)

with sqlite3.connect("main.sqlite") as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS image (id STRING PRIMARY KEY, ext STRING)")


@client.event
async def on_ready():
    print(f"Online as {client.user}")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("http://r6.themichael-cheng.com"))


@client.event
async def on_member_join(member):
    with open("secured/messages.json", "r", encoding="utf8") as file:
        data = json.load(file)

        await (await client.fetch_channel(753109524327432193)).send(
            data["JOIN"].format(user=member.mention, server="Light Year"))


@client.event
async def on_member_remove(member):
    with open("secured/messages.json", "r", encoding="utf8") as file:
        data = json.load(file)

        await (await client.fetch_channel(753109524327432193)).send(
            data["EXIT"].format(user=member.display_name, server="Light Year"))


@client.command(name=["help"])
async def help_(ctx, cmd="1"):
    if cmd not in ["gamble", "events", "1"]:
        cmd = "1"

    await ctx.send(">>> " + {"1": "1. `;help <page>` Show This Command\nSupported List: `gamble`, `event`", "gamble": "1. `;dice` Get a random Number\n2.`;flip_coin` To flip coin"}[cmd])



@client.command()
async def dice(ctx):
    await ctx.send(f":dice: You got {GameEngine.Gamble.dice()}")


@client.command()
async def flip_coin(ctx):
    await ctx.send(f":money_with_wings: You got {GameEngine.Gamble.flip_coin()}")


def check_user():
    try:
        dc.fetch_user()
    except:
        return False
    else:
        return True


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/login")
async def login():
    return dc.create_session()


@app.route("/callback/")
async def callback():
    await dc.callback_quart()

    if 747638406342901780 in [d.id for d in dc.fetch_guilds()] and 747640538211024977 in [u.id for u in (
    await (await client.fetch_guild(747638406342901780)).fetch_member(dc.fetch_user().id)).roles]:
        return redirect(url_for("console"))

    return redirect(url_for("logout"))


@app.route("/logout")
async def logout():
    dc.revoke()
    return redirect(url_for('index'))


@app.route("/console")
@requires_authorization
async def console():
    with open("secured/messages.json", encoding="utf8") as file:
        data = json.load(file)
        return await render_template("Console/index.html", join=data["JOIN"])


@app.route("/handle", methods=["POST"])
@requires_authorization
async def handle():
    if request.args.get("type") == "welcome":
        with open("secured/messages.json") as file:
            data = json.load(file)
            data["JOIN"] = (await request.form).get("message")


@requires_authorization
@app.route("/image", methods=["GET", "POST"])
async def img_home():
    if request.method == "POST":
        f = (await request.files)["image"]
        with sqlite3.connect("main.sqlite") as conn:
            c = conn.cursor()
            while True:
                code = "".join(random.sample([*string.ascii_letters, *string.digits, "_", "-"], 5))
                print(code)
                if not c.execute(f"SELECT * FROM image WHERE id='{code}'").fetchone():
                    c.execute(f"INSERT INTO image (id, ext) VALUES ('{code}', '{os.path.splitext(f.filename)[1]}')")
                    break
            conn.commit()
        open(f"./static/upload/image/{code + os.path.splitext(f.filename)[1]}", "w").close()
        f.save(f"./static/upload/image/{code + os.path.splitext(f.filename)[1]}")
        return await render_template("Image/success.html", img=code)
    return await render_template("Image/share_image.html")


@app.route("/show_img/<img_id>/dl")
async def image_download(img_id):
    with sqlite3.connect("main.sqlite") as conn:
        c = conn.cursor()
        if not c.execute(f"SELECT * FROM image WHERE id='{img_id}'").fetchone():
            abort(404)
        a = c.execute(f"SELECT * FROM image WHERE id='{img_id}'").fetchone()
        return await send_from_directory(f"./static/upload/image", file_name=img_id + a[1], as_attachment=True)


@app.route("/show_img/<img_id>")
async def show_image(img_id):
    with sqlite3.connect("main.sqlite") as conn:
        c = conn.cursor()
        if not c.execute(f"SELECT * FROM image WHERE id='{img_id}'").fetchone():
            abort(404)

        return await render_template("Image/show_img.html", image=img_id,
                                     ext=c.execute(f"SELECT * FROM image WHERE id='{img_id}'").fetchone()[1])


@client.command()
async def get_img(ctx, img_id):
    with sqlite3.connect("main.sqlite") as conn:
        c = conn.cursor()
        r = c.execute(f"SELECT * FROM image WHERE id='{img_id}'").fetchone()
        if not r: return await ctx.send("Image ID {} not found.".format(r[0]))
        await ctx.send(file=discord.File(f"./static/upload/image/{img_id}{r[1]}"))


@app.errorhandler(flask_discord.exceptions.AccessDenied)
async def access_denied():
    pass


app.jinja_env.globals.update(check_user=check_user)
client.add_cog(Event(client))
app.run(host=gethostbyname(gethostname()), port=80, loop=l, start_now=False)
client.run(data["TOKEN"])
