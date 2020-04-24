import os
import json
import time
import base64
import random
import shutil
import getpass
import discord
import requests
import selenium
import cryptography
import urllib.request
from discord.ext import tasks
from selenium import webdriver
from datetime import timedelta
from discord.ext import commands
from time import gmtime, strftime
from cryptography.fernet import Fernet
from timeit import default_timer as time_func
from selenium.webdriver.common.keys import Keys
from cryptography.hazmat.primitives import hashes
from selenium.webdriver.chrome.options import Options
from cryptography.hazmat.backends import default_backend
from selenium.webdriver.common.action_chains import ActionChains
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


while 1==1:
    data = 'gAAAAABec6cUkWTFCmPj-7F1GFI8lPhyxTVOt-muPHCk6fJMcVSOQAiHBpBilk6GjBHOcJh2dd1wlWwiPfMey2MCqxlF7ameoyD3nVkNJbDoYfx-__RXMLZRTZafdYgKvuo6MXW38R_M0jh0dkHG59c3ppp-DnQTJQ=='
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
bot.is_startup = True


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


# send watchdog posts to discord
@tasks.loop(minutes=20, count=None)
async def checker():
    for i in bot.get_guild(646638903503224833).text_channels:
        if i.name == 'watchdog':
            channel = i

    bot.req_num += 1
    url = f'https://watchdogapi.paladinanalytics.com/public/post/{bot.post_num}'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    request = urllib.request.Request(url, headers={'User-Agent': user_agent})

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError:
        pass
    else:
        html = response.read()
        my_json = html.decode('utf8')
        data = json.loads(my_json)

        title = data['body']['en_title']
        description = data['body']['en_description']
        source = data['body']['source_name']
        url = f'https://watchdog.paladinanalytics.com/post?id={bot.post_num}'

        embed = discord.Embed(title=title, url=url, colour=discord.Colour(0x1DBF98), description=description)
        embed.set_author(name=source, icon_url="https://watchdog.paladinanalytics.com/site_image.png")
        embed.set_footer(text="Watchdog")
        await channel.send(embed=embed)

        bot.post_num += 1


# grab the data from roar
@tasks.loop(minutes=1, count=None)
async def roar_checker():
    if strftime('%H:%M', gmtime()) == '18:30':
        for i in bot.get_guild(646638903503224833).text_channels:
            if i.name == 'corona':
                channel = i

        options = Options()
        options.headless = True
        driver_loc = r'./chromedriver'
        driver = webdriver.Chrome(options=options, executable_path=driver_loc, port=3544)
        driver.get('https://roar.media/english/life/reports/live-updates-coronavirus-outbreak')

        time.sleep(20)
        image = driver.find_element_by_xpath('/html/body/div/div[1]/div[3]/div/div[4]/div[1]/div[3]/div[1]/p[2]/div').get_attribute('src')
        driver.quit()

        r = requests.get(image, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        
        
        with open("temp_roar.jpg", 'wb') as file:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, file)
            
        with open('./temp_roar.jpg', 'rb') as file:
            await channel.send(file=discord.File(file, 'roar.jpg'))
            
        os.remove('./temp_roar.jpg')
            
        
        
    


# the on ready event
@bot.event
async def on_ready():
    if not bot.is_startup:
        return
    time.sleep(4)
    for i in bot.get_guild(646638903503224833).text_channels:
        if i.name == 'watchdog':
            channel = i
    print("Watchdog is online again, Sir")
    await channel.send("Feed me that news motherfucker")
    bot.timee = time_func()
    bot.post_num = 3640
    bot.req_num = 0
    checker.start()
    roar_checker.start()
    bot.is_startup = False


# respond to a .stats call
@bot.command()
async def stats(ctx):
    if ctx.author == bot.user or not(ctx.channel.name == 'watchdog'):
        temp = await ctx.send('Wrong Channel')
        await temp.delete(delay=5)
        await ctx.message.delete(delay=5)
        return
    
    run_time = int(time_func() - bot.timee)
    
    embed = discord.Embed(title="Stats", colour=discord.Colour(0x1DBF98), description="**Run-time:** {}\n**Req_num:** {}" .format(timematter(run_time), bot.req_num))
    stat = await ctx.send(embed=embed)
    await stat.delete(delay=20)
    await ctx.delete(delay=20)


# catch syntax errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        for i in bot.get_guild(646638903503224833).text_channels:
            if i.name == 'watchdog':
                channel = i
        await channel.send("Syntax error")


while True:
    try:
	    bot.loop.run_until_complete(bot.run(token))
    except BaseException:
	    time.sleep(5)
