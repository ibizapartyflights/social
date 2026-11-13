#!/usr/bin/env python3
"""TikTok remake of 'Ibiza clubs FAQ 2/3: getting home' using ONLY Rubén's own footage (13/11/2026).
Hook text on screen from frame 0, hard cuts ~1.8 s, no alcohol references. Output: reel_home_v2_tiktok.mp4 (no audio).
Usage: faq2.py  (segment sources/times are set in SEG below)"""
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = os.path.dirname(os.path.abspath(__file__)) + '/'
W, H = 1080, 1920
LIME, CYAN, INK, BLK = (200, 255, 46), (56, 225, 255), (255, 255, 255), (0, 0, 0)
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
PM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
F = ImageFont.truetype
SEAL = '/tmp/claude-0/-home-claude/66b6d558-d986-5edb-84a4-47ec5aa45195/scratchpad/story/logo.png'

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]
def fitfont(d, lines, path, size, maxw):
    while size > 40 and any(d.textlength(l, font=F(path, size)) > maxw for l in lines): size -= 4
    return F(path, size)
def shade(im, y0, y1, a=180):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, y0, W, y1), fill=a)
    im.paste(Image.new('RGBA', (W, H), (0, 0, 0, 255)), (0, 0), m.filter(ImageFilter.GaussianBlur(90)))
def st(d, xy, s, font, fill, sw=6): d.text(xy, s, font=font, fill=fill, stroke_width=sw, stroke_fill=BLK)
def chip(d, x, y, s, font, bg, fg=BLK):
    w = d.textlength(s, font=font); d.rectangle((x, y, x + w + 36, y + font.size + 22), fill=bg); d.text((x + 18, y + 8), s, font=font, fill=fg)
    return y + font.size + 22

def hook():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 330, 1160, 190); d = ImageDraw.Draw(im)
    y = chip(d, 70, 380, 'IBIZA CLUBS FAQ 2/3', F(MONO, 42), LIME) + 36
    for s, c in (('HOW DO YOU', INK), ('GET HOME', LIME), ('AT 6AM?', INK)):
        st(d, (62, y), s, F(PB, 140), c, 7); y += 152
    st(d, (68, y + 6), '5 things Ibiza regulars do', F(PM, 54), CYAN, 4)
    d.polygon([(74, y + 100), (130, y + 100), (102, y + 145)], fill=LIME)
    im.save(D + 'o0.png')

TIPS = [('PRE-BOOK YOUR RIDE HOME', 'Closing-time taxi queues can be long'),
        ('PICK A MEET-UP SPOT', 'Agree it before the first drop, not after'),
        ('SAVE YOUR HOTEL ADDRESS OFFLINE', 'No signal at 6am? Still sorted'),
        ('KEEP BATTERY FOR THE RIDE', 'A power bank makes you the group hero'),
        ('GET HOME TOGETHER', 'Same squad in, same squad out')]
def tip(i, t, s):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 340, 1140, 180); d = ImageDraw.Draw(im)
    for k in range(5):
        x = 70 + k * 46; d.rectangle((x, 340, x + 34, 352), fill=LIME if k < i else (255, 255, 255, 110))
    n = F(PB, 150); w = d.textlength(f'{i}/5', font=n)
    d.rectangle((64, 400, 64 + w + 48, 590), fill=LIME); d.text((88, 402), f'{i}/5', font=n, fill=BLK)
    lines = wrap(d, t, F(PB, 104), W - 150); tf = fitfont(d, lines, PB, 104, W - 140)
    y = 640
    for l in lines: st(d, (64, y), l, tf, INK, 6); y += int(tf.size * 1.12)
    y += 16
    for l in wrap(d, s, F(PM, 52), W - 150): st(d, (68, y), l, F(PM, 52), CYAN, 4); y += 66
    im.save(D + f'o{i}.png')
def end():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 330, 1220, 200); d = ImageDraw.Draw(im)
    seal = Image.open(SEAL).convert('RGBA').resize((180, 180), Image.LANCZOS); im.paste(seal, (70, 380), seal)
    for k, (s, c) in enumerate((('SUNRISE', LIME), ('OR BED', INK), ('BY 3?', INK))):
        st(d, (62, 590 + k * 150), s, F(PB, 140), c, 7)
    chip(d, 70, 1060, 'FOLLOW FOR PART 3/3', F(MONO, 44), INK)
    st(d, (70, 1160), '@ibizapartyflights', F(PM, 44), CYAN, 4)
    im.save(D + 'o6.png')

hook(); [tip(i, t, s) for i, (t, s) in enumerate(TIPS, 1)]; end()

SEG = [tuple(x) for x in __import__('json').load(open(D + 'seg.json'))]   # [src, start, dur, punch]
args = ['ffmpeg', '-v', 'error', '-y']
for src, ss, du, _ in SEG: args += ['-ss', str(ss), '-t', str(du), '-i', src]
for k, s in enumerate(SEG): args += ['-loop', '1', '-t', str(s[2]), '-i', D + f'o{k}.png']
n = len(SEG); fc = []
for k, (src, ss, du, punch) in enumerate(SEG):
    z = "1+0.10*max(0\\,1-t/0.45)" if punch else "1"
    fc.append(f"[{k}:v]setpts=PTS-STARTPTS,fps=30,scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':force_original_aspect_ratio=increase:eval=frame,"
              f"crop=1080:1920,eq=contrast=1.08:saturation=1.12,setsar=1[v{k}];[{n+k}:v]format=rgba,fps=30[t{k}];[v{k}][t{k}]overlay=0:0:shortest=1,format=yuv420p[s{k}]")
fc.append(''.join(f'[s{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=0[out]')
args += ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
         '-r', '30', '-movflags', '+faststart', D + 'reel_home_v2_tiktok.mp4']
subprocess.run(args, check=True); print('done')
