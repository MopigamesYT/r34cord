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
    if num_posts > 5:
        await ctx.send("Sorry, the maximum number of posts is 5.")
        return
    await ctx.send(f'Searching for {query}...')
    result_search = r34Py.search([query], limit=num_posts)
    links = ""
    for post in result_search:
        links += post.image + "\n"
    await ctx.send(links)
    # BEGIN: 2d5f1d7d7d5d
bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of available commands", color=0x00ff00)
    embed.add_field(name="ping", value="Returns 'Pong!'", inline=False)
    embed.add_field(name="post", value="Searches for posts on rule34 with the given query and returns the links to the images. Maximum of 5 posts. Usage example: r//post catgirl 3", inline=False)
    await ctx.send(embed=embed)
    

bot.run('MTE1OTk2MjUxNTI5MjI5OTI3Ng.GonXlC.l0QNKBtB_lQ8_Kc1I1lZfc2bC_Y-dPxyVvhTQw')

