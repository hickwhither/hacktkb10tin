import discord
from discord import Embed
from discord.ext import commands
import aiohttp
import json

async def setup(bot) -> None:
    await bot.add_cog(api(bot))

class api(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        self.bot.http.token

    #ham api dep trai
    @staticmethod
    async def _request(url : str, **kwrags):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, **kwrags) as resp:
                return await resp.json()

    @commands.is_nsfw()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = 'randomorz')
    async def randomorz(self, ctx:commands.Context):

        COUNDNT_FOUND_RESULT = 'https://images-ext-1.discordapp.net/external/AUKM52nm37_7bqv0souTdSHEkCaDHeVft8bAITfLFpE/https/cdn.discordapp.com/emojis/941346145022672946.png'

        params = {
            'api_key': 'rfk9wx4ZQkcmPnU1fhZru11h',
            'login': 'iuuahct'
        }
        resp = await self._request('https://danbooru.donmai.us/posts/random.json',params=params)
        

        await ctx.reply(
            embed=Embed().set_image(
                url=resp.get('large_file_url', COUNDNT_FOUND_RESULT)
            )
        )


    # @commands.command(name = '8ball')
    # async def _8ball(self, ctx: commands.Context, *, ques: str):
    #     await ctx.typing()
    #     json = await self._request(f'https://8ball.delegator.com/magic/json/{ques}')
    #     await ctx.reply(embed = Embed(
    #         colour = discord.Colour.random(),
    #         title = '🎱 8ball',
    #         description = json['magic']['answer'] + ' ' + ctx.author.mention
    #     ),mention_author = False)
    
    # @commands.command()
    # async def cov(self, ctx: commands.Context,*, country = None):
    #     await ctx.typing()
    #     if country is None:
    #         country = 'World'
    #     try:
    #         json = await self._request(f'https://coronavirus-19-api.herokuapp.com/countries/{country}')
    #     except Exception as e:
    #         embed = Embed(
    #             title = 'Có một lỗi nào đó 😔',
    #             description = 'Có lẽ quốc gia bạn nhập không có thống kê hoặc đập troai',
    #             color = 0x43AAEB
    #         ).set_footer(
    #             text = e
    #         )
    #     else:
    #         embed = Embed(
    #             title = f'Cập nhật tình hình Covid-19 trên thế giới 🌏',
    #             url = f'https://coronavirus-19-api.herokuapp.com/countries/{country}',
    #             color = 0x43AAEB
    #         ).add_field(
    #             name = '☢ Tổng ca mắc',
    #             value = f"{json['cases']:,}",
    #         ).add_field(
    #             name = '☢ Số ca mắc hôm nay ⛅',
    #             value = f"{json['todayCases']:,}"
    #         ).add_field(
    #             name = '💀 Tử vong',
    #             value = f"{json['deaths']:,}",
    #             inline = False
    #         ).add_field(
    #             name = '💀 Tử vong hôm nay ⛅',
    #             value = f"{json['todayDeaths']:,}"
    #         ).add_field(
    #             name = '🧪 Đã khỏi',
    #             value = f"{json['recovered']:,}",
    #             inline = False
    #         )
    #         if country != 'World':
    #             embed.title = f'Cập nhật tình hình Covid-19 tại {json["country"]} ❤'
    #     await ctx.send(embed = embed)


