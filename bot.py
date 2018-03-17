import discord
from discord.ext import commands
from lib.load import load

import sys, traceback

_cfg = 'config.json'
_settings = load(_cfg)
_plugins = _settings['plugins']

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    

def main():
    token = _settings['token']

    for plugin in _plugins:
        try:
            client.load_extension(plugin)
        except Exception as e:
            print(f'Failed to load extension {plugin}.', file=sys.stderr)
            traceback.print_exc()

    client.run(token)


if __name__ == "__main__":
    main()
