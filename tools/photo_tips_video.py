#!/usr/bin/env python3
"""Modern "editorial" tips reel over full-bleed photos (Instagram ONLY when photos are Unsplash; TikTok only with own photos).
Usage: python3 tools/photo_tips_video.py spec.json out_dir
Spec: {"name", "chip", "hook_big": [..lines..], "hook_mid": "...", "hook_photo": path,
       "tips": [[title, sub, tag, photo], ...], "end_big", "end_mid", "end_chip", "end_photo": path,
       "credit": "Photos: ... / Unsplash" (optional, small text on end card)}
Static photos (no zoompan / Ken Burns), crisp 1080x1920 lanczos crop; text slides in (integer px), hook visible from frame 0.
Cuts: hook 2.3 s, tips 1.9 s, end 2.6 s. Output <name>_tiktok.mp4 (no audio)."""
import subprocess, os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = json.load(open(sys.argv[1])); D = sys.argv[2]; os.makedirs(D, exist_ok=True)
W, H = 1080, 1920
NIGHT, DEEP, ROYAL, LIME, CYAN, INK, BLK = (4, 7, 46), (10, 26, 143), (49, 80, 255), (200, 255, 46), (56, 225, 255), (255, 255, 255), (0, 0, 0)
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
PM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
F = ImageFont.truetype
N = len(spec['tips'])
DY = -640 if spec.get('layout') == 'top' else 0  # 'top': text over the sky, for scene videos from beach_scene_bg.py
DUR = [2.3] + [1.9] * N + [2.6]

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def fit_lines(d, text, path, size, maxw, maxl):
    while size > 40:
        f = F(path, size); ls = wrap(d, text, f, maxw)
        if len(ls) <= maxl and all(d.textlength(s, font=f) <= maxw for s in ls): return f, ls
        size -= 4
    f = F(path, size); return f, wrap(d, text, f, maxw)

def st(d, xy, s, font, fill, sw=5): d.text(xy, s, font=font, fill=fill, stroke_width=sw, stroke_fill=BLK)

def photo_bg(path, k):
    im = ImageOps.fit(Image.open(path).convert('RGB'), (W, H), Image.LANCZOS, centering=(0.5, 0.45))
    # brand grade: slight contrast + night-blue gradient bottom 60 %, light top shade for the progress bar
    g = Image.new('L', (1, H))
    for y in range(H):
        t = max(0.0, (y - H * 0.38) / (H * 0.62)); top = max(0.0, (260 - y) / 260)
        g.putpixel((0, y), int(255 * min(1, 0.92 * t ** 1.15 + 0.45 * top)))
    im = Image.composite(Image.new('RGB', (W, H), NIGHT), im, g.resize((W, H)))
    p = os.path.join(D, f'bg{k}.png'); im.save(p); return p

