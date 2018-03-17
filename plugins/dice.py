import discord
from discord.ext import commands
import random
import re
import asyncio


async def _range(numbers):
    for i in range(numbers):
        yield i


async def _iterate_list(list):
    for i in list:
        yield i


class Dice:
    reg = "[0-9]+[dD][0-9]+$"

    def __init__(self, client):
        self.client = client

    @commands.command(name='roll', pass_context=True)
    async def roll(self, ctx, roll):
        random.seed(None)
        valid = re.match(self.reg, roll)
        sender = ctx.message.author.mention

        if valid:
            roll = roll.split('d')
            num_dice = int(roll[0])
            num_sides = int(roll[1])

            if num_dice > 100:
                await self.client.say("Error: Maximum number of dice: 100")
            elif num_sides > 10000:
                await self.client.say("Error: Maximum number of sides: 10000")
            else:
                total = 0
                rolls = [random.randint(1, num_sides) async for
                         i in _range(num_dice)]

                async for i in _iterate_list(rolls):
                    total += i
                payload = '+'.join(map(str, rolls))

                await self.client.say("{0}: `{1}` = {2}".format(sender, payload, total))
        else:
            await self.client.say("Error: Invalid input!")


def setup(client):
    client.add_cog(Dice(client))
