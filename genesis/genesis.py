import os
import time
import json
import base64
import asyncio
import getpass
import discord
import datetime
import cryptography
from cryptography.fernet import Fernet
from discord.ext import commands, tasks
from timeit import default_timer as time_func
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def timematter(x):
    s = datetime.timedelta(seconds=x)
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


def firstletter(name):
    nlist = []
    for i in name:
        nlist.append(i)
    nlist[0] = nlist[0].upper()
    return ''.join(nlist)


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
    data = 'gAAAAABeGc-yfAebRV4I8RYJFfVmEReaS261SY8E6cb-W1Xs__-Qypf99uOPuQgMScXPDhzKWis7jATVKRgNOtOLmonNt7TbQqzyzztk7naBBCJpoiD5bmONacrUIkYCC7kNGDRtx69duyf98nnxVGipZ0M2C697Jw=='
    password = getpass.getpass('Input password: ')
    data = data.encode('utf-8')
    password = password.encode('utf-8')
    f = alg(password)
    try:
        token = (f.decrypt(data)).decode('utf-8')
    except cryptography.fernet.InvalidToken:
        print("Invalid password, try again")
        continue
    else:
        print("Password verified")
        break


bot = commands.Bot(command_prefix='.genesis ')
bot.is_startup = True

@bot.event
async def on_ready():
    if not bot.is_startup:
        return
    time.sleep(3)
    for i in bot.get_guild(646638903503224833).text_channels:
        if i.name == 'genesis':
            channel = i
    check.start()
    await channel.send("I'm up to blow some candles mate")
    print("Genesis is online again, Sir")
    bot.timee = time_func()
    bot.is_startup = False
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f".genesis help"))


@tasks.loop(hours=24, count=None)
async def check():
    for i in bot.get_guild(646638903503224833).text_channels:
        if i.name == 'genesis':
            channel = i
    nlthing = []


    with open('jthing.json', 'r') as file:
        dthing = json.load(file)


    if int(time.strftime('%d')) == 1:
        for i, j in dthing.items():
            if j[0] == int(time.strftime('%m')):
                nlthing.append(firstletter(i))

        out = '\n'.join(nlthing)
        embed = discord.Embed(title=f"Birthdays is this month", description=out, colour=discord.Colour(0xc64170))
        await channel.send(embed=embed)
        del nlthing
    
    if datetime.date.today().isoweekday() == 7:
        for i, j in dthing.items():
            if j[1] in range(int(time.strftime('%d')) + 1, int(time.strftime('%d')) + 8) and j[0] == int(time.strftime('%m')):
                date = datetime.datetime(datetime.date.today().year, j[0], j[1]).strftime('%A')
                nlthing.append(f"{firstletter(i)}'s birthday is next {date}")
                

        try:
            nlthing
        except NameError:
            pass
        else:
            if nlthing == '':
                pass
            else:
                out = '\n'.join(nlthing)
                embed = discord.Embed(title=f"Birthdays this week", description=out , colour=discord.Colour(0xc64170))
                await channel.send(embed=embed)
                del nlthing, dthing

    for i,j in dthing.items():
        if j[1] == int(time.strftime('%d')) + 1 and j[0] == int(time.strftime('%m')):
            await channel.send('<@534321754517143553>')
            embed = discord.Embed(title=f"{firstletter(i)}'s birthday is tomarrow", colour=discord.Colour(0xc64170))
            await channel.send(embed=embed)



bot.remove_command('help')
@bot.command(name='help')
async def help(ctx):
    await ctx.send("""
```
Okay, let's see what we've got here now.


add:
    .origin add 'name' 'mm/dd'

delete:
    .origin remove 'name'
    
stats:
    .origin stats
    
records:
    .origin records

edit:
    .origin edit 'name'
    
```""")




