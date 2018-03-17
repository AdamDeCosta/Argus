from discord.ext import commands
from lib.base.load import load

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
        except Exception:
            print("Failed to load extension: {}".format(plugin))

    client.run(token)


if __name__ == "__main__":
    main()
