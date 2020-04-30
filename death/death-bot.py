import re
import os
import time
import random
import base64
import asyncio
import getpass
import discord
import threading
import subprocess
import cryptography
from discord.ext import tasks
from datetime import timedelta
from discord.ext import commands
from cryptography.fernet import Fernet
from timeit import default_timer as time_func
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def alg(password):
    salt = b'876543256777777'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_256(),
        length=32,
        salt=salt,
        iterations=300000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    return f


while 1 == 1:
    global password
    data = 'gAAAAABeGdB3_srHUTbNuRbiR1W3XSMqRoV16aQ9zpCPsc1q5cOUYlh1xIWKN4taGYryQcWqHKRXkd_F_ZM_B8lsQLMypQEpR9i-tFKF8OjkFDS3LzlKYpSySbQabV1gc6ZXesNsZRNQtc74Zq1R8vcqHp7Q-OYihw=='
    passwor = getpass.getpass('Input password:')
    data = data.encode('utf-8')
    password = passwor.encode('utf-8')
    f = alg(password)
    try:
        token = (f.decrypt(data)).decode('utf-8')
    except cryptography.fernet.InvalidToken:
        print("Invalid password, try again")
        continue
    else:
        print("Password verified")
        break

bot = commands.Bot(command_prefix='.death ')
bot.is_startup = True

# on ready commands
@bot.event
async def on_ready():
    if not bot.is_startup:
        return
    time.sleep(3)
    for i in bot.get_guild(646638903503224833).text_channels:
        if i.name == 'death':
            channel = i
    print("Death Bot is online again, Sir")
    msg = "Sup bitch, just came online ya'll"
    await channel.send(msg)
    bot.timee = time_func()
    bot.failsafe = False
    bot.is_startup = False


# the main countdown
def threadings():
    while bot.x > 0:
        bot.x -= 1
        time.sleep(1)
        if bot.x == 0:
            tmonitor.cancel()
            bot.failsafe = True
            del bot.x
            os.remove('temp/freezer.txt')
            finale()
            break


# convert seconds into a string of days, hours, and minutes
def timematter(x):
    s = timedelta(seconds=x)
    if s.days < 1:
        if s.seconds <= 60*60:
            if s.seconds <= 60:
                out = f'{s.seconds}s'
            else:
                out = f'{s.seconds//60}m {s.seconds - (s.seconds//60)*60}s'
        else:
            out = f'{s.seconds//(60*60)}h {int(s.seconds/60 - (s.seconds//3600)*60)}m {s.seconds - (s.seconds//60)*60}s'
    else:
        out = f'{s.days}d {s.seconds//(60*60)}h {int(s.seconds/60 - (s.seconds//3600)*60)}m {s.seconds - (s.seconds//60)*60}s'
    return out


# converts the rewrite and extend value+string to a sepetate list
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

# freezing the countdown in case of a seizure
@tasks.loop(minutes=10, count=None)
async def freezer():
    try:
        bot.x
    except NameError:
        pass
    else:
        with open('temp/freezer.txt', 'w') as file:
            file.write(str(bot.x))


# checking if the coundown is at a certain threshold
@tasks.loop(seconds=1, count=None)
async def tmonitor():
    for i in bot.get_guild(646638903503224833).text_channels:
        if i.name == 'death':
            channel = i
    if bot.x == 259200:
        embed = discord.Embed(title="Notice", colour=discord.Colour(0xDE0405), description="**You only have three days remaining**")
        await channel.send(embed=embed)       
        await channel.send('<@534321754517143553>')

    if bot.x == 86400:
        embed = discord.Embed(title="Notice", colour=discord.Colour(0xDE0405), description="**You only have a day remaining. Consider rewriting or extending**")
        await channel.send(embed=embed)       
        await channel.send('<@534321754517143553>')
    
    if bot.x == 21600:
        embed = discord.Embed(title="Notice", colour=discord.Colour(0xDE0405), description="**You only have 6h remaining. Consider rewriting or extending**")
        await channel.send(embed=embed)       
        await channel.send('<@534321754517143553>')

    if bot.x == 1800:
        embed = discord.Embed(title="Notice", colour=discord.Colour(0xDE0405), description="**You only have 30m remaining. Consider rewriting or extending**")
        await channel.send(embed=embed)
        await channel.send('<@534321754517143553>')
    
    if bot.x == 60:
        embed = discord.Embed(title="Notice", colour=discord.Colour(0xDE0405), description="**You only have a minute remaining. Consider rewriting or extending**")
        await channel.send(embed=embed)
        await channel.send('<@534321754517143553>')
    
    if bot.x == 2:
        embed = discord.Embed(title="Notice", colour=discord.Colour(0x6B8CA6), description="**Deadline ended. Emergency Protocol activated**")
        await channel.send(embed=embed)
        await channel.send('<@534321754517143553>')


