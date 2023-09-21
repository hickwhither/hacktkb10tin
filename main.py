import os
import discord
from discord import Object, Embed
from discord.ext import commands
from discord.ext.commands import Context

import dotenv
import time

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

    async def on_command(self, ctx: Context):
        if ctx.author.bot: return
        self.usecount += 1

    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.CommandNotFound): await ctx.reply("Command ko co:("); return
        if isinstance(error, commands.errors.NSFWChannelRequired): await ctx.reply("NSFW channel 🔞"); return
        if isinstance(error, commands.errors.CommandOnCooldown): await ctx.reply("Command cham thoi!"); return
        await ctx.reply(embed=Embed(
            title = "Exception",
            description=error
        ), mention_author = False)

    async def on_ready(self):
        self.uptime = f'<t:{int(time.time())}:R>'
        self.usecount = 0
        await self.tree.sync()
        await bot.change_presence(activity=discord.Game(name=env['COMMAND_PREFIX']))
        print(f'=== Logged as {self.user} ({self.user.id}) ===')
    
    


bot = MyBot()
bot.run(env['BOT_TOKEN'])