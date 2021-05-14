# bot.py
import os
import requests
from bs4 import BeautifulSoup as bs
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.channel.send('Pong! {:.2f}ms'.format(bot.latency))

@bot.command()
async def m(ctx, *arg):
    mName = " ".join(arg[:])
    await ctx.channel.send(f'So, you wanna watch {mName}, huh?')

bot.run(TOKEN)