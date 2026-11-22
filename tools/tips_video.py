#!/usr/bin/env python3
"""Hook-first TikTok on Rubén's own footage (same format as hook5_video.py, but driven by a JSON spec).
Usage: python3 tools/tips_video.py spec.json out_dir
Spec: {"name": "reel_x", "chip": "...", "hook_big": [[text, "lime"|"ink"], ...], "hook_mid": [...],
       "tips": [[title, sub], ...] (5), "end_big": "...", "end_mid": "...", "end_chip": "...",
       "seg": [[clip, start, dur, punch], ...]  # len = tips + 2 (hook, tips..., end)}
Only own clips from assets/clips/. Output: <name>_tiktok.mp4 (no audio). Text visible from frame 0."""
import subprocess, os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CL = os.path.join(ROOT, 'assets/clips/')
spec = json.load(open(sys.argv[1])); D = sys.argv[2]; os.makedirs(D, exist_ok=True)
W, H = 1080, 1920
LIME, CYAN, INK, BLK = (200, 255, 46), (56, 225, 255), (255, 255, 255), (0, 0, 0)
COL = {'lime': LIME, 'ink': INK, 'cyan': CYAN}
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
PM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
F = ImageFont.truetype

def seal(size):
    im = Image.open(os.path.join(ROOT, 'assets/brand/perfil_sello_oscuro.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255); im.putalpha(m); return im

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def fit(d, lines, path, size, maxw):
    """Largest font size <= size where every line fits (never hyphenate words)."""
    while size > 40 and any(d.textlength(s, font=F(path, size)) > maxw for s in lines): size -= 4
    return F(path, size)

def shade(im, y0, y1, a=175):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, y0, W, y1), fill=a)
    im.paste(Image.new('RGBA', (W, H), (0, 0, 0, 255)), (0, 0), m.filter(ImageFilter.GaussianBlur(90)))

def st(d, xy, s, font, fill, sw=6): d.text(xy, s, font=font, fill=fill, stroke_width=sw, stroke_fill=BLK)

def chip(d, x, y, s, font, bg, fg=BLK, pad=(18, 10)):
    w = d.textlength(s, font=font); h = font.size
    d.rectangle((x, y, x + w + pad[0] * 2, y + h + pad[1] * 2), fill=bg); d.text((x + pad[0], y + pad[1] - 2), s, font=font, fill=fg)
    return y + h + pad[1] * 2

N = len(spec['tips'])
def hook_png():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 330, 1180, 185); d = ImageDraw.Draw(im)
    y = chip(d, 70, 380, spec['chip'], F(MONO, 40), LIME) + 34
    big = fit(d, [s for s, _ in spec['hook_big']], PB, 138, W - 130)
    for s, c in spec['hook_big']: st(d, (64, y), s, big, COL[c], 7); y += int(big.size * 1.09)
    y += 8; mid = fit(d, [s for s, _ in spec['hook_mid']], PB, 76, W - 130)
    for s, c in spec['hook_mid']: st(d, (68, y), s, mid, COL[c], 5); y += int(mid.size * 1.16)
    d.polygon([(70, y + 30), (130, y + 30), (100, y + 75)], fill=LIME)
    im.save(os.path.join(D, 'o0.png'))

def tip_png(i, title, sub):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 360, 1150, 175); d = ImageDraw.Draw(im)
    num = F(PB, 150); s = f'{i}/{N}'; w = d.textlength(s, font=num)
    d.rectangle((64, 400, 64 + w + 48, 590), fill=LIME); d.text((88, 402), s, font=num, fill=BLK)
    tf = F(PB, 104); lines = wrap(d, title, tf, W - 150)
    if len(lines) > 3: tf = F(PB, 88); lines = wrap(d, title, tf, W - 150)
    y = 640
    for line in lines: st(d, (64, y), line, tf, INK, 6); y += int(tf.size * 1.12)
    y += 18; sf = F(PM, 52)
    for line in wrap(d, sub, sf, W - 150): st(d, (68, y), line, sf, CYAN, 4); y += 66
    for k in range(N):
        x = 70 + k * 46; d.rectangle((x, 340, x + 34, 352), fill=LIME if k < i else (255, 255, 255, 110))
    im.save(os.path.join(D, f'o{i}.png'))

