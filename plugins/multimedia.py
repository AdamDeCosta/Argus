from discord.ext import commands
from lib.base.config import Config
from lib.multimedia.spotify import *
import aiohttp
import json


class Multimedia(Config):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.session = aiohttp.ClientSession()

    async def on_ready(self):
        self.yt_key = self.settings['youtube-key']
        self.sp_key = self.settings['spotify-secret']

        sp_token = await get_auth(self)

        self.sp_header = {'content-type': 'application/json',
                          'accept': 'application/json',
                          'Authorization': 'Bearer {0}'.format(sp_token)}

    @commands.command(name="yt", pass_context = True)
    async def youtube(self, ctx, *args):
        """
        Searches youtube for a video matching inputted string
        :parameter args: string to input
        """
        key = ' '.join(args)
        payload = {
            'key': self.yt_key,
            'type': 'video',
            'q': key,
            'maxResults': 1,
            'part': 'snippet'
        }
        r = await self.session.request('GET',
                                       "https://www.googleapis.com/youtube/v3/search",
                                       params=payload)
        resp = await r.text()
        resp = json.loads(resp)
        try:
            result = resp['items'][0]
        except IndexError:
            mention = ctx.message.author.mention
            await self.client.say("{}: No results found".format(mention))
        else:
            url = 'https://youtu.be/{0}'.format(result['id']['videoId'])
            await self.client.say(url)

    @commands.command(name='sp', pass_context=True)
    async def spotify(self,ctx, *args):
        """
        Get track or artist from spotify search
        :param args: string to search
        """
        key = ' '.join(args)

        payload = {'q': key,
                   'type': 'track,artist',
                   'limit': 1}
        r = await self.session.request('GET',
                                       "https://api.spotify.com/v1/search",
                                       headers=self.sp_header,
                                       params=payload)
        resp = await r.text()
        resp = json.loads(resp)
        if len(resp['artists']['items']) > 0:
            result = resp['artists']['items'][0]['external_urls']['spotify']
        else:
            try:
                result = resp['tracks']['items'][0]['external_urls']['spotify']
            except IndexError:
                mention = ctx.message.author.mention
                result = "{} No results found".format(mention)

        await self.client.say(result)


def setup(client):
    client.add_cog(Multimedia(client))
