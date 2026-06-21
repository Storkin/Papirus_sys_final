# -*- coding: utf-8 -*-
"""Papirus SYS için basit bir .ico uygulama ikonu üretir."""
from PIL import Image, ImageDraw, ImageFont
import os

SIZE = 256
img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# Lacivert-mavi yuvarlak köşeli kare
d.rounded_rectangle([8, 8, SIZE - 8, SIZE - 8], radius=48, fill=(46, 85, 160, 255))

# Ortada "P" harfi
try:
    font = ImageFont.truetype("arialbd.ttf", 170)
except Exception:
    try:
        font = ImageFont.truetype("arial.ttf", 170)
    except Exception:
        font = ImageFont.load_default()

text = "P"
bbox = d.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
d.text(((SIZE - tw) / 2 - bbox[0], (SIZE - th) / 2 - bbox[1]), text, font=font, fill=(255, 255, 255, 255))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'papirus.ico')
img.save(out, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print('Ikon olusturuldu:', out)
