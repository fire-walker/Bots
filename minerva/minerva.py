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
bot.join_kick_msg = 'You have been kicked due to verification failure or the lack of a response.'
bot.join_fin_msg = 'Successfully verified. You can now access the server.'
bot.join_role = 'Member'
bot.join_msg = 'This is the rule thing mate'
bot.join_time_lim = 20
bot.user_verification = False

# the on ready event
@bot.event
async def on_ready():
    if not bot.is_startup:
        return
    print("Minerva is ready sir.")
    bot.is_startup = False
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f".help"))
   
    
# new user verification
@bot.event
async def on_member_join(user):
    if bot.user_verification == False:
        return
    letters = string.ascii_lowercase
    join_pass = ''.join(random.choice(letters) for i in range(5))
    
    word_list = bot.join_msg.split(' ')
    word = random.randint(int(len(word_list)/2), len(word_list) - 2)
    word_list.insert(word, f'pass is: {join_pass}')
    
    head = f"Hello, {user.name}"
    message = ' '.join(word_list)
    
    embed = discord.Embed(title=head, colour=discord.Colour(0xeaa289), description=message)
    await user.send(embed=embed)   

    def check(m):
        if m.content == join_pass:
            return True
    
    try:
        await bot.wait_for('message', check=check, timeout=bot.join_time_lim*60 )
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
        embed = discord.Embed(title=variable, colour=discord.Colour(0xeaa289), description="Please send the new variable you wish to replace the one stated below")
        embed.add_field(name="Variable value", value=f"```{getattr(bot, variable)}```")
        await ctx.send(embed=embed)
    except AttributeError:
        return
    else:
        def check(m):
            if m.author == ctx.author and m.channel == ctx.channel:
                return True

        try:
            message = await bot.wait_for('message', check=check, timeout=120)
        except asyncio.exceptions.TimeoutError:
            await ctx.send("Feedback time limit reached. Please try again, or don't")
        else:
            setattr(bot, variable, message.content)
            await ctx.send('Sucessfully edited')

            
            
# bot stats
@bot.command()
async def stats(ctx):
    await ctx.send('Fuck your stats.')
    
# user join verification
@bot.command(name='user-verification')
async def verif(ctx, bool):
    if bool.lower() == 'activate':
        if bot.user_verification == True:
            await ctx.send('User verification was already active.')
        else:
            bot.user_verification = True
            await ctx.send('User verification successfully activated.')
            
    elif bool.lower() == 'deactivate':
        if bot.user_verification == False:
            await ctx.send('User verification was already not in function.')
        else:
            bot.user_verification = False
            await ctx.send('User verification deactivated')
    
    else:
        raise AttributeError
        
# checking the currently set custom variables
@bot.command()
async def check(ctx, variable):
    embed = discord.Embed(title=variable, colour=discord.Colour(0xeaa289))
    embed.add_field(name="Variable value", value=f"```{getattr(bot, variable)}```")
    await ctx.send(embed=embed)


bot.remove_command('help')
@bot.command(name='help')
async def help(ctx, var=None):
    if var == None:
        embed = discord.Embed(title='FUNCTION LIST', colour=discord.Colour(0xeaa289), description=f"```The current prefix is '.'\nType 'help <function/variable>' to get more info about variables or commands```")
        embed.add_field(name="Variables", value="```\njoin_kick_msg\njoin_fin_msg\njoin_role\njoin_msg\njoin_time_lim```")
        embed.add_field(name="Commands", value="```purge (num)\nedit (variable)\ncheck (variable)\nuser-verification (de/activate)\n```")
        await ctx.send(embed=embed)
        
    elif var == 'join_kick_msg':
        embed = discord.Embed(title='**join_kick_msg**', colour=discord.Colour(0xeaa289), description=f"This variable is the message sent through DM when a new user fails or takes too much time to complete the server entrance verification within the given time limit, which is attributed to the variable `join_time_lim`.")   
        embed.add_field(name="Usage example", value="```edit join_kick_msg <message>```", inline=False)
        await ctx.send(embed=embed)
    
    elif var == 'join_fin_msg':
        embed = discord.Embed(title='**join_fin_msg**', colour=discord.Colour(0xeaa289), description=f"This variable is the message sent through DM when a new user successfully completes the server entrance verification.")   
        embed.add_field(name="Usage example", value="```edit join_fin_msg <message>```", inline=False)
        await ctx.send(embed=embed)

    elif var == 'join_role':
        embed = discord.Embed(title='**join_role**', colour=discord.Colour(0xeaa289), description=f"This variable is the role given to a new user who just finished server entrance verification. In usage please be mindful of role letter case.")   
        embed.add_field(name="Usage example", value="```edit join_role <role>```", inline=False)   
        await ctx.send(embed=embed)
        
    elif var == 'join_msg':
        embed = discord.Embed(title='**join_msg**', colour=discord.Colour(0xeaa289), description=f"This variable is the message sent when a user newly joins the server. This is the message the verification password is hidden. Most usually this message is made up of a rule set.")   
        embed.add_field(name="Usage example", value="```edit join_msg <msg>```", inline=False)   
        await ctx.send(embed=embed)
    
    elif var == 'join_time_lim':
        embed = discord.Embed(title='**join_time_lim**', colour=discord.Colour(0xeaa289), description=f"This variable is the given for a user to complete the server entrance verification")   
        embed.add_field(name="Usage example", value="```edit join_time_lim <mins>```", inline=False)   
        await ctx.send(embed=embed)
        
    elif var == 'purge':
        embed = discord.Embed(title='**purge**', colour=discord.Colour(0xeaa289), description=f"This command purges messages as per the number you supply")   
        embed.add_field(name="Usage example", value="```purge <number>```", inline=False)   
        await ctx.send(embed=embed)
    
    elif var == 'edit':
        embed = discord.Embed(title='**edit**', colour=discord.Colour(0xeaa289), description=f"This command is used to edit the custom variables that appear on the command `help`.")   
        embed.add_field(name="Usage example", value="```edit <variable>```", inline=False)   
        await ctx.send(embed=embed)

    elif var == 'check':
        embed = discord.Embed(title='**check**', colour=discord.Colour(0xeaa289), description=f"This command is used to check or view the current value of a variable.")   
        embed.add_field(name="Usage example", value="```check <variable>```", inline=False)   
        await ctx.send(embed=embed)
        
    elif var == 'user-verification':
        embed = discord.Embed(title='**edit**', colour=discord.Colour(0xeaa289), description=f"This command activates or deactivates the new user verification option. Activating this requires you to pre set the variables beginning with `join_`.")   
        embed.add_field(name="Usage example", value="```user-verification <activate/deactivate>```", inline=False)   
        await ctx.send(embed=embed)
    
    else:
        raise AttributeError
    
    

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing Arguments")
        return
        
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Syntax Error")
        return

    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found')
        return
    
    raise error
        
    
while True:
    try:
        bot.loop.run_until_complete(bot.run(token))
    except BaseException:
        time.sleep(10)
