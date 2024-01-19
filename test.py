import discord, os
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.environ.get("TOKEN")

bot = commands.Bot(command_prefix='!', self_bot=True)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    await bot.change_presence(activity=discord.Game(name='Hello World'), status=discord.Status.dnd)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        if message.content.startswith('!chat'):
            await message.channel.send('REPLY HERE')

bot.run(TOKEN)
 