import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import hybrid_command,Context
from typing import Optional

import requests

from PIL import ImageDraw, ImageFont, Image
from bs4 import BeautifulSoup
import io, re, unicodedata, textwrap

async def setup(bot) -> None:
    await bot.add_cog(ImageCog(bot))

PATTERNS = {
        r'[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
        r'[đ]': 'd',
        r'[èéẻẽẹêềếểễệ]': 'e',
        r'[ìíỉĩị]': 'i',
        r'[òóỏõọôồốổỗộơờớởỡợ]': 'o',
        r'[ùúủũụưừứửữự]': 'u',
        r'[ỳýỷỹỵ]': 'y'
    }

with open("./images/classid.txt", "r") as f: classid = f.read().split()

def no_accent_vietnamese(s):
        for pattern, replace in PATTERNS.items():
            s = re.sub(pattern, replace, s)
            s = re.sub(pattern.upper(), replace.upper(), s)
        return s

class ImageCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    
    def getclass(self, idname:str):
        for i,v in enumerate(classid):
            if v==idname:
                id = i
                break
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(f"http://thptchuyennguyentatthanh.kontum.edu.vn/TKB/tkb_2bclass_{id}.html", headers=headers)
        block = BeautifulSoup(r.content.decode(), "html.parser")

        t = block.text.find('TKB có tác dụng từ:')
        date = block.text[t:t+30]

        space = 12
        result = ''
        table = []
        br = 1
        for tr in block.find('table').find_all('tr'):
            if br:
                br=0
                continue
            row = []
            for td in tr.find_all('td'):
                if td.text in ['Buổi', 'Sáng', 'Chiều'] or td.text.isdigit(): continue
                row.append(td.text.replace('\xa0','`'))
                # space = max(space,len(td.text))
                # result += td.text + ' '*(space-len(td.text))
            table.append(row)
        return date, table

    
    @commands.command()
    # @commands.cooldown(1, 300, commands.BucketType.user)
    async def deptrai(self, ctx, *, msg: str):
        await ctx.typing()
        
        img = Image.open('./images/deptraibg.png')

        msg = no_accent_vietnamese(msg)
        para = list(textwrap.wrap(msg, width = 35)[:6])

        MAX_W, MAX_H = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./fonts/8pxbus.ttf', 30, encoding = 'utf-8')

        current_h, pad = 420, 50
        for line in para:
            w, h = draw.textsize(line, font = font)
            draw.text(((MAX_W - w) / 2, current_h), line, fill = 'black', font = font)
            current_h += h + pad


        # ko hiểu thì nhớ 1 cách máy móc cx đc :L dù sau cx chỉ có cách này
        buffer = io.BytesIO()
        img.save(buffer, 'png')
        buffer.seek(0)

        await ctx.reply(file=discord.File(fp=buffer, filename = 'image.png'))
    
    @hybrid_command(name = 'tkb')
    async def tkb(self, ctx :Context, *, idclass):
        img = Image.open('./images/formattkb.png')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 15, encoding = 'utf-8')
        m = []
        dating = ''
        for _ in idclass.split():
            _ = _.upper()
            if _ not in classid or _ in m: continue
            date, table = self.getclass(_)
            for i, v in enumerate(table):
                for j, v in enumerate(v):
                    if v and v!='`': draw.text((110+j*154,33+i*22), v, fill = 'black', font = font)
            m.append(_)
            dating = date

        buffer = io.BytesIO()
        img.save(buffer, 'png')
        buffer.seek(0)
        if dating == '': await ctx.reply(content = "Vui lòng nhập id tkb!")
        else: await ctx.reply(content = dating, file=discord.File(fp=buffer, filename = 'image.png'))