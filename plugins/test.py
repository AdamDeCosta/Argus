from discord.ext import commands


class TestPlugin:
    def __init__(self, client):
        self.client = client

    @commands.command(name='ping')
    async def ping(self):
        await self.client.say('Pong!')


def setup(client):
    client.add_cog(TestPlugin(client))