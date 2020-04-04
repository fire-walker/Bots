import time
import random
import base64
import string
import asyncio
import discord
import getpass
import cryptography
from discord.utils import get
from discord.ext import commands
from cryptography.fernet import Fernet
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
    data = 'gAAAAABeiFciM9HmAJ_fB1HYPrskeGaHo76viamcPpSLP6vTLBTED8W6wVrga9t1Xr0I7V-lIRY3yntqMHTdfkbxPrzG7nXa7Q9onOxJ5Se_fr16r2rK3r6cVu7zEhbAmIYECxzasmpZfViIeUuYGErcWpWokb-WKA=='
    password = getpass.getpass('Input password:')
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

# custom variables
bot.is_startup = True
bot.join_kick_msg = 'You have been kicked due to verification faliure or the lack of a response.'
bot.join_fin_msg = 'Succesfully verified. You can now access the server.'
bot.join_role = 'Member'
bot.join_msg = 'This is the rule thing mate'

# the on ready event
@bot.event
async def on_ready():
    if not bot.is_startup:
        return
    print("Minerva is ready sir.")
    bot.is_startup = False
   
    
# new user verification
@bot.event
async def on_member_join(user):
    letters = string.ascii_lowercase
    join_pass = ''.join(random.choice(letters) for i in range(5))
    
    message = f"Hello, {user.nick}\n{bot.join_msg}"
    word_list = message.split(' ')
    word = random.randint(int(len(word_list)/2), len(word_list) - 2)
    word_list.insert(word, f'pass is: {join_pass}')
    message = ' '.join(word_list)
    
    await user.send(message)   

    def check(m):
        if m.content == join_pass:
            return True
    
    try:
        await bot.wait_for('message', check=check, timeout=600)
    except asyncio.exceptions.TimeoutError:
        
        await user.send(bot.join_kick_msg)
        await user.kick()
    else:
        role = get(user.guild.roles, name=bot.join_role)
        await user.add_roles(role)
        await user.send(bot.join_fin_msg)
   
  
# message purge
@bot.command()
async def purge(ctx, num):
    await ctx.channel.purge(limit=int(num) + 1)
    

# editing custom variables
@bot.command()
async def edit(ctx, variable):
    try:
        embed = discord.Embed(title=variable, colour=discord.Colour(0xeaa289), description=f"Edit as you please and reply with the final draft```{getattr(bot, variable)}```")
        await ctx.send(embed=embed)
    except AttributeError:
        await ctx.send('Syntax Error')    
    else:
        def check(m):
            if m.author == ctx.author and m.channel == ctx.channel:
                return True

        try:
            message = await bot.wait_for('message', check=check, timeout=1000)
        except asyncio.exceptions.TimeoutError:
            return
        else:
            setattr(bot, variable, message.content)
            await ctx.send('Sucessfully edited')

            
            
# bot stats
@bot.command()
async def stats(ctx):
    await ctx.send('Fuck your stats.')


bot.remove_command('help')
@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title='*Commands*', colour=discord.Colour(0xeaa289), description=f"")
    embed.add_field(name="somesome", value="somesome", inline=True)
    embed.add_field(name="some", value="thing", inline=True)
    await ctx.send(embed=embed)
    
    
    
    
while True:
    try:
        bot.loop.run_until_complete(bot.run(token))
    except BaseException:
        time.sleep(10)
