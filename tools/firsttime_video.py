#!/usr/bin/env python3
"""TikTok: 'First time in Ibiza? Follow our step-by-step'. Hook on real footage from frame 0, then the site
step by step inside a phone, then the address. Output: reel_firsttime_tiktok.mp4 (no audio)."""
import subprocess, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = '/tmp/claude-0/-home-claude/66b6d558-d986-5edb-84a4-47ec5aa45195/scratchpad/'
D = S + 'first/'
W, H, FPS = 1080, 1920, 30
LIME, CYAN, INK, BLK, NAVY = (200, 255, 46), (56, 225, 255), (255, 255, 255), (0, 0, 0), (10, 26, 143)
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
PM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
F = ImageFont.truetype
U = '/mnt/user-data/uploads/IMG_0901.MOV'
WEB = '/home/claude/webrepo/video/'

def shade(im, y0, y1, a=180):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, y0, W, y1), fill=a)
    im.paste(Image.new('RGBA', (W, H), (0, 0, 0, 255)), (0, 0), m.filter(ImageFilter.GaussianBlur(90)))
def st(d, xy, s, font, fill, sw=6): d.text(xy, s, font=font, fill=fill, stroke_width=sw, stroke_fill=BLK)
def chip(d, x, y, s, font, bg, fg=BLK):
    w = d.textlength(s, font=font); d.rectangle((x, y, x + w + 36, y + font.size + 22), fill=bg); d.text((x + 18, y + 8), s, font=font, fill=fg)
def tri(d, x, y, sz, fill): d.polygon([(x, y), (x + sz, y), (x + sz / 2, y + sz * .8)], fill=fill)

# ---------- overlays for the footage parts ----------
def ov_hook():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 340, 1150, 190); d = ImageDraw.Draw(im)
    chip(d, 70, 390, 'UK → IBIZA 2027', F(MONO, 40), LIME)
    st(d, (62, 480), 'FIRST TIME', F(PB, 150), INK, 7)
    st(d, (62, 640), 'IN IBIZA?', F(PB, 150), LIME, 7)
    st(d, (68, 820), "Don't wing it.", F(PB, 80), INK, 5)
    tri(d, 74, 950, 56, LIME)
    im.save(D + 'o_hook.png')
def ov_follow():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 380, 1100, 190); d = ImageDraw.Draw(im)
    st(d, (64, 440), 'FOLLOW OUR', F(PB, 118), INK, 6)
    st(d, (64, 570), 'STEP-BY-STEP', F(PB, 118), LIME, 6)
    st(d, (68, 730), 'Everything you need for the', F(PM, 56), INK, 4)
    st(d, (68, 800), 'trip of your life, in one place', F(PM, 56), CYAN, 4)
    im.save(D + 'o_follow.png')
def ov_end():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 330, 1260, 205); d = ImageDraw.Draw(im)
    seal = Image.open(S + 'story/logo.png').convert('RGBA').resize((190, 190), Image.LANCZOS); im.paste(seal, (70, 370), seal)
    st(d, (64, 590), 'YOUR FIRST IBIZA,', F(PB, 92), INK, 6)
    st(d, (64, 700), 'SORTED', F(PB, 150), LIME, 7)
    st(d, (68, 880), 'ibizapartyflights.co.uk', F(PB, 70), INK, 5)
    chip(d, 70, 990, 'TYPE IT IN YOUR BROWSER', F(MONO, 42), LIME)
    st(d, (70, 1100), 'Save this + follow for more', F(PM, 48), CYAN, 4)
    im.save(D + 'o_end.png')
ov_hook(); ov_follow(); ov_end()

def footage(src, ss, du, png, out, punch=True):
    z = "1+0.10*max(0\\,1-t/0.45)" if punch else "1"
    fc = (f"[0:v]setpts=PTS-STARTPTS,fps=30,scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':force_original_aspect_ratio=increase:eval=frame,"
          f"crop=1080:1920,eq=contrast=1.08:saturation=1.15,setsar=1[v];[1:v]format=rgba,fps=30[t];[v][t]overlay=0:0:shortest=1,format=yuv420p[o]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(du), '-i', src, '-loop', '1', '-t', str(du), '-i', png,
                    '-filter_complex', fc, '-map', '[o]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-r', '30', out], check=True)

NEW = D + 'new_party.mp4'  # Rubén's clip sent 13/11; replaces the closing footage
footage(NEW, 12.4, 2.2, D + 'o_hook.png', D + 'p0.mp4')
footage(NEW, 8.4, 1.9, D + 'o_follow.png', D + 'p1.mp4')
footage(NEW, 0.5, 3.0, D + 'o_end.png', D + 'p3.mp4', punch=False)

