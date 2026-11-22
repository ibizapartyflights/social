#!/usr/bin/env python3
"""Own-graphic moving backgrounds in brand colours (alternative to the wave pattern and the island map).
Usage: python3 tools/kinetic_bg.py <style> <variant> <seconds> out.mp4 [WORD]
styles:
  type  - rows of huge words scrolling in alternate directions (outline/filled, one accent row)
  sun   - the brand's striped sun: big circle with stripes sliding down through it, rings pulsing
variants: navy | royal | night | lime | cyan  (which accent colour leads)
Integer px per frame (crisp), no zoom/Ken Burns. 1080x1920, 30 fps, yuv420p, no audio."""
import sys, subprocess, math
from PIL import Image, ImageDraw, ImageFont

style, var, dur, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
word = (sys.argv[5] if len(sys.argv) > 5 else 'IBIZA').upper()
W, H, FPS = 1080, 1920, 30
NIGHT, DEEP, ROYAL, LIME, CYAN = (4, 7, 46), (10, 26, 143), (49, 80, 255), (200, 255, 46), (56, 225, 255)
ACC = {'navy': ROYAL, 'royal': CYAN, 'night': ROYAL, 'lime': LIME, 'cyan': CYAN}[var]
BASE = {'navy': DEEP, 'royal': ROYAL, 'night': NIGHT, 'lime': NIGHT, 'cyan': NIGHT}[var]
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
N = int(round(dur * FPS))

def strip(text, size, fill, outline, sw, bg):
    f = ImageFont.truetype(PB, size); unit = text + '  •  '
    d0 = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    uw = int(d0.textlength(unit, font=f)); reps = W // uw + 3
    im = Image.new('RGB', (uw * reps, int(size * 1.18)), bg); d = ImageDraw.Draw(im)
    for r in range(reps):
        d.text((r * uw, -int(size * .12)), unit, font=f, fill=fill, stroke_width=sw, stroke_fill=outline)
    return im, uw

frames_cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
              '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
p = subprocess.Popen(frames_cmd, stdin=subprocess.PIPE)

if style == 'type':
    size = 250; rows = []
    k = 0; y = -60
    while y < H:
        accent = (k % 4 == 2)
        if accent: im, uw = strip(word, size, BASE, ACC, 5, BASE)            # outline in accent colour
        elif k % 2: im, uw = strip(word, size, DEEP if BASE != DEEP else ROYAL, DEEP, 0, BASE)  # filled, tone-on-tone
        else: im, uw = strip(word, size, BASE, ROYAL if BASE != ROYAL else DEEP, 4, BASE)       # outline, tone-on-tone
        rows.append((im, uw, y, 1 if k % 2 else -1, 3 + (k % 3)))
        y += im.height - 10; k += 1
    for n in range(N):
        fr = Image.new('RGB', (W, H), BASE)
        for im, uw, y, dr, sp in rows:
            off = (n * sp) % uw
            x = -off if dr < 0 else -(uw - off)
            fr.paste(im, (x, y))
        p.stdin.write(fr.tobytes())
elif style == 'sun':
    R = 820; cx, cy = W // 2, int(H * .72)
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).ellipse((cx - R // 2 * 1, cy - R // 2, cx + R // 2, cy + R // 2), fill=255)
    gap, th = 70, 38
    for n in range(N):
        fr = Image.new('RGB', (W, H), BASE); d = ImageDraw.Draw(fr)
        # pulsing rings (integer radius steps)
        for i in range(6):
            r = (R // 2 + 40 + i * 110 + (n * 3) % 110)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=DEEP if BASE != DEEP else ROYAL, width=6)
        sun = Image.new('RGB', (W, H), ACC); sd = ImageDraw.Draw(sun)
        off = (n * 2) % gap
        for yy in range(cy - R // 2 - gap + off, cy + R // 2 + gap, gap):
            t = max(0, (yy - (cy - R // 2)) / R)          # stripes thicken towards the bottom (sunset)
            sd.rectangle((0, yy, W, yy + int(6 + th * t)), fill=BASE)
        fr.paste(sun, (0, 0), mask)
        p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait()
print('bg', style, var, out)
