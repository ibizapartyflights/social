#!/usr/bin/env python3
"""Story video: the website inside a phone, with the island map as the hero. Writes raw frames to stdout."""
import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = '/tmp/claude-0/-home-claude/66b6d558-d986-5edb-84a4-47ec5aa45195/scratchpad/story/'
FPS, W, H = 30, 1080, 1920
NAVY, LIME, CYAN, BLUE, INK = (10, 26, 143), (200, 255, 46), (56, 225, 255), (49, 80, 255), (242, 242, 242)
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
def F(p, s): return ImageFont.truetype(p, s)

# phone screen geometry (screenshots are 1170x2532)
SW = 560; SH = round(SW * 2532 / 1170); SX = (W - SW) // 2; SY = 436
def load(n): return Image.open(D + n + '.png').convert('RGB').resize((SW, SH), Image.LANCZOS)
SHOTS = {n: load(n) for n in ('hero', 'flights', 'hotels', 'tickets')}
MAPF = [D + 'map/%04d.png' % i for i in range(225)]

# background: navy radial glow + faint grid
bg = Image.new('RGB', (W, H), (6, 10, 60))
g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse((-300, 200, W + 300, H - 100), fill=255)
g = g.filter(ImageFilter.GaussianBlur(220))
bg = Image.composite(Image.new('RGB', (W, H), NAVY), bg, g)
gd = ImageDraw.Draw(bg)
for x in range(0, W, 60): gd.line((x, 0, x, H), fill=(22, 40, 150))
for y in range(0, H, 60): gd.line((0, y, W, y), fill=(22, 40, 150))

# phone body
phone = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(phone)
pd.rounded_rectangle((SX - 22, SY - 22, SX + SW + 22, SY + SH + 22), 64, fill=(8, 8, 12, 255), outline=(60, 70, 140, 255), width=3)
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).rounded_rectangle((SX - 30, SY - 30, SX + SW + 30, SY + SH + 30), 70, outline=CYAN + (150,), width=10)
glow = glow.filter(ImageFilter.GaussianBlur(18))
mask = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, SW - 1, SH - 1), 44, fill=255)

def tri(d, x, y, sz, fill):
    d.polygon([(x, y), (x + sz, y), (x + sz / 2, y + sz * .8)], fill=fill)

def ease(t): t = max(0., min(1., t)); return t * t * (3 - 2 * t)

def text_c(d, y, s, font, fill):
    w = d.textlength(s, font=font); d.text(((W - w) / 2, y), s, font=font, fill=fill)

def label(d, step, title, sub, a):
    """Top caption: lime tag + big title, faded in by a (0..1)."""
    if a <= 0: return
    off = int((1 - a) * 24)
    f1, f2, f3 = F(MONO, 30), F(PB, 66), F(PB, 32)
    tw = d.textlength(step, font=f1) + 32
    x = (W - tw) / 2; y = 196 + off
    d.rectangle((x, y, x + tw, y + 48), fill=LIME); d.text((x + 16, y + 7), step, font=f1, fill=(0, 0, 0))
    text_c(d, 258 + off, title, f2, INK)
    if sub: text_c(d, 340 + off, sub, f3, CYAN)

def bottom(d, a, big=False):
    if a <= 0: return
    f = F(PB, 40 if not big else 46)
    s = 'TAP THE LINK'
    w = d.textlength(s, font=f) + 110; x = (W - w) / 2; y = SY + SH + 50
    d.rounded_rectangle((x, y, x + w, y + 74), 37, fill=LIME); d.text((x + 30, y + 10), s, font=f, fill=(0, 0, 0)); tri(d, x + w - 70, y + 26, 30, (0, 0, 0))

def frame(screen, cap, bot=0., extra=None):
    im = bg.copy(); im.paste(glow, (0, 0), glow); im.paste(phone, (0, 0), phone)
    im.paste(screen, (SX, SY), mask)
    d = ImageDraw.Draw(im)
    if cap: label(d, *cap)
    bottom(d, bot)
    if extra: extra(im, d)
    return im

def slide(a, b, t):
    """Vertical scroll from screen a to screen b."""
    e = ease(t); c = Image.new('RGB', (SW, SH * 2)); c.paste(a, (0, 0)); c.paste(b, (0, SH))
    o = int(e * SH); return c.crop((0, o, SW, o + SH))

out = sys.stdout.buffer
def emit(im): out.write(im.tobytes())

