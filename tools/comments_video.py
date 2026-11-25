#!/usr/bin/env python3
""""Hot take + comment reactions" reel: each scene shows a statement and 3 comment bubbles popping in (own graphics only).
Usage: python3 tools/comments_video.py spec.json out_dir
Spec: {"name", "chip", "hook_big": [lines], "hook_mid", "items": [[label, statement, [[name, text], x3]], ...],
       "end_big", "end_mid", "end_chip", "note" (small, e.g. "Comments dramatised"), "bg": [mp4 per scene (items + 2)]}
Durations: hook 2.3 s, items 2.6 s, end 2.6 s. Text visible from frame 0 (hook). Bubbles slide up by whole pixels. No audio."""
import subprocess, os, sys, json, unicodedata
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = json.load(open(sys.argv[1])); D = sys.argv[2]; os.makedirs(D, exist_ok=True)
W, H = 1080, 1920
NIGHT, DEEP, ROYAL, LIME, CYAN, INK, BLK = (4, 7, 46), (10, 26, 143), (49, 80, 255), (200, 255, 46), (56, 225, 255), (255, 255, 255), (0, 0, 0)
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
PM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
F = ImageFont.truetype
N = len(spec['items']); DUR = [2.3] + [2.6] * N + [2.6]
T_IN = [0.30, 0.95, 1.60]  # bubble appear times

def is_emo(ch): return ord(ch) > 0x2100 and unicodedata.category(ch) in ('So', 'Sk', 'Mn', 'Cf') or ord(ch) >= 0x1F000
def tokens(s):  # group grapheme-ish runs: emoji (with variation selectors / ZWJ) vs text
    out, cur, emo = [], '', None
    for ch in s:
        e = bool(is_emo(ch) or (emo and ch in '\ufe0f\u200d'))
        if emo is None or e == emo: cur += ch
        else: out.append((cur, emo)); cur = ch
        emo = e
    if cur: out.append((cur, emo))
    return out
def emoji_img(e, size):
    im = Image.new('RGBA', (140 * len(e), 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((0, 0), e, font=EMO, embedded_color=True); bb = im.getbbox() or (0, 0, 1, 1); im = im.crop(bb)
    return im.resize((max(1, int(im.width * size / 128)), max(1, int(im.height * size / 128))), Image.LANCZOS)
def tlen(d, s, font):
    return sum(d.textlength(t, font=font) if not e else emoji_img(t, font.size).width + 6 for t, e in tokens(s))
def draw_rich(im, d, xy, s, font, fill, sw=0):
    x, y = xy
    for t, e in tokens(s):
        if e:
            ei = emoji_img(t, font.size); im.alpha_composite(ei, (int(x) + 3, int(y + font.size * 0.18))); x += ei.width + 6
        else:
            d.text((x, y), t, font=font, fill=fill, stroke_width=sw, stroke_fill=BLK); x += d.textlength(t, font=font)
def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if tlen(d, t, font) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines
def chip(d, x, y, s, font, bg, fg=BLK, pad=(18, 10)):
    w = d.textlength(s, font=font); h = font.size
    d.rounded_rectangle((x, y, x + w + pad[0] * 2, y + h + pad[1] * 2), 8, fill=bg); d.text((x + pad[0], y + pad[1] - 2), s, font=font, fill=fg)
    return y + h + pad[1] * 2
def seal(size):
    im = Image.open(os.path.join(ROOT, 'assets/brand/perfil_sello_oscuro.png')).convert('RGBA').resize((size, size), Image.LANCZOS)
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255); im.putalpha(m); return im
def panel(im, box, a=200, col=NIGHT):
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle(box, 36, fill=col + (a,)); im.alpha_composite(ov)
def progress(d, i):
    seg = (W - 140 - (N - 1) * 10) / N
    for k in range(N):
        x = 70 + k * (seg + 10); d.rounded_rectangle((x, 120, x + seg, 130), 5, fill=LIME if k < i else (255, 255, 255, 120))
def blank(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))

AV = [LIME, CYAN, (255, 138, 92), (255, 61, 139), ROYAL]
def bubble(k, name, text, y, side):
    im = blank(); d = ImageDraw.Draw(im); tf = F(PM, 44); nf = F(PB, 34)
    maxw = 640; lines = wrap(d, text, tf, maxw); bw = max(tlen(d, l, tf) for l in lines + [name]) + 70; bh = 70 + 58 * len(lines)
    x = 150 if side == 0 else W - 70 - bw
    ax = 70 if side == 0 else None
    col = AV[sum(map(ord, name)) % len(AV)]
    if side == 0:
        d.ellipse((60, y + 6, 130, y + 76), fill=col); d.text((95, y + 41), name[0], font=F(PB, 38), fill=BLK, anchor='mm')
    else:
        x = W - 150 - bw; d.ellipse((W - 130, y + 6, W - 60, y + 76), fill=col); d.text((W - 95, y + 41), name[0], font=F(PB, 38), fill=BLK, anchor='mm')
    d.rounded_rectangle((x, y, x + bw, y + bh), 34, fill=(255, 255, 255, 245))
    tail = [(x + 10, y + 30), (x - 18, y + 52), (x + 26, y + 50)] if side == 0 else [(x + bw - 10, y + 30), (x + bw + 18, y + 52), (x + bw - 26, y + 50)]
    d.polygon(tail, fill=(255, 255, 255, 245))
    d.text((x + 35, y + 16), name, font=nf, fill=ROYAL)
    for j, l in enumerate(lines): draw_rich(im, d, (x + 35, y + 56 + 58 * j), l, tf, NIGHT)
    return im, bh

