import discord
from discord.ext import commands
import aiohttp


class Inspire():
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()

    @commands.command(name='inspire')
    async def inspire(self):
        """
        Sends an inspirational quote from Inspirobot.
        """
        r = await self.session.get('http://inspirobot.me/api?generate=true')
        img = await r.text()
        embed = discord.Embed(color=0x9b59b6)
        embed.set_image(url=img)
        await self.client.say(embed=embed)


def setup(client):
    client.add_cog(Inspire(client))
