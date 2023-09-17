import discord
from discord import Embed
from discord.ext import commands
import os

async def setup(bot) -> None:
    await bot.add_cog(Handle(bot))

class Handle(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CommandNotFound): await ctx.reply("Command ko co:("); return
        if isinstance(error, commands.errors.NSFWChannelRequired): await ctx.reply("NSFW channel 🔞"); return
        if isinstance(error, commands.errors.CommandOnCooldown): await ctx.reply("Command cham thoi!"); return
        await ctx.reply(embed=Embed(
            title = "Exception",
            description=error
        ))
    

    
