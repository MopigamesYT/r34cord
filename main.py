import discord
import asyncio
import os
from discord.ext import commands

print()

from rule34Py import rule34Py
r34Py = rule34Py()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='r//',intents=intents)

print(os.getenv('TOKEN'))

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
    print(os.getenv('TOKEN'))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

import random

@bot.command()
@commands.is_nsfw()
async def post(ctx, query, num_posts=1):
    if num_posts > 5:
        await ctx.send("Sorry, the maximum number of posts is 5.")
        return
    await ctx.send(f'Searching for {query}...')
    result_search = r34Py.search([query], limit=50)  # Search for 50 images

    if not result_search:
        await ctx.send("No results found.")
        return

    # Shuffle the search results to make them random
    random.shuffle(result_search)

    links = ""
    for i in range(num_posts):
        if i < len(result_search):
            post = result_search[i]
            if "scat" in post.tags or "beaastiality" in post.tags or "zoophilia" in post.tags:
                links += "filtered\n"
                print(post.tags)
            else:
                links += post.image + "\n"
                print(post.tags)
        else:
            break #

    await ctx.send(links)

@post.error
async def post_error(ctx, error):
    if isinstance(error, commands.NSFWChannelRequired):
        await ctx.send(f"Hey! {ctx.author.mention}, sorry but I can't submit NSFW content without an NSFW category.")


bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of available commands", color=0x00ff00)
    embed.add_field(name="ping", value="Returns 'Pong!'", inline=False)
    embed.add_field(name="post", value='Searches for posts on rule34 with the given query and returns the links to the images. Maximum of 5 posts. Usage example: r//post "catgirl, lesbian" 3', inline=False)
    await ctx.send(embed=embed)
bot.run(os.getenv('TOKENDEV'))