def hook():
    im = blank(); d = ImageDraw.Draw(im); panel(im, (40, 330, W - 40, 1240), 175); d = ImageDraw.Draw(im)
    y = chip(d, 80, 380, spec['chip'], F(MONO, 38), LIME) + 30
    sz = 150
    while sz > 60 and any(d.textlength(s, font=F(PB, sz)) > W - 170 for s in spec['hook_big']): sz -= 4
    for s in spec['hook_big']: d.text((74, y), s, font=F(PB, sz), fill=INK, stroke_width=6, stroke_fill=BLK); y += int(sz * 1.02)
    y += 16
    for s in wrap(d, spec['hook_mid'], F(PB, 64), W - 170): draw_rich(im, d, (78, y), s, F(PB, 64), LIME, 4); y += 78
    # teaser bubble already visible on frame 0
    b, _ = bubble(0, spec.get('hook_teaser', ['Jess', 'nah you did NOT just say that 😭'])[0], spec.get('hook_teaser', ['Jess', 'nah you did NOT just say that 😭'])[1], y + 40, 1)
    im.alpha_composite(b); im.save(os.path.join(D, 's0_base.png'))
    return []

def item(i, label, statement, comments):
    im = blank(); d = ImageDraw.Draw(im); progress(d, i)
    tf = F(PB, 100); lines = wrap(d, statement, tf, W - 170)
    if len(lines) > 2: tf = F(PB, 84); lines = wrap(d, statement, tf, W - 170)
    top = 200; ph = 150 + int(tf.size * 1.05) * len(lines)
    panel(im, (40, top, W - 40, top + ph), 205); d = ImageDraw.Draw(im)
    chip(d, 80, top + 36, f'{label} {i:02d}/{N:02d}', F(MONO, 40), LIME)
    y = top + 112
    for l in lines: d.text((76, y), l, font=tf, fill=INK); y += int(tf.size * 1.05)
    ei = emoji_img('🗣️', 90); im.alpha_composite(ei, (W - 80 - ei.width, top + 24))
    im.save(os.path.join(D, f's{i}_base.png'))
    y = top + ph + 70; layers = []
    for k, (name, text) in enumerate(comments):
        b, bh = bubble(k, name, text, y, k % 2); p = os.path.join(D, f's{i}_c{k}.png'); b.save(p); layers.append((p, T_IN[k])); y += bh + 46
    return layers

def end():
    k = N + 1; im = blank(); d = ImageDraw.Draw(im); panel(im, (40, 330, W - 40, 1300), 190); d = ImageDraw.Draw(im)
    sl = seal(200); im.alpha_composite(sl, (80, 380))
    y = 620; sz = 140
    while sz > 60 and d.textlength(spec['end_big'], font=F(PB, sz)) > W - 170: sz -= 4
    d.text((74, y), spec['end_big'], font=F(PB, sz), fill=LIME, stroke_width=6, stroke_fill=BLK); y += int(sz * 1.15)
    for s in wrap(d, spec['end_mid'], F(PB, 62), W - 170): draw_rich(im, d, (78, y), s, F(PB, 62), INK, 4); y += 76
    y = chip(d, 80, y + 30, spec['end_chip'], F(MONO, 42), INK) + 26
    d.text((80, y), '@ibizapartyflights', font=F(PM, 46), fill=CYAN, stroke_width=3, stroke_fill=BLK)
    if spec.get('note'): d.text((80, 1240), spec['note'], font=F(PM, 28), fill=(255, 255, 255, 190))
    im.save(os.path.join(D, f's{k}_base.png')); return []

scenes = [hook()] + [item(i, spec['label'], s, c) for i, (s, c) in enumerate(spec['items'], 1)] + [end()]
args = ['ffmpeg', '-v', 'error', '-y']; idx = 0; fc = []; n = len(scenes)
for k in range(n):
    args += ['-t', str(DUR[k]), '-i', spec['bg'][k]]; b = idx; idx += 1
    args += ['-loop', '1', '-framerate', '30', '-t', str(DUR[k]), '-i', os.path.join(D, f's{k}_base.png')]; base = idx; idx += 1
    chain = f"[{b}:v]fps=30,setpts=PTS-STARTPTS,format=yuv420p,setsar=1[r{k}];[r{k}][{base}:v]overlay=0:0[c{k}_0]"
    for j, (p, t0) in enumerate(scenes[k]):
        args += ['-loop', '1', '-framerate', '30', '-t', str(DUR[k]), '-i', p]; li = idx; idx += 1
        f0 = int(t0 * 30)
        chain += (f";[c{k}_{j}][{li}:v]overlay=x=0:y='if(lt(n\\,{f0})\\,{H}\\,max(0\\,48-trunc((n-{f0})*48/6)))'"
                  f":enable='gte(n\\,{f0})'[c{k}_{j+1}]")
    chain += f";[c{k}_{len(scenes[k])}]format=yuv420p[s{k}]"; fc.append(chain)
fc.append(''.join(f'[s{k}]' for k in range(n)) + f'concat=n={n}:v=1:a=0[out]')
args += ['-filter_complex', ';'.join(fc), '-map', '[out]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
         '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', os.path.join(D, spec['name'] + '_tiktok.mp4')]
subprocess.run(args, check=True); print('done', spec['name'])