# custom help message
bot.remove_command('help')
@bot.command(name='help')
async def help(ctx):
    await ctx.send("**Fuck off mate**")


# starting the countdown
@bot.command()
async def start(ctx):
    if ctx.author == bot.user or not(ctx.channel.name == 'death'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    if bot.failsafe == False:
        try: 
            bot.x
        except NameError:
            if os.path.exists('temp/freezer.txt'):
                with open('temp/freezer.txt', 'r') as file:
                    bot.x = int(file.read())
                    await ctx.channel.send("Deadline resumed")
            else:
                bot.x = 120
                await ctx.channel.send("Deadline commenced")

            if __name__ == "__main__":
                y = threading.Thread(target=threadings)
                y.start()
            
            tmonitor.start()
            freezer.start()
        else:
            await ctx.send("A deadline is already running")
    else:
        await ctx.send("Failsafe activated")


# extending the countdown by a given amount
@bot.command()
async def extend(ctx, value):
    if ctx.author == bot.user or not(ctx.channel.name == 'death'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    if bot.failsafe == False:
        try:
            bot.x
        except NameError:
            await ctx.send("No deadlines active. Activate one before extending")
        else:
            try:
                value = inmatter(value)
            except ValueError:
                await ctx.send("Syntax Error")
            else:
                bot.x = int(bot.x + value[0])
                await ctx.send("Deadline now totals to {}" .format(timematter(bot.x)))
    
    else:
        await ctx.send("Failsafe activated")


# restarting the countdown from a given amount
@bot.command()
async def rewrite(ctx, value):
    if ctx.author == bot.user or not(ctx.channel.name == 'death'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    if bot.failsafe == False:
        try:
            bot.x
        except NameError:
            await ctx.channel.send("No deadlines active. Activate one before rewriting")
        else:
            try:
                value = inmatter(value)
            except ValueError:
                await ctx.send("Syntax Error")
            else:
                if bot.x < value[0]:
                    bot.x = value[0]
                    await ctx.channel.send("Deadline now totals to {}" .format(timematter(bot.x)))
                else:
                    await ctx.send("Sorry you can't go backwards")
    else:
        await ctx.send("Failsafe activated")


# give the stats of the bot and the countdown
@bot.command()
async def stats(ctx):
    if ctx.author == bot.user or not(ctx.channel.name == 'death'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return
    
    run_time = int(time_func() - bot.timee)
    
    try:
        embed = discord.Embed(title="Stats", colour=discord.Colour(0xe6ddbc), description="**Deadline:** active\n**Time-left:** {}\n**Run-time:** {}" .format(timematter(bot.x), timematter(run_time)))
        await ctx.send(embed=embed)
    except NameError:
        embed = discord.Embed(title="Stats", colour=discord.Colour(0xe6ddbc), description="**Deadline:** inactive\n**Time-left:** none\n**Run-time:** {}" .format(timematter(run_time)))
        await ctx.send(embed=embed)



# kills/ finishes the deadline abruptly
@bot.command()
async def suicide(ctx):
    if ctx.author == bot.user or not(ctx.channel.name == 'death'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    if bot.failsafe == False:
        await ctx.send("Are you sure? (Y/N)")

        def check(m):
            if m.content.lower() == 'n' and m.channel == ctx.channel and m.author == ctx.author:
                return True
            if m.content.lower() == 'y' and m.channel == ctx.channel and m.author == ctx.author:
                return True

        try:
            input = await bot.wait_for('message', check=check, timeout=60.0)

        except asyncio.exceptions.TimeoutError:
            ctx.send("Response timedout.")
            return

        else:
            input = input.content
            if input == 'n':
                await ctx.send("Suicide protocol disengaged")
            else:
                try:
                    bot.x
                except NameError:
                    await ctx.channel.send("Deadline terminated.")
                else:
                    bot.x = 0
                    await ctx.channel.send("Deadline terminated.")
    
    else:
        await ctx.send("Failsafe activated")


# the ending
def finale():
    # global password
    # f = alg(password)

    # with open('./temp/Ftgvb7on34tcw4t3445t4t94led5', 'w') as file:
    #     data = file.read()

    # os.remove('./temp/Ftgvb7on34tcw4t3445t4t94led5')

    # out = (f.decrypt(data)).decode('utf-8')

    # with open('./temp/finale.py') as file:
    #     file.write(out)
    
    # subprocess.call('./bash.sh')
    # os.remove('./temp/finale.py')

    # raise SystemExit
    pass





# sends an error message when arguments are missing
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Syntax error")



while True:
	try:
		bot.loop.run_until_complete(bot.run(token))
	except BaseException:
		time.sleep(5)
