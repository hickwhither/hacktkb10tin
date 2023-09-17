import os
import discord
from discord import Object
from discord.ext import commands
import dotenv

env = dotenv.dotenv_values('config.env')

class MyBot(commands.Bot):

    def __init__(self):
        self.env = dotenv.dotenv_values('config.env')
        super().__init__(
            command_prefix = 'w.',
            intents = discord.Intents.all(),
            application_id = env['APPLICATION_ID'],
            
        )

    async def setup_hook(self):
        for files in os.listdir('cogs'):
            if files.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{files[:-3]}')
                    print(f'✅ Loaded {files}')
                except Exception as e:
                    print(f'❌ Error {files}: {e}')

    async def on_ready(self):
        await self.tree.sync(guild = Object(944606508644204546))
        await self.tree.sync(guild = Object(941346099011133440))
        print(f'=== Logged as {self.user} ({self.user.id}) ===')
    


bot = MyBot()
bot.run(env['BOT_TOKEN'])