def seal(size):
    im = Image.open(os.path.join(ROOT, 'assets/brand/perfil_sello_oscuro.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255); im.putalpha(m); return im

def progress(d, i):
    seg = (W - 140 - (N - 1) * 10) / N
    for k in range(N):
        x = 70 + k * (seg + 10); d.rounded_rectangle((x, 120, x + seg, 130), 5, fill=LIME if k < i else (255, 255, 255, 120))

def chip(d, x, y, s, font, bg, fg=BLK, pad=(18, 10)):
    w = d.textlength(s, font=font); h = font.size
    d.rounded_rectangle((x, y, x + w + pad[0] * 2, y + h + pad[1] * 2), 8, fill=bg); d.text((x + pad[0], y + pad[1] - 2), s, font=font, fill=fg)
    return y + h + pad[1] * 2

# layers: static = drawn from frame 0; slide = slides up 60 px over 8 frames (integer px)
def hook():
    a = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(a)
    y = 1010 + DY; y = chip(d, 70, y, spec['chip'], F(MONO, 38), LIME) + 26
    ls, sz = spec['hook_big'], 150
    while sz > 60 and any(d.textlength(s, font=F(PB, sz)) > W - 140 for s in ls): sz -= 4
    big = F(PB, sz)
    for s in ls: st(d, (64, y), s, big, INK, 7); y += int(big.size * 1.02)
    y += 14; mf = F(PB, 62)
    for s in wrap(d, spec['hook_mid'], mf, W - 140): st(d, (68, y), s, mf, LIME, 5); y += 74
    a.save(os.path.join(D, 'a0.png')); Image.new('RGBA', (W, H), (0, 0, 0, 0)).save(os.path.join(D, 'b0.png'))

def tip(i, title, sub, tag):
    a = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(a); progress(d, i)
    nf = F(PB, 300); s = f'{i:02d}'
    d.text((52, 820 + DY + (80 if DY else 0)), s, font=nf, fill=(0, 0, 0, 0), stroke_width=4, stroke_fill=LIME)
    a.save(os.path.join(D, f'a{i}.png'))
    b = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    y = chip(d, 70, 1180 + DY + (60 if DY else 0), tag, F(MONO, 36), CYAN) + 24
    tf, ls = fit_lines(d, title, PB, 118, W - 140, 2)
    for s2 in ls: st(d, (64, y), s2, tf, INK, 6); y += int(tf.size * 1.06)
    y += 12; sf = F(PM, 50)
    for s2 in wrap(d, sub, sf, W - 150): st(d, (68, y), s2, sf, INK, 4); y += 64
    d.rectangle((70, y + 20, 190, y + 30), fill=LIME)
    b.save(os.path.join(D, f'b{i}.png'))

def end():
    k = N + 1; a = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(a)
    sl = seal(210); a.paste(sl, (70, 880 + DY), sl)
    bf, ls = fit_lines(d, spec['end_big'], PB, 140, W - 140, 2); y = 1120 + DY
    for s in ls: st(d, (64, y), s, bf, LIME, 7); y += int(bf.size * 1.04)
    mf = F(PB, 62)
    for s in wrap(d, spec['end_mid'], mf, W - 150): st(d, (68, y), s, mf, INK, 5); y += 76
    y = chip(d, 70, y + 24, spec['end_chip'], F(MONO, 42), INK) + 24
    st(d, (70, y), '@ibizapartyflights', F(PM, 46), CYAN, 4)
    if spec.get('credit'): d.text((70, H - 120), spec['credit'], font=F(PM, 26), fill=(255, 255, 255, 170))
    a.save(os.path.join(D, f'a{k}.png')); Image.new('RGBA', (W, H), (0, 0, 0, 0)).save(os.path.join(D, f'b{k}.png'))

hook()
for i, (t, s, tag, _) in enumerate(spec['tips'], 1): tip(i, t, s, tag)
end()
def video_bg(path, k):
    # top shade (night blue) behind the text block for scene videos
    g = Image.new('L', (1, H))
    for y in range(H): g.putpixel((0, y), int(165 * max(0.0, min(1.0, (1000 - y) / 650)) ** 0.9))
    m = Image.new('RGBA', (W, H), NIGHT + (0,)); m.putalpha(g.resize((W, H)))
    p = os.path.join(D, f'shade{k}.png'); m.save(p); return path, p
photos = [spec['hook_photo']] + [t[3] for t in spec['tips']] + [spec['end_photo']]
photos = [p if p.startswith('/') else os.path.join(ROOT, p) for p in photos]
bgs = [video_bg(p, k) if p.endswith('.mp4') else (photo_bg(p, k), None) for k, p in enumerate(photos)]
n = len(bgs); args = ['ffmpeg', '-v', 'error', '-y']
for k in range(n):
    src, sh = bgs[k]
    if sh: args += ['-t', str(DUR[k]), '-i', src]
    else: args += ['-loop', '1', '-framerate', '30', '-t', str(DUR[k]), '-i', src]
    for o in (sh or os.path.join(D, 'none.png'), os.path.join(D, f'a{k}.png'), os.path.join(D, f'b{k}.png')):
        args += ['-loop', '1', '-framerate', '30', '-t', str(DUR[k]), '-i', o]
Image.new('RGBA', (W, H), (0, 0, 0, 0)).save(os.path.join(D, 'none.png'))
fc = []
for k in range(n):
    b, h, a, s = 4 * k, 4 * k + 1, 4 * k + 2, 4 * k + 3
    fc.append(f"[{b}:v]fps=30,setpts=PTS-STARTPTS,format=yuv420p,setsar=1[r{k}];[r{k}][{h}:v]overlay=0:0[p{k}];[p{k}][{a}:v]overlay=0:0[q{k}];"
              f"[q{k}][{s}:v]overlay=x=0:y='max(0\\,60-trunc(n*60/8))',format=yuv420p[s{k}]")
fc.append(''.join(f'[s{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=0[out]')
args += ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
         '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', os.path.join(D, spec['name'] + '_tiktok.mp4')]
subprocess.run(args, check=True)
print('done', spec['name'])
