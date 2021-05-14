# bot.py
import os
import requests as req
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
async def watch(ctx, *arg):
    if(len(arg)!=0):
        home = 'https://www.f2movies.to'
        url = home + '/search/' + '-'.join(arg)
        page = req.get(url)
        soup = bs(page.text,'html.parser')
        partLink = str(soup.find_all('a',class_='film-poster-ahref flw-item-tip',href=True)[0]['href'])
        await ctx.channel.send(home+partLink)
    
    else:
        await ctx.channel.send('Usage: - $watch moviename')
    

bot.run(TOKEN)