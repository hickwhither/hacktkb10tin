import discord
from discord import Embed
from discord.ext import commands
import os

async def setup(bot) -> None:
    await bot.add_cog(Developer(bot))

class Developer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.command(aliases = ['rl','yell'])
    # @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, exts: str = ''):
        # async with ctx... dài hơn
        await ctx.typing()
        content = ''
        exts = exts.split(' ')
        no_extension = exts == ['']
        extensions = {}
        for file in os.listdir('./cogs') if no_extension else exts:
            if file.endswith('.py') or not no_extension:
                if no_extension:
                    file = file[:-3]
                try:
                    await self.bot.unload_extension(f'cogs.{file}')
                    await self.bot.load_extension(f'cogs.{file}')
                except discord.ext.commands.errors.ExtensionNotLoaded: # Chua load extension
                    extensions[file] = None
                    try:
                        await self.bot.load_extension(f'cogs.{file}')
                    except Exception as e:
                        extensions[file] = e
                except Exception as e: 
                    extensions[file] = e
                else: # Ko loi
                    extensions[file] = None

        for file, error in extensions.items():
                if error:
                    content += f'\❌ `{file}.py`: **{error}**\n'
                else:
                    content += f'\✅ `{file}.py`\n'

        await ctx.reply(content)
    

    
