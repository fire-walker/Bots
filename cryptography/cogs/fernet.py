import discord
import base64
import cryptography
from discord.ext import commands
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
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

class fernet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='.fernet encrypt/decrypt password "string to be encrypted"')
    async def fernet(self, ctx, method, pwd, data):

        if method == 'encrypt':
            await ctx.message.delete()
            temp = await ctx.channel.send("Processing.....")
            password = pwd.encode('utf-8')

            f = alg(password)
            encrypted = f.encrypt(str.encode(data))
            encrypted = encrypted.decode('utf-8')
            await temp.delete()

            embed = discord.Embed(title="Encrypted", colour=discord.Colour(0x41bbc6), description="This will delete in 30s ```\n{}```" .format(encrypted))
            temp2 = await ctx.send(embed=embed)

            await temp2.delete(delay=30)
        

        elif method == 'decrypt':
            data = data.encode('utf-8')
            password = pwd.encode('utf-8')

            f = alg(password)
            try:
                decrypted = (f.decrypt(data)).decode('utf-8')

            except cryptography.fernet.InvalidToken:
                await ctx.channel.send("Password or cypher text incorrect")

            else:
                await ctx.message.delete()
                embed = discord.Embed(title="Decrypted", colour=discord.Colour(0xc64170), description="This will delete in 30s ```\n{}```" .format(decrypted))
                temp2 = await ctx.send(embed=embed)

                await temp2.delete(delay=30)

        else:
            await ctx.send("Wrong syntax: `{}` is not a recognized intake" .format(method))


def setup(bot):
    bot.add_cog(fernet(bot))