# ---------- phone part: the site, step by step ----------
SW = 560; SH = round(SW * 2532 / 1170); SX = (W - SW) // 2; SY = 470
def fit(im): return im.convert('RGB').resize((SW, SH), Image.LANCZOS)
SH_ = {n: fit(Image.open(S + 'story/' + n + '.png')) for n in ('flights', 'hotels', 'tickets', 'transfers')}
GFULL = Image.open(D + 'guide_full.png').convert('RGB'); GW = GFULL.size[0]
def guide_at(y):  # y in screenshot px; returns a phone-sized crop of the guide page
    ch = round(GW * 2532 / 1170); return fit(GFULL.crop((0, y, GW, y + ch)))
MAPF = [S + 'story/map/%04d.png' % i for i in range(225)]

bg = Image.new('RGB', (W, H), (6, 10, 60))
g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse((-300, 200, W + 300, H - 100), fill=255)
bg = Image.composite(Image.new('RGB', (W, H), NAVY), bg, g.filter(ImageFilter.GaussianBlur(220)))
gd = ImageDraw.Draw(bg)
for x in range(0, W, 60): gd.line((x, 0, x, H), fill=(22, 40, 150))
for y in range(0, H, 60): gd.line((0, y, W, y), fill=(22, 40, 150))
phone = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(phone).rounded_rectangle((SX - 22, SY - 22, SX + SW + 22, SY + SH + 22), 64, fill=(8, 8, 12, 255), outline=(60, 70, 140, 255), width=3)
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).rounded_rectangle((SX - 30, SY - 30, SX + SW + 30, SY + SH + 30), 70, outline=CYAN + (150,), width=10)
glow = glow.filter(ImageFilter.GaussianBlur(18))
mask = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, SW - 1, SH - 1), 44, fill=255)
def ease(t): t = max(0., min(1., t)); return t * t * (3 - 2 * t)

def cap(d, n, title, a):
    off = int((1 - a) * 20)
    f1 = F(MONO, 34); s = f'STEP {n}/6'; w = d.textlength(s, font=f1) + 36
    d.rectangle((70, 210 + off, 70 + w, 262 + off), fill=LIME); d.text((88, 216 + off), s, font=f1, fill=BLK)
    d.text((70, 290 + off), title, font=F(PB, 88), fill=INK)
    for k in range(6):  # progress
        x = 70 + k * 52; d.rectangle((x, 180, x + 40, 190), fill=LIME if k < n else (60, 80, 180))

def frame(scr, n, title, a):
    im = bg.copy(); im.paste(glow, (0, 0), glow); im.paste(phone, (0, 0), phone); im.paste(scr, (SX, SY), mask)
    cap(ImageDraw.Draw(im), n, title, a); return im

def slide(a, b, t):
    e = ease(t); c = Image.new('RGB', (SW, SH * 2)); c.paste(a, (0, 0)); c.paste(b, (0, SH)); o = int(e * SH); return c.crop((0, o, SW, o + SH))

steps = []  # (n, title, list-of-screens per frame)
gy0, gy1 = 2050, 6300
steps.append((1, 'First-timer guide', [guide_at(int(gy0 + (gy1 - gy0) * ease(i / 54))) for i in range(54)]))
steps.append((2, 'Compare flights', [SH_['flights']] * 40))
steps.append((3, 'Pick where to stay', [SH_['hotels']] * 40))
steps.append((4, 'The island map', [fit(Image.open(MAPF[i])) for i in range(0, 150, 2)]))
steps.append((5, 'Club tickets', [SH_['tickets']] * 36))
steps.append((6, 'Airport ride', [SH_['transfers']] * 36))

ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                       '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', D + 'p2.mp4'], stdin=subprocess.PIPE)
prev = None
for n, title, scrs in steps:
    if prev is not None:
        for i in range(9): ff.stdin.write(frame(slide(prev, scrs[0], (i + 1) / 9), n, title, 0).tobytes())
    for i, sc in enumerate(scrs): ff.stdin.write(frame(sc, n, title, ease(i / 6)).tobytes())
    prev = scrs[-1]
ff.stdin.close(); ff.wait()

# ---------- join ----------
with open(D + 'list.txt', 'w') as f:
    for p in ('p0', 'p1', 'p2', 'p3'): f.write(f"file '{D}{p}.mp4'\n")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', D + 'list.txt', '-c:v', 'libx264', '-preset', 'medium',
                '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', D + 'reel_firsttime_tiktok.mp4'], check=True)
print('done')
