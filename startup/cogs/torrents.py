import os
import psutil
import discord
import qbittorrentapi
from discord.ext import commands


class arrrg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def torrent(self, ctx, action, var1='all'):
        if action == 'start':
            def check():
                return "qbittorrent.exe" in (p.name() for p in psutil.process_iter())
            if check() == False:
                os.startfile(r'D:\Program files\qBittorrent\qbittorrent.exe')
            await ctx.send("Qbittorrent started up")
            global qbt_client
            qbt_client = qbittorrentapi.Client(host='localhost:6060', username='admin', password='12345678')
        
        if action == 'stats':
            try:
                qbt_client
            except NameError:
                await ctx.send("Qbittorrent is not active.")
            
            else: 
                # printing out all torrent names with a reference numeral used to get further info from the next command
                if var1 == 'all':
                    torrent_dict = {}
                    torrent_list = []

                    # making a dict in the form {**1**:torrent-name} into torrent_dict
                    x = 0
                    for torrent in qbt_client.torrents.info():
                        x += 1
                        torrent_dict[str(f'**{x}**')] = torrent.name

                    # making a list in the form ["**1** : torrent1", "**2** : torrent2"] into torret_list
                    for i in torrent_dict.items():
                        torrent_list.append(' : '.join(i))

                    # joining all the formatted list items into one printable element with linebreaks
                    out = '\n'.join(torrent_list)
                    embed = discord.Embed(title="Stats", colour=discord.Colour(0xe6ddbc), description="{}" .format(out))
                    await ctx.send(embed=embed)
                else:
                    # printing out torrent info for specific numerals which can be obtained from the above command
                    num = int(var1)
                    x = 0
                    for torrent in qbt_client.torrents.info():
                        x +=1
                        if x == num:
                            out = f"{torrent.name} : {torrent.progress*100}% : {torrent.state} : {torrent.eta}s"
                            embed = discord.Embed(title="Stats", colour=discord.Colour(0xe6ddbc), description="{}" .format(out))
                            await ctx.send(embed=embed)


        # if action == 'add':
        #     try:
        #         qbt_client
        #     except NameError:
        #         await ctx.send("Please start Qbittorrent before issuing orders, you maniac")
        #     else:
        #         qbt_client.torrents_add(url=var1, save_path=r'D:\Downloads\Torrents')


        
        if action == 'pause':
            try:
                qbt_client
            except NameError:
                await ctx.send("Qbittorrent is not active.")
            else:
                if var1 == 'all':
                    qbt_client.torrents.pause.all()
                    await ctx.send("All torrents paused")
                else:
                    num = int(var1)
                    x = 0
                    for torrent in qbt_client.torrents.info():
                        x +=1
                        if x == num:
                            torrent.pause()
        
        if action == 'resume':
            try:
                qbt_client
            except NameError:
                await ctx.send("Qbittorrent is not active.")
            else:
                if var1 == 'all':
                    qbt_client.torrents.resume.all()
                    await ctx.send("All torrents resumed")
                else:
                    num = int(var1)
                    x = 0
                    for torrent in qbt_client.torrents.info():
                        x += 1
                        if x == num:
                            torrent.resume()

                    

        


def setup(bot):
    bot.add_cog(arrrg(bot))