def end_png():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 380, 1200, 195); d = ImageDraw.Draw(im)
    s = seal(200); im.paste(s, (70, 400), s)
    bf = fit(d, [spec['end_big']], PB, 150, W - 130); st(d, (64, 640), spec['end_big'], bf, LIME, 7)
    y = 640 + int(bf.size * 1.15); mf = F(PB, 70)
    for line in wrap(d, spec['end_mid'], mf, W - 150): st(d, (68, y), line, mf, INK, 5); y += 82
    y = chip(d, 70, y + 30, spec['end_chip'], F(MONO, 46), INK) + 30
    st(d, (70, y), '@ibizapartyflights', F(PM, 44), CYAN, 4)
    im.save(os.path.join(D, f'o{N+1}.png'))

hook_png()
for i, (t, s) in enumerate(spec['tips'], 1): tip_png(i, t, s)
end_png()

SEG = spec['seg']; assert len(SEG) == N + 2
# Own-graphic backgrounds (no footage): seg src "bg:<variant>" = brand-colour wave pattern scrolling
# at a whole number of pixels per frame (crisp, no Ken Burns). Variants defined in BG below.
import math
BG = {'navy': ((10, 26, 143), (49, 80, 255), 'up'), 'royal': ((49, 80, 255), (10, 26, 143), 'down'),
      'night': ((4, 7, 46), (56, 225, 255), 'left'), 'lime': ((10, 26, 143), (200, 255, 46), 'right'),
      'deep': ((4, 7, 46), (49, 80, 255), 'down')}
def bg_png(v):
    base, line, _ = BG[v]; p = os.path.join(D, f'bg_{v}.png')
    if os.path.exists(p): return p
    im = Image.new('RGB', (W * 2, H * 2), base); d = ImageDraw.Draw(im)
    amp, per, gap, th = 46, 360, 150, 34
    for y0 in range(-gap, H * 2 + gap, gap):
        pts = [(x, y0 + amp * math.sin(2 * math.pi * x / per)) for x in range(0, W * 2 + 8, 8)]
        d.line(pts, fill=line, width=th, joint='curve')
    im.save(p); return p
args = ['ffmpeg', '-v', 'error', '-y']
for src, ss, du, _ in SEG:
    if src.startswith('bg:'): args += ['-loop', '1', '-framerate', '30', '-t', str(du), '-i', bg_png(src[3:])]
    else: args += ['-ss', str(ss), '-t', str(du), '-i', src if src.startswith('/') else CL + src]
for k in range(len(SEG)): args += ['-loop', '1', '-t', str(SEG[k][2]), '-i', os.path.join(D, f'o{k}.png')]
n = len(SEG); fc = []
for k, (src, ss, du, punch) in enumerate(SEG):
    z = "1+0.10*max(0\\,1-t/0.45)" if punch else "1"
    if src.startswith('bg:'):
        dx, dy = {'up': (0, 1), 'down': (0, -1), 'left': (1, 0), 'right': (-1, 0)}[BG[src[3:]][2]]
        sp = 6  # px per frame, integer
        cx = f"mod(n*{sp},360)" if dx > 0 else (f"360-mod(n*{sp},360)" if dx < 0 else "0")
        cy = f"mod(n*{sp},150)" if dy > 0 else (f"150-mod(n*{sp},150)" if dy < 0 else "0")
        fc.append(f"[{k}:v]fps=30,crop=1080:1920:'{cx}':'{cy}',setsar=1[v{k}];"
                  f"[{n+k}:v]format=rgba,fps=30[t{k}];[v{k}][t{k}]overlay=0:0:shortest=1,format=yuv420p[s{k}]")
        continue
    fc.append(f"[{k}:v]setpts=PTS-STARTPTS,fps=30,scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':force_original_aspect_ratio=increase:eval=frame,"
              f"crop=1080:1920,eq=contrast=1.08:saturation=1.15,setsar=1[v{k}];"
              f"[{n+k}:v]format=rgba,fps=30[t{k}];[v{k}][t{k}]overlay=0:0:shortest=1,format=yuv420p[s{k}]")
fc.append(''.join(f'[s{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=0[out]')
args += ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
         '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', os.path.join(D, spec['name'] + '_tiktok.mp4')]
subprocess.run(args, check=True)
print('done', spec['name'])
