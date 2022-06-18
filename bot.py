# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

import eyetrack as eye
bar = ''

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    # channel = client.get_channel(986162355698294834)
    # await channel.send('hello')

    if message.author == bot.user:
        return
    if message.content == 'hey bot':
        await message.channel.send('what u want')

    if message.content == 'bot you seeing this?':
        await message.channel.send('what where')
    await bot.process_commands(message)

    
foo = 0
@bot.command()
async def increase(ctx):
    global foo
    await ctx.send(foo)
    foo += 1


@bot.command()
async def test(ctx, arg1, arg2):
    await ctx.send('You passed {} and {}'.format(arg1, arg2))

@bot.command()
async def result(ctx):
    global bar
    bar = eye.returnvalue()
    await ctx.send(bar)

bot.run(TOKEN)