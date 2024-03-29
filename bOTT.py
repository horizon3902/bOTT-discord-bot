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
    embed.add_field(name="$watch titlename", value="Sends links of relevant requested title", inline=False)
    embed.add_field(name="$imdb tiltename", value="Shows IMDb rating of requested title", inline=False)
    embed.add_field(name="$trending movie/$trending tv", value="Shows top 5 trending movies/tv shows of the day", inline=False)
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
        partLink = soup.find_all('a',class_='film-poster-ahref flw-item-tip',href=True)
        await ctx.channel.send('Top results:-')
        for idx, x in enumerate(partLink[:3]):
            await ctx.channel.send(f'{idx+1}.')
            await ctx.channel.send(home+str(x['href']))
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
        embed.add_field(name="Visit the IMDb Page: -",
                        value=f"https://imdb.com/title/tt{movies[0].getID()}\nPro Tip: If incorrect result displayed, "
                              f"try adding year of movie/tv show to the query",
                        inline=False)
        embed.set_thumbnail(url=movies[0]['full-size cover url'])
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

@bot.command()
async def trending(ctx, *arg):
    if(arg[0] in ['movie','tv']):
        api_key = os.getenv('TMDB_API_KEY')
        base_url = "https://api.themoviedb.org/3/trending"
        thumb_base_url = "https://image.tmdb.org/t/p/w500"
        url = base_url + '/' + arg[0] + '/day?api_key=' + api_key
        r = req.get(url)
        data = r.json()
        await ctx.channel.send('Top 5 Trending ' + arg[0] + 's:-')
        for entity in data['results'][:5]:
            if(arg[0]=='movie'):
                embed=discord.Embed(title=entity['title'])
                embed.add_field(name="Visit the TMDb Page: -",
                            value=f"https://tmdb.com/movie/{entity['id']}",
                            inline=False)
            elif(arg[0]=='tv'):
                embed=discord.Embed(title=entity['name'])
                embed.add_field(name="Visit the TMDb Page: -",
                            value=f"https://tmdb.com/tv/{entity['id']}",
                            inline=False)
            # embed.add_field(name="Overview", value=entity['overview'], inline=False)
            embed.set_thumbnail(url=thumb_base_url + entity['poster_path'])
            await ctx.send(embed=embed)
            
    else:
        await ctx.channel.send('Usage: - $trending tv / $trending movie')

bot.run(TOKEN)