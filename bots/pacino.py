from discord.ext import commands
import os

DISCORD_PACINO_TOKEN = os.getenv('DISCORD_PACINO_TOKEN')


client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('Vaidade… Definitivamente é o meu pecado favorito!')


if __name__ == '__main__':
    client.run(DISCORD_PACINO_TOKEN)
