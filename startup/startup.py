import re
import os
import time
import discord
from mss import mss
from discord.ext import commands

token = "NjQ3ODgyMjA4NDM4MTI0NTY0.XjGRDA.M8Rp7VhXuFAvT35oTSK_-A4sqJ4"
bot = commands.Bot(command_prefix='-')
bot.load_extension("cogs.torrents")


def inmatter(x):
    match = re.match(r"([0-9]+)([a-z]+)", x, re.I)
    items = []
    if match:
        items = match.groups()
        items = list(items)
        items[0] = int(items[0])

    if items[1] == 'd':
        items[0] = items[0] * 86400
    elif items[1] == 'h':
        items[0] = items[0] * 3600
    elif items[1] == 'm':
        items[0] = items[0] * 60
    elif items[1] == 's':
        items[0] = items[0]
    else:
        raise ValueError
    return items

bot.remove_command('help')
@bot.command(name='help')
async def help(ctx):
    await ctx.send("""
```
shutdown:
  -shutdown

screenshot:
  -screenshot

torrent:
  -torrent start
  -torrent stats [num/all]
  -torrent pause [num/all]
  -torrent resume [num/all]
    
```""")
@bot.command()
async def stats(ctx):
    await ctx.send("Bot is up")

@bot.command()
async def shutdown(ctx, date='1'):
    if ctx.author == bot.user or not(ctx.channel.name == 'diagnostics'):
        temp = await ctx.send('Wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    try:
        date = inmatter(date)
    except ValueError:
        await ctx.send("Syntax Error")
    else:
        with mss() as sct:
            sct.shot(output=r"E:\Code\Python\Discord\startup\some.png")

        await ctx.send(file=discord.File('some.png'))

        os.remove(r"E:\Code\Python\Discord\startup\some.png")
        time.sleep(5)

        os.system(f"shutdown /s /t {date}")
        await ctx.send("Shutting down")
    
@bot.command()
async def screenshot(ctx):
    if ctx.author == bot.user or not(ctx.channel.name == 'diagnostics'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    with mss() as sct:
        sct.shot(output=r"E:\Code\Python\Discord\startup\some.png")

    await ctx.send(file=discord.File('some.png'))
    os.remove(r"E:\Code\Python\Discord\startup\some.png")

bot.run(token)




