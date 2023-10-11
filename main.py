import discord
import asyncio
import os
from discord.ext import commands

from rule34Py import rule34Py
r34Py = rule34Py()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='r//',intents=intents)

@bot.event

async def change_activity():
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="the horny | r//help"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with myself | r//help"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with you~ | r//help"))
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    bot.loop.create_task(change_activity())
    print(f'Logged in as {bot.user.name}')
    print("Using Rule34Py v" + r34Py.version)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def post(ctx, query, num_posts=1):
    if num_posts > 5:
        await ctx.send("Sorry, the maximum number of posts is 5.")
        return
    await ctx.send(f'Searching for {query}...')
    result_search = r34Py.search([query], limit=num_posts)
    if not result_search:
        await ctx.send("No results found.")
        return
    links = ""
    for post in result_search:
        if "scat" in post.tags or "bestiality" in post.tags:
            links += "filtered\n" + post.tags + "\n"
        else:
            links += post.image + "\n" + post.tags + "\n"
    await ctx.send(links)
bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of available commands", color=0x00ff00)
    embed.add_field(name="ping", value="Returns 'Pong!'", inline=False)
    embed.add_field(name="post", value="Searches for posts on rule34 with the given query and returns the links to the images. Maximum of 5 posts. Usage example: r//post catgirl 3", inline=False)
    await ctx.send(embed=embed)

bot.run(os.getenv('TOKEN'))
