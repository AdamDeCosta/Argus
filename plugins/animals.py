import discord
from discord.ext import commands
import aiohttp
import json


class Animals:

    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()

    @commands.command(name='rd', pass_context=True)
    async def random_dog(self, ctx, *args):
        """
        gets a random dog image from dog.ceo
        :param args: breed of dog
        """
        mention = ctx.message.author.mention
        args = args or {}

        if len(args) == 1:
            url = "https://dog.ceo/api/breed/{0}/images/random".format(args[0])
        elif len(args) == 2:
            url = "https://dog.ceo/api/breed/{0}/{1}/images/random".format(
                args[1], args[0])
        else:
            url = "https://dog.ceo/api/breeds/image/random"

        r = await self.session.get(url)
        resp = await r.text()

        if resp == "Not found":
            await self.client.say("{0} Error: No image found!".format(mention))
            return
        else:
            resp = json.loads(resp)

        if resp['status'] != "success":
            await self.client.say("{0} Error: {1}"
                                  .format(mention, resp['message']))

        else:
            try:
                img = resp['message']
            except Exception as e:
                await self.client.say("{0} Error: Something went wrong!"
                                      .format(mention))
                print(e)
            else:
                embed = discord.Embed()
                embed.set_image(url=img)

                await self.client.say(embed=embed)


def setup(client):
    client.add_cog(Animals(client))