@bot.command()
async def add(ctx, name, date):
    if ctx.author == bot.user or not(ctx.channel.name == 'genesis'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    check.cancel()
    lthing = []
    dthing = {}
    if os.path.exists('jthing.json'):
        with open('jthing.json', 'r') as file:
            dthing = json.load(file)

    temp_date = date.split('/')

    for i in temp_date:
        i = int(i)
        lthing.append(i)

    dthing[name.lower()] = lthing

    with open('jthing.json', 'w') as file:
        json.dump(dthing, file)
        await ctx.send("Record added")
    check.start()


@bot.command()
async def remove(ctx, name):
    if ctx.author == bot.user or not(ctx.channel.name == 'genesis'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    with open('jthing.json', 'r') as file:
        dthing = json.load(file)   

    try:
        del dthing[name.lower()]

    except KeyError:
        await ctx.send("No such record exists. Please try again")

    else:
        await ctx.send('Record deleted')

        with open('jthing.json', 'w') as file:
            json.dump(dthing, file)


@bot.command()
async def edit(ctx, name):
    if ctx.author == bot.user or not(ctx.channel.name == 'genesis'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    with open('jthing.json', 'r') as file:
        dthing = json.load(file)

    try:
        dthing[name]

    except KeyError:
        await ctx.send("Such a record does not exist")
    
    else:
        await ctx.send("What do you want to change? (name/date)")
        def check(m):
            if m.content.lower() == 'name' and m.channel == ctx.channel and m.author == ctx.author:
                return True
            if m.content.lower() == 'date' and m.channel == ctx.channel and m.author == ctx.author:
                return True

        try:
            enter = await bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.exceptions.TimeoutError:
            await ctx.send("Response timedout.")
            return
        else:
            enter = enter.content.lower()

            if enter == 'name':
                await ctx.send("To what do you want to change the name to?")
                def check2(m):
                    if m.channel == ctx.channel and m.author == ctx.author:
                        return True
                
                try:
                    enter = await bot.wait_for('message', check=check2, timeout=60.0)
                except asyncio.exceptions.TimeoutError:
                    await ctx.send("Response timedout.")
                    return
                else:
                    enter = enter.content.lower()
                    dthing[enter] = dthing.pop(name)
                    await ctx.send(f"Name successfully changed from {name} to {enter}")
            
            if enter == 'date':
                await ctx.send("Which one? (m/d)")
                def check3(m):
                    if m.channel == ctx.channel and m.author == ctx.author:
                        return True
                try:
                    enter = await bot.wait_for('message', check=check3, timeout=60.0)
                except asyncio.exceptions.TimeoutError:
                    await ctx.send("Response timedout.")
                    return
                else:
                    enter = enter.content.lower()

                    if enter == 'd':
                        await ctx.send("To which day?")
                        def check4(m):
                            if m.channel == ctx.channel and m.author == ctx.author:
                                return True
                        try:
                            enter = await bot.wait_for('message', check=check4, timeout=60.0)
                        except asyncio.exceptions.TimeoutError:
                            await ctx.send("Response timedout.")
                            return
                        else:
                            enter = int(enter.content)
                            old = dthing[name][1]
                            dthing[name][1] = int(enter)
                            await ctx.send(f'Day successfully changed from {old} to {enter}')
                    
                    if enter == 'm':
                        await ctx.send("To which month?")
                        def check5(m):
                            if m.channel == ctx.channel and m.author == ctx.author:
                                return True
                        try:
                            enter = await bot.wait_for('message', check=check5, timeout=60.0)
                        except asyncio.exceptions.TimeoutError:
                            await ctx.send("Response timedout.")
                            return
                        else:
                            enter = int(enter.content)
                            old = dthing[name][0]
                            dthing[name][0] = int(enter)
                            await ctx.send(f'Month successfully changed from {old} to {enter}')
                    
        with open('jthing.json', 'w') as file:
            json.dump(dthing, file)



@bot.command()
async def stats(ctx):
    if ctx.author == bot.user or not(ctx.channel.name == 'genesis'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    with open('jthing.json', 'r') as file:
        dthing = json.load(file)

    x = len(dthing.keys())

    run_time = int(time_func() - bot.timee)
    last = list(dthing.items())[-1][0]
    
    embed = discord.Embed(title="Stats", colour=discord.Colour(0xc64170), description=f"**Total-entries:** {x}\n**Last-added:** {firstletter(last)}\n**Run-time:** {timematter(run_time)}")
    await ctx.send(embed=embed)


@bot.command()
async def records(ctx):
    if ctx.author == bot.user or not(ctx.channel.name == 'genesis'):
        temp = await ctx.send('wrong channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return

    with open('jthing.json', 'r') as file:
        dthing = json.load(file)

    names = []
    x = 0

    for i, j in dthing.items():
        x += 1
        dates = []
        for n in j:
            dates.append(str(n))
        j = '/'.join(dates)
        i = f'{firstletter(i)}  :  {j}'
        names.append(i)

    names = '\n'.join(sorted(names))

    embed = discord.Embed(title="Records", colour=discord.Colour(0xc64170), description=names)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        for i in bot.get_guild(646638903503224833).text_channels:
            if i.name == 'genesis':
                channel = i
        await channel.send("Syntax error")

while True:
	try:
		bot.loop.run_until_complete(bot.run(token))
	except BaseException:
		time.sleep(5)