# 1. intro card (1.6 s)
logo = Image.open(D + 'logo.png').convert('RGBA').resize((300, 300), Image.LANCZOS)
for i in range(48):
    t = i / 48; im = bg.copy(); d = ImageDraw.Draw(im); a = ease(t * 2.2)
    lg = logo.rotate(-t * 40, resample=Image.BICUBIC); im.paste(lg, ((W - 300) // 2, 520), lg)
    off = int((1 - a) * 30)
    text_c(d, 900 + off, 'YOUR IBIZA TRIP,', F(PB, 84), INK)
    text_c(d, 1000 + off, 'SORTED IN ONE PLACE', F(PB, 84), LIME)
    f4 = F(PB, 44); s4 = 'Here’s how it works'; w4 = d.textlength(s4, font=f4) + 50; x4 = (W - w4) / 2
    d.text((x4, 1130 + off), s4, font=f4, fill=CYAN); tri(d, x4 + w4 - 30, 1150 + off, 30, CYAN)
    emit(im)

# 2. quick tour: hero → flights → hotels (each ~1.5 s, 0.4 s scroll)
seq = [('hero', ('IBIZAPARTYFLIGHTS.CO.UK', 'Open the site', None)),
       ('flights', ('STEP 1', 'Compare flights', 'From every UK airport')),
       ('hotels', ('STEP 2', 'Pick where to stay', 'Near the clubs you want'))]
for k, (name, cap) in enumerate(seq):
    hold = 34 if k else 40
    for i in range(hold):
        emit(frame(SHOTS[name], cap + (ease(i / 8),), bot=0))
    nxt = SHOTS[seq[k + 1][0]] if k + 1 < len(seq) else Image.open(MAPF[0]).convert('RGB').resize((SW, SH), Image.LANCZOS)
    for i in range(12):
        emit(frame(slide(SHOTS[name], nxt, (i + 1) / 12), cap + (1 - ease(i / 6),)))

# 3. THE MAP (7.5 s): live radar, points switching
names = {0: "Playa d'en Bossa", 56: 'Ushuaïa', 112: 'Pacha', 168: 'San Antonio'}
def badge(im, d, i):
    # pulsing NEW tag on the phone corner
    p = 1 + 0.06 * math.sin(i / 30 * 2 * math.pi * 1.2)
    f = F(MONO, int(30 * p)); s = 'NEW'
    w = d.textlength(s, font=f) + 26; x = SX + SW - w + 30; y = SY - 46
    d.rectangle((x, y, x + w, y + 46 * p), fill=CYAN); d.text((x + 13, y + 6), s, font=f, fill=(0, 0, 0))
for i in range(225):
    scr = Image.open(MAPF[i]).convert('RGB').resize((SW, SH), Image.LANCZOS)
    emit(frame(scr, ('STEP 3 · NEW', 'The island map', 'Hotel zones + clubs, live', ease(i / 8)), bot=0, extra=lambda im, d, i=i: badge(im, d, i)))

# 4. tickets (1.4 s)
last = Image.open(MAPF[-1]).convert('RGB').resize((SW, SH), Image.LANCZOS)
for i in range(12):
    emit(frame(slide(last, SHOTS['tickets'], (i + 1) / 12), None))
for i in range(32):
    emit(frame(SHOTS['tickets'], ('STEP 4', 'Grab club tickets', 'From the official sellers', ease(i / 8))))

# 5. outro (3 s): URL + tap the link
for i in range(90):
    t = i / 90; im = bg.copy(); d = ImageDraw.Draw(im); a = ease(t * 3)
    lg = logo.rotate(-40 - t * 30, resample=Image.BICUBIC); im.paste(lg, ((W - 300) // 2, 470), lg)
    off = int((1 - a) * 30)
    text_c(d, 840 + off, 'PLAN YOUR IBIZA 2027', F(PB, 74), INK)
    text_c(d, 940 + off, 'ibizapartyflights.co.uk', F(PB, 62), LIME)
    text_c(d, 1050 + off, 'Flights · hotels · tickets · map', F(PB, 40), CYAN)
    pulse = 1 + 0.04 * math.sin(t * 2 * math.pi * 2)
    f = F(PB, int(50 * pulse)); s = 'TAP THE LINK'
    w = d.textlength(s, font=f) + 130; x = (W - w) / 2; y = 1250
    if a > 0.3:
        d.rounded_rectangle((x, y, x + w, y + 90 * pulse), 45, fill=LIME); d.text((x + 35, y + 14), s, font=f, fill=(0, 0, 0)); tri(d, x + w - 82, y + 32 * pulse, 38 * pulse, (0, 0, 0))
    if a > 0.3:
        for k in range(3):
            yy = 1390 + k * 34 + int(10 * math.sin(t * 2 * math.pi * 2 - k)); tri(d, W / 2 - 22, yy, 44, LIME + (0,) if False else LIME)
    emit(im)
