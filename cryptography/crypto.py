import time
import discord
import secrets
import base64
import getpass
import cryptography
from discord.ext import commands
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def alg(password):
    salt = b'876543256777777'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=300000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    return f


while 1 == 1:
    data = 'gAAAAABd7V9JaJPZqkDy_3YSb1dbJqxKE1MPP_ZIOWR1RoKVcI50EN94NMSRABOukn20zex6d4VOBaX0F4SS58CEChZbL7OCHMUkyreQJkAor24QzSXK8-Mxm9RNW202lriKe_vvTQ92pqL7JdE99FnEj89DTU4QuA=='
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


bot = commands.Bot(command_prefix='.')
bot.is_startup = True


@bot.event
async def on_ready():
    if not bot.is_startup:
        return 
    time.sleep(4)
    for i in bot.get_guild(646638903503224833).text_channels:
        if i.name == 'bot-test':
            channel = i
    bot.is_startup = False

    await channel.send("Im back to hide stuff ya cunts")
    print("Cryptography bot is online again, Sir")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f".help"))


bot.remove_command('help')
@bot.command(name='help')
async def help(ctx):
    await ctx.send("""
```Don't know how this works, then feast your eyes

fernet:
    .fernet encrypt password "plain text"
    .fernet decrypt password "cypher text"


strong primes:
    .prime send length (message)
    .prime upload length (file)

    length:
        prime bit length
        shortcuts:
            1 = 512 bits (~10m)
            2 = 1024 bits (~15m)
            3 = 2048 bits (~25m)
            4 = 4096 bits (~1h)
            default = 1024 bits
        anything else will be taken at face value.


glagolitic:
    .glag "text to be converted"  


cogs:
    .cogs load "cog_name"
    .cogs unload "cog_name"
    .cogs reload "cog_name"
    .cogs stats

    cog_names:
        prime
        fernet
        glag
        corona
```""")


bot.load_extension("cogs.prime")
bot.load_extension("cogs.fernet")
bot.load_extension("cogs.glag")


@bot.command()
async def cogs(ctx, act, extension=None):
    if act == 'load':
        try:
            bot.load_extension(f'cogs.{extension}')
        except discord.ext.commands.errors.ExtensionAlreadyLoaded:
            await ctx.send("Cog already loaded")
        except discord.ext.commands.errors.ExtensionNotFound:
            await ctx.send("Such a cog does not exist\nType `.help` to see which do")
        else:
            await ctx.send("Cog loaded")

    if act == 'unload':
        try:
            bot.unload_extension(f'cogs.{extension}')
        except discord.ext.commands.errors.ExtensionNotLoaded:
            await ctx.send("Such a cog does not exist or has not yet been loaded")
        else:
            await ctx.send("Cog unloaded")

    if act == 'reload':
        try:
            bot.unload_extension(f'cogs.{extension}')
            bot.load_extension(f'cogs.{extension}')
        except discord.ext.commands.errors.ExtensionNotFound:
            await ctx.send("Such a cog does not exist\nType `.help` to see which do")
        else:
            await ctx.send("Cog reloaded")

    if act == 'stats':
        cgs = ['prime', 'fernet', 'glag']
        stat_dict = {}
        for i in cgs:
            try:
                bot.load_extension(f'cogs.{i}')
            except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                stat_dict[i] = 'active'
            except discord.ext.commands.errors.ExtensionNotFound:
                stat_dict[i] = 'not-active'
        embed = discord.Embed(title="Stats", colour=discord.Colour(0xe6ddbc), description="**prime:** {}\n**fernet:** {}\n**glag:** {}\n" .format(
            stat_dict['prime'], stat_dict['fernet'], stat_dict['glag']))
        await ctx.send(embed=embed)


bot.run(token)
