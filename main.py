import os
import discord
from discord import Object
from discord.ext import commands
import dotenv

env = dotenv.dotenv_values('config.env')

with open("owners.txt","r") as f: owners_ids = list(int(i) for i in f.read().split())

class MyBot(commands.Bot):

    def __init__(self):
        self.env = dotenv.dotenv_values('config.env')
        super().__init__(
            command_prefix = env['COMMAND_PREFIX'],
            intents = discord.Intents.all(),
            application_id = env['APPLICATION_ID'],
            owner_ids = owners_ids,
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
        await self.tree.sync()
        print(f'=== Logged as {self.user} ({self.user.id}) ===')
    


bot = MyBot()
bot.run(env['BOT_TOKEN'])