import discord

from discord.ext import commands

from rule34Py import rule34Py
r34Py = rule34Py()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='r//',intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print("Using Rule34Py v" + r34Py.version)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def post(ctx, query, num_posts=1):
    await ctx.send(f'Searching for {query}...')
    result_search = r34Py.search([query], limit=num_posts)
    for post in result_search:
        await ctx.send(post.image)
        await ctx.send(post.tags)

bot.run('MTE1OTk2MjUxNTI5MjI5OTI3Ng.GonXlC.l0QNKBtB_lQ8_Kc1I1lZfc2bC_Y-dPxyVvhTQw')

