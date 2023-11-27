import discord
import asyncio
import os
import random
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View

from rule34Py import rule34Py
r34Py = rule34Py()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bot = commands.Bot(command_prefix='r//',intents=intents)

print(os.getenv('TOKEN'))

@bot.event
async def change_activity():
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="the horny | /help"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with myself | /help"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with you~ | /help"))
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    bot.loop.create_task(change_activity())
    print(f'Logged in as {bot.user.name}')
    print("Using Rule34Py v" + r34Py.version)
    print(os.getenv('TOKEN'))
    try:
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} commands.")
    except Exception as e:
        print(e)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of available commands", color=0x00ff00)
    embed.add_field(name="ping", value="Returns 'Pong!'", inline=False)
    embed.add_field(name="post", value='Searches for posts on rule34 with the given tags and returns the links to the images. Maximum of 5 posts. Usage example: r//post "catgirl, lesbian" 3', inline=False)
    await ctx.send(embed=embed)

@bot.tree.command(name="ping")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong!")

@bot.tree.command(name="r34")
@app_commands.describe(query="The tags to search for. can be multiple and separated by a space.", num_posts="The number of posts to return. Maximum of 5.")
async def r34_command(interaction: discord.Interaction, query: str, num_posts: int = 1):
    await perform_r34_search(interaction, query, num_posts)

async def perform_r34_search(interaction, query, num_posts):
    more = Button(label="More", style=discord.ButtonStyle.blurple, emoji="➕")
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message("Sorry, I can't submit NSFW content in a non-NSFW category.")
        return
    if num_posts > 5:
        await interaction.response.send_message("Sorry, the maximum number of posts is 5.")
        return
    result_search = r34Py.search([query], limit=50)
    random.shuffle(result_search)
    links = ""
    buttons = []

    if not result_search:
        await interaction.response.send_message("Nothing was found! make sure that your tags exists and that you use space as separator for multiple tags.")
        return

filtered_tags = ["scat", "beastiality", "zoophilia"]

for i in range(num_posts):
    if i < len(result_search):
        post = result_search[i]
        if any(tag in post.tags for tag in filtered_tags):
            links += "filtered\n"
        else:
            if post.content_type == "video":
                links += f"[{i + 1}] \nThis is a video! Click on the Source button to see it on r34!\n"
            else:
                links += f"[{i + 1}]\n{post.image}\n"
            button = Button(label=f"[{i + 1}] Source", style=discord.ButtonStyle.primary, url=f"https://rule34.xxx/index.php?page=post&s=view&id={post.id}")
            buttons.append(button)
    else:
        break

    async def button_callback(interaction):
        await perform_r34_search(interaction, query, num_posts)

    more.callback = button_callback

    view = View()
    for button in buttons:
        view.add_item(button)

    if buttons:
        view.add_item(more)

    interaction.response.send_message(links, view=view)




bot.run(os.getenv('TOKEN'))
