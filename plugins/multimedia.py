import discord
from discord.ext import commands
from lib.load import load_plugin_cfg
from lib.spotify import get_auth
import aiohttp
import json


class Multimedia:
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()

    async def on_ready(self):
        self.settings = load_plugin_cfg(self)

        self.yt_key = self.settings['youtube-key']
        self.sp_key = self.settings['spotify-secret']

        sp_token = await get_auth(self)

        self.sp_header = {'content-type': 'application/json',
                          'accept': 'application/json',
                          'Authorization': 'Bearer {0}'.format(sp_token)}

    @commands.command(name="yt")
    async def youtube(self, *args):
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
        result = resp['items'][0]
        url = 'https://youtu.be/{0}'.format(result['id']['videoId'])
        await self.client.say(url)

    @commands.command(name='sp')
    async def spotify(self, *args):
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
        print(resp)
        if len(resp['artists']['items']) > 0:
            result = resp['artists']['items'][0]['external_urls']['spotify']
        else:
            result = resp['tracks']['items'][0]['external_urls']['spotify']
        await self.client.say(result)


def setup(client):
    client.add_cog(Multimedia(client))
