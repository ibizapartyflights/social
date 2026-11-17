#!/usr/bin/env python3
"""TikTok "This or that" on 100% own graphics: scrolling brand wave pattern + two colour panels per pair,
hook readable on frame 0, cut every 1.8 s, panels slide in on each cut (except frame 0). No footage, no stock.
Usage: python3 tools/this_or_that_video.py spec.json out_dir
Spec: {"name","chip","hook":[[text,col],...],"hook_sub","pairs":[[A,B],...],"end_big","end_sub"}"""
import subprocess, os, sys, json, math
from PIL import Image, ImageDraw, ImageFont
spec = json.load(open(sys.argv[1])); D = sys.argv[2]; os.makedirs(D, exist_ok=True)
W, H = 1080, 1920
LIME, CYAN, INK, BLK, NAVY, ROYAL, NIGHT = (200,255,46), (56,225,255), (255,255,255), (0,0,0), (10,26,143), (49,80,255), (4,7,46)
COL = {'lime': LIME, 'ink': INK, 'cyan': CYAN}
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; PM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'; F = ImageFont.truetype
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fit(d, s, path, size, maxw):
    while size > 40 and d.textlength(s, font=F(path, size)) > maxw: size -= 4
    return F(path, size)
def st(d, xy, s, font, fill, sw=6, anchor=None): d.text(xy, s, font=font, fill=fill, stroke_width=sw, stroke_fill=BLK, anchor=anchor)
def chip(d, x, y, s, font, bg, fg=BLK):
    w = d.textlength(s, font=font); d.rectangle((x, y, x + w + 36, y + font.size + 20), fill=bg); d.text((x + 18, y + 8), s, font=font, fill=fg)

# background pattern (period 360 x 150, scrolled by whole pixels)
bg = Image.new('RGB', (W * 2, H * 2), NIGHT); d = ImageDraw.Draw(bg)
for y0 in range(-150, H * 2 + 150, 150):
    d.line([(x, y0 + 46 * math.sin(2 * math.pi * x / 360)) for x in range(0, W * 2 + 8, 8)], fill=NAVY, width=34, joint='curve')
bg.save(os.path.join(D, 'bg.png'))

P = spec['pairs']; N = len(P)
def header(d, k):
    chip(d, 64, 250, spec['chip'], F(MONO, 40), LIME)
    if k: st(d, (W - 64, 250), f'{k}/{N}', F(PB, 64), INK, 5, 'ra')
def blank(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
scenes = []  # (dur, [(png, slide_from)]) slide_from: 0 none, -1 left, +1 right
# hook
im = blank(); d = ImageDraw.Draw(im); header(d, 0); y = 560
for s, c in spec['hook']:
    f = fit(d, s, PB, 150, W - 128); st(d, (64, y), s, f, COL[c], 7); y += int(f.size * 1.1)
st(d, (66, y + 20), spec['hook_sub'], F(PM, 56), CYAN, 4); im.save(os.path.join(D, 'h.png')); scenes.append((2.2, [('h.png', 0)]))
cols = [(ROYAL, INK, LIME, BLK), (LIME, BLK, ROYAL, INK), (NAVY, INK, CYAN, BLK)]
for k, (a, b) in enumerate(P, 1):
    ca, ta, cb, tb = cols[(k - 1) % 3]
    A = blank(); d = ImageDraw.Draw(A); d.rectangle((40, 470, W - 40, 1010), fill=ca + (255,))
    f = fit(d, a, PB, 120, W - 160); d.text((W // 2, 740), a, font=f, fill=ta, anchor='mm'); A.save(os.path.join(D, f'a{k}.png'))
    B = blank(); d = ImageDraw.Draw(B); d.rectangle((40, 1090, W - 40, 1630), fill=cb + (255,))
    f = fit(d, b, PB, 120, W - 160); d.text((W // 2, 1360), b, font=f, fill=tb, anchor='mm'); B.save(os.path.join(D, f'b{k}.png'))
    T = blank(); d = ImageDraw.Draw(T); header(d, k)
    d.ellipse((W // 2 - 90, 960, W // 2 + 90, 1140), fill=BLK, outline=LIME, width=8); d.text((W // 2, 1050), 'OR', font=F(PB, 76), fill=LIME, anchor='mm')
    T.save(os.path.join(D, f't{k}.png')); scenes.append((1.8, [(f'a{k}.png', -1), (f'b{k}.png', 1), (f't{k}.png', 0)]))
im = blank(); d = ImageDraw.Draw(im); header(d, 0)
seal = Image.open(os.path.join(ROOT, 'assets/brand/perfil_sello_oscuro.png')).convert('RGBA').resize((220, 220))
m = Image.new('L', (220, 220), 0); ImageDraw.Draw(m).ellipse((0, 0, 219, 219), fill=255); seal.putalpha(m); im.paste(seal, (64, 470), seal)
y = 740
for s in spec['end_big']:
    f = fit(d, s, PB, 130, W - 128); st(d, (64, y), s, f, LIME, 7); y += int(f.size * 1.1)
st(d, (66, y + 20), spec['end_sub'], F(PM, 56), INK, 4); st(d, (66, y + 110), '@ibizapartyflights', F(PM, 48), CYAN, 4)
im.save(os.path.join(D, 'e.png')); scenes.append((2.4, [('e.png', 0)]))

args = ['ffmpeg', '-v', 'error', '-y']; fc = []; idx = 0; outs = []
for si, (du, layers) in enumerate(scenes):
    args += ['-loop', '1', '-framerate', '30', '-t', str(du), '-i', os.path.join(D, 'bg.png')]; b = idx; idx += 1
    sp = 6; dirx = 1 if si % 2 else -1
    cx = f"mod(n*{sp},360)" if dirx > 0 else f"360-mod(n*{sp},360)"
    fc.append(f"[{b}:v]fps=30,crop=1080:1920:'{cx}':'mod(n*3,150)',format=rgba,setsar=1[bg{si}]"); cur = f'bg{si}'
    for li, (png, sl) in enumerate(layers):
        args += ['-loop', '1', '-framerate', '30', '-t', str(du), '-i', os.path.join(D, png)]; j = idx; idx += 1
        x = '0' if sl == 0 else f"{sl}*1100*max(0\\,1-t/0.22)*max(0\\,1-t/0.22)"
        fc.append(f"[{cur}][{j}:v]overlay=x='{x}':y=0:shortest=1[o{si}_{li}]"); cur = f'o{si}_{li}'
    fc.append(f"[{cur}]format=yuv420p[s{si}]"); outs.append(f'[s{si}]')
fc.append(''.join(outs) + f'concat=n={len(outs)}:v=1:a=0[out]')
args += ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30',
         '-movflags', '+faststart', os.path.join(D, spec['name'] + '_tiktok.mp4')]
subprocess.run(args, check=True); print('done', spec['name'])
