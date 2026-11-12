#!/usr/bin/env python3
"""Hook-first TikTok: 'Don't book Ibiza 2027 until you know these 5 things', on real club footage.
Text is fully on screen from frame 0. Hard cuts every ~1.8 s. Output: reel_hook5_tiktok.mp4 (no audio)."""
import subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
LIME, CYAN, INK, BLK = (200, 255, 46), (56, 225, 255), (255, 255, 255), (0, 0, 0)
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
PM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
F = ImageFont.truetype
U = '/mnt/user-data/uploads/IMG_0901.MOV'
WEB = '/home/claude/webrepo/video/'

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def shade(im, y0, y1, a=170):
    """Soft dark band behind the text so it reads on any footage."""
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, y0, W, y1), fill=a)
    m = m.filter(ImageFilter.GaussianBlur(90))
    im.paste(Image.new('RGBA', (W, H), (0, 0, 0, 255)), (0, 0), m)

def stroke_text(d, xy, s, font, fill, sw=6):
    d.text(xy, s, font=font, fill=fill, stroke_width=sw, stroke_fill=BLK)

def chip(d, x, y, s, font, bg, fg=BLK, pad=(18, 10)):
    w = d.textlength(s, font=font); h = font.size
    d.rectangle((x, y, x + w + pad[0] * 2, y + h + pad[1] * 2), fill=bg); d.text((x + pad[0], y + pad[1] - 2), s, font=font, fill=fg)
    return y + h + pad[1] * 2

def hook_png():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 330, 1150, 185); d = ImageDraw.Draw(im)
    y = chip(d, 70, 380, 'BRITS, READ THIS', F(MONO, 40), LIME) + 34
    big = F(PB, 138)
    for s, c in (("DON'T BOOK", INK), ('IBIZA 2027', LIME)):
        stroke_text(d, (64, y), s, big, c, 7); y += 150
    y += 8; mid = F(PB, 76)
    for s in ('UNTIL YOU KNOW', 'THESE 5 THINGS'):
        stroke_text(d, (68, y), s, mid, INK, 5); y += 88
    # arrow cue
    d.polygon([(70, y + 30), (130, y + 30), (100, y + 75)], fill=LIME)
    im.save(os.path.join(D, 'o0.png'))

TIPS = [('CHECK THE CLUB DATES FIRST', 'Book flights around the night you want'),
        ('STAY NEAR YOUR CLUB', 'Late-night taxis add up fast'),
        ('PRE-BOOK YOUR AIRPORT RIDE', 'Peak-season taxi queues get long'),
        ('OFFICIAL TICKET SELLERS ONLY', 'Resale scams are real'),
        ('SORT YOUR DATA BEFORE YOU FLY', 'Check roaming or grab an eSIM')]

def tip_png(i, title, sub):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 360, 1120, 175); d = ImageDraw.Draw(im)
    num = F(PB, 150); s = f'{i}/5'
    w = d.textlength(s, font=num)
    d.rectangle((64, 400, 64 + w + 48, 400 + 190), fill=LIME); d.text((88, 402), s, font=num, fill=BLK)
    y = 640; tf = F(PB, 104)
    for line in wrap(d, title, tf, W - 150):
        stroke_text(d, (64, y), line, tf, INK, 6); y += 116
    y += 18
    for line in wrap(d, sub, F(PM, 52), W - 150):
        stroke_text(d, (68, y), line, F(PM, 52), CYAN, 4); y += 66
    # progress dots
    for k in range(5):
        x = 70 + k * 46; d.rectangle((x, 340, x + 34, 352), fill=LIME if k < i else (255, 255, 255, 110))
    im.save(os.path.join(D, f'o{i}.png'))

def end_png():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 380, 1180, 195); d = ImageDraw.Draw(im)
    seal = Image.open('/tmp/claude-0/-home-claude/66b6d558-d986-5edb-84a4-47ec5aa45195/scratchpad/story/logo.png').convert('RGBA').resize((200, 200), Image.LANCZOS)
    im.paste(seal, (70, 400), seal)
    stroke_text(d, (64, 640), 'SAVE THIS', F(PB, 150), LIME, 7)
    stroke_text(d, (68, 810), 'for the group chat', F(PB, 76), INK, 5)
    chip(d, 70, 950, 'FOLLOW FOR PART 2', F(MONO, 46), INK)
    stroke_text(d, (70, 1060), '@ibizapartyflights', F(PM, 44), CYAN, 4)
    im.save(os.path.join(D, 'o6.png'))

hook_png()
for i, (t, s) in enumerate(TIPS, 1): tip_png(i, t, s)
end_png()

# (source, start, duration, punch-in)
SEG = [(U, 59.6, 2.3, True), (WEB + 'lasers_red.mp4', 0.4, 1.8, True), (U, 1.0, 1.8, True),
       (WEB + 'stage_gold.mp4', 0.4, 1.8, True), (U, 28.0, 1.8, True), (WEB + 'club_haze.mp4', 0.4, 1.8, True),
       (U, 65.5, 2.6, False)]
args = ['ffmpeg', '-v', 'error', '-y']
for src, ss, du, _ in SEG: args += ['-ss', str(ss), '-t', str(du), '-i', src]
for k in range(len(SEG)): args += ['-loop', '1', '-t', str(SEG[k][2]), '-i', os.path.join(D, f'o{k}.png')]
n = len(SEG); fc = []
for k, (src, ss, du, punch) in enumerate(SEG):
    z = "1+0.10*max(0\\,1-t/0.45)" if punch else "1"
    fc.append(f"[{k}:v]setpts=PTS-STARTPTS,fps=30,scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':force_original_aspect_ratio=increase:eval=frame,"
              f"crop=1080:1920,eq=contrast=1.08:saturation=1.15,setsar=1[v{k}];"
              f"[{n+k}:v]format=rgba,fps=30[t{k}];[v{k}][t{k}]overlay=0:0:shortest=1,format=yuv420p[s{k}]")
fc.append(''.join(f'[s{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=0[out]')
args += ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
         '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', os.path.join(D, 'reel_hook5_tiktok.mp4')]
subprocess.run(args, check=True)
print('done')
