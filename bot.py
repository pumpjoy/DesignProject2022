"""
1. /TODO 'TRIGGER' WHEN FIRST CHANGE 1.0 TO 0.0 AND 0.0 TO 0.1 SO ONLY 1 RESULT() RUNS
2. / TODO STOP THE WHOLE OPERATION OF LOOPING() WHEN RESULT() IS RUNNING FOR A WHILE
3.  TODO (INTERRUPTION) add STOP() function that interrupts LOOPING() and stop the process
- CURRENTLY INTERRUPT BREAKS THE WHOLE DISCORD CONNECTION
- SOMETHING IS WRONG AT THE CORE OF THIS CODE, MAYBE RESTRUCTURE TO TASK?
"""
# bot.py
import eyetrack as eye
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import asyncio

from pylsl import StreamInlet, resolve_stream
""" custom opencv eyetracking libraries"""

""" main functions """
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

"""the real deal is here"""
camis = 0
anotherfoo = 'Built-in cam'
""" used to triger focused state so result doesnt keep running when looping detects multiple 1s in a row"""
trigger = 0
supposedletter = ""

@bot.command()
async def changecam(ctx, arg1: int):
    global camis
    global anotherfoo

    if arg1 == camis:
        await ctx.send(f'Configuration is already {camis} which is {anotherfoo}')
        return

    if arg1 != 0 and arg1 != 1:
        await ctx.send('Only 0 or 1 is accepted. 0 for Built-in cam, 1 for External cam 1.')
        return
    else:
        camis = arg1
        if camis == 0:
            anotherfoo = 'Built-in cam'
        elif camis == 1:
            anotherfoo = 'External cam 1'

        await ctx.send(f'Done. Cam is set to {camis}, {anotherfoo}')
        await ctx.send("You seeing this?")


def result():
    global camis, supposedletter
    bar = eye.returnvalue(camis)
    supposedletter += bar
    print(f"{supposedletter} {bar}" )
    """only prints on 1 channel currently"""
    bot.loop.create_task(bot.get_channel(986162355698294834).send(supposedletter))


@bot.command()
async def loopem(ctx):
    global trigger
    """print to channel saying: Running loop"""
    task = bot.loop.create_task(bot.get_channel(
        986162355698294834).send("Running loop"))
    await asyncio.sleep(1)
    task.cancel()

    """ Connect to OPENBCI's LSL network to get focused state"""
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])
    try:
        while True:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            
                sample, timestamp = inlet.pull_sample()
                # print (f'{sample} and type is {type(sample)}')
                if sample[0] == 1.0:
                    if trigger == 0:
                        trigger = 1
                        result()
                        await asyncio.sleep(1)
                        """TODO HERE IS WHERE I CAN TAKE OUT THE LSL CONNECTION AND TAKE OUT THE LOOP"""

                else:
                    trigger = 0
    except KeyboardInterrupt:
        inlet.__del__
        
            

bot.run(TOKEN)
