import os
import discord
import platform
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from discord.ext import commands


def text_wrap(text, font, max_width):
    lines = []
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines

def downloadImage(imageUrl, localFileName):
    response = requests.get(imageUrl)

    # if response.status_code == 200:
    #     print('Downloading %s...' % (localFileName))

    with open(localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)



class glago(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def glag(self, ctx, text):
        await ctx.channel.send("Processing...")
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir_path)

        downloadImage(r'https://i.imgur.com/XpWe0Dp.png', 'glag.png')
        img = Image.open('glag.png')

        d = ImageDraw.Draw(img)
        # sze = img.size

        if platform == 'win32':
            glag = ImageFont.truetype(r'C:\Windows\Fonts\glag.ttf', size=60, encoding="unic")
        else: 
            glag = ImageFont.truetype(r'glag.ttf', size=60, encoding="unic")

        text = text.upper()
        lines = text_wrap(text, glag, 650)

        line_height = 65
        n = 0
        for i in lines:
            n += 1

        try:
            if n == 1:
                y = 225
            elif n == 2:
                y = 195
            elif n == 3:
                y = 175
            elif n == 4:
                y = 155
            elif n == 5:
                y = 135
            else:
                raise ValueError
        except ValueError:
            await ctx.send("Please enter a string with fewer words")
        
        else:
            x = 75
            for line in lines:
                d.text((x, y), line, fill=(207, 203, 225), font=glag)
                y = y + line_height

            img.save('some.png', optimize=True)
            await ctx.channel.send(file=discord.File('some.png'))
            os.remove('some.png')
            os.remove('glag.png')


def setup(bot):
    bot.add_cog(glago(bot))
