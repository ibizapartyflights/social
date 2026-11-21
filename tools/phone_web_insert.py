#!/usr/bin/env python3
"""Phone insert: our own site (rendered locally from tools/web) inside a phone, address bar typed,
page scrolls to a highlighted line. 100% own content. Usage:
python3 tools/phone_web_insert.py full.png target_y_css out.mp4 [secs]   (full.png = 2x fullPage at 390px)"""
import sys, os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
full, ty, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]; secs = float(sys.argv[4]) if len(sys.argv) > 4 else 4.5
W, H, FPS = 1080, 1920, 30
LIME, CYAN, INK, BLK = (200, 255, 46), (56, 225, 255), (255, 255, 255), (0, 0, 0)
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; PM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
F = ImageFont.truetype
page = Image.open(full).convert('RGB'); SW = 720; k = SW / page.width
page = page.resize((SW, int(page.height * k)), Image.LANCZOS)
PX, PY, PW, PH = 150, 430, 780, 1400   # phone body
SX, SY, SH = PX + 30, PY + 150, PH - 190  # screen (below address bar)
bg = Image.new('RGB', (W, H), (4, 7, 46)); d = ImageDraw.Draw(bg)
for r, c in ((900, (10, 26, 143)), (600, (49, 80, 255))):
    g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse((W//2 - r, 1100 - r, W//2 + r, 1100 + r), fill=110)
    bg.paste(Image.new('RGB', (W, H), c), (0, 0), g.filter(ImageFilter.GaussianBlur(160)))
d = ImageDraw.Draw(bg)
def st(dr, xy, s, f, fill, sw=6): dr.text(xy, s, font=f, fill=fill, stroke_width=sw, stroke_fill=BLK)
t1 = F(PB, 84); st(d, (70, 150), "IT'S ALL IN OUR", t1, INK); st(d, (70, 245), "IBIZA CLUBS GUIDE", t1, LIME)
URL = 'ibizapartyflights.co.uk'; target = max(0, int(ty * 2 * k) - 420)
tmp = tempfile.mkdtemp(); N = int(secs * FPS)
for i in range(N):
    t = i / FPS; im = bg.copy(); dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((PX, PY, PX + PW, PY + PH), 70, fill=(12, 14, 30), outline=CYAN, width=6)
    dr.rounded_rectangle((PX + 30, PY + 40, PX + PW - 30, PY + 130), 30, fill=(235, 238, 245))
    n = min(len(URL), int(t / 0.04)); uf = F(PM, 40)
    dr.text((PX + 70, PY + 60), URL[:n] + ('|' if n < len(URL) and i % 10 < 6 else ''), font=uf, fill=(20, 20, 40))
    e = min(1, max(0, (t - 1.2) / 2.2)); e = e * e * (3 - 2 * e); y = int(target * e)
    im.paste(page.crop((0, y, SW, y + SH)), (SX, SY))
    m = Image.new('L', (W, H), 255); ImageDraw.Draw(m).rounded_rectangle((SX, SY, SX + SW, SY + SH), 34, fill=0)
    # keep screen corners rounded: repaint phone body outside screen corners
    im.save(f'{tmp}/{i:04d}.png')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/%04d.png', '-c:v', 'libx264', '-crf', '17',
                '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', out], check=True)
print('done', out)
