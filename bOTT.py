# bot.py
import os
import requests as req
from bs4 import BeautifulSoup as bs
import discord
from discord.ext import commands
from dotenv import load_dotenv
import urllib
from re import findall
from imdb import Cinemagoer, IMDbError

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

i = Cinemagoer()

intents=discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="$", help_command=None, intents=intents)

@bot.event
async def on_ready():
    servers = list(bot.guilds)
    print('We have logged in as {0.user}'.format(bot))
    print('\n'.join(guild.name for guild in servers))

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="bOTT - TV and Movies", description="Get the link for your movie or TV show, join a voice channel and share your screen with your friends to watch a movie together!\n\nCommands: -")
    embed.set_thumbnail(url="https://res.cloudinary.com/horizon3902/image/upload/v1621056104/color_logo_with_background_pvoe1n.png")
    embed.add_field(name="$watch titlename", value="Sends link of requested title", inline=False)
    embed.add_field(name="$imdb tiltename", value="Shows IMDb rating of requested title", inline=False)
    embed.add_field(name="$trailer titlename", value="Sends YouTube trailer link of the requested title", inline=False)
    embed.add_field(name="$ping", value="Check bot's response time", inline=False)
    await ctx.send(embed=embed)

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

@bot.command()
async def imdb(ctx, *arg):
    if(len(arg)!=0):
        movies = i.search_movie((' ').join(arg).lower(), results=1)
        i.update(movies[0])
        embed=discord.Embed(title='IMDb Rating')
        rating = movies[0]['rating']
        embed.add_field(name=movies[0]['title'], value=rating, inline=False)
        embed.add_field(name="Visit the IMDb Page: -", value=f"https://imdb.com/title/tt{movies[0].getID()}",
                        inline=False)
        await ctx.send(embed=embed)

    else:
        await ctx.channel.send('Usage: - $imdb titlename')

@bot.command()
async def trailer(ctx, *arg):
    home = "https://www.youtube.com/results?search_query="
    tquery = ' '.join(arg) + ' trailer'
    url = home + urllib.parse.quote(tquery)
    page = urllib.request.urlopen(url)
    vid = findall(r'watch\?v=(\S{11})',page.read().decode())[0]
    vidlink = "https://www.youtube.com/watch?v=" + vid
    await ctx.channel.send(vidlink)

bot.run(TOKEN)