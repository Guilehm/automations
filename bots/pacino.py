import os

import discord

DISCORD_PACINO_TOKEN = os.getenv('DISCORD_PACINO_TOKEN')


class Pacino(discord.Client):
    MAIN_QUOTE = 'Vaidade… Definitivamente é o meu pecado favorito!'

    async def on_ready(self):
        print(self.MAIN_QUOTE)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('.ping'):
            await message.channel.send(self.MAIN_QUOTE)


pacino = Pacino()

if __name__ == '__main__':
    pacino = Pacino()
    pacino.run(DISCORD_PACINO_TOKEN)
