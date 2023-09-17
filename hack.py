import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import io

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


with open("./images/classid.txt", "r") as f: classid = f.read().split()

def getclass(self, id:str):
    for i,v in enumerate(self.classid):
        if v==id:
            id = i+1
            break
    r = requests.get(f"http://thptchuyennguyentatthanh.kontum.edu.vn/TKB/tkb_2bclass_{id}.html", headers=headers)
    block = BeautifulSoup(r.content.decode(), "html.parser")
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
    return table

def drawclass(idclass):
    img = Image.open('./images/formattkb.png')

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 15, encoding = 'utf-8')
    for _ in idclass:
        if _ not in classid: continue
        table = getclass(_)
        for i, v in enumerate(table):
            for j, v in enumerate(v):
                if v and v!='`': draw.text((110+j*154,33+i*22), v, fill = 'black', font = font)

    buffer = io.BytesIO()
    img.save(buffer, 'png')
    buffer.seek(0)