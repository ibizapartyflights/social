#!/usr/bin/env python3
"""Own animated beach "simulations" (flat travel-poster style, brand colours, no people/characters).
100 % own graphics -> allowed on TikTok. Usage: python3 tools/beach_scene_bg.py <scene> <seconds> out.mp4
scenes: island | spit | longbeach | capelight | village | cliffs | sunset
Motion = waves/boats/sun moving by whole pixels per frame (no zoom / Ken Burns). 1080x1920, 30 fps, yuv420p, no audio.
Horizon sits low (~y 1150) so tips_video.py text (y 340-1150) stays readable over the sky."""
import sys, subprocess, math
from PIL import Image, ImageDraw

scene, dur, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
W, H, FPS = 1080, 1920, 30; N = int(round(dur * FPS))
NIGHT, DEEP, ROYAL, LIME, CYAN = (4, 7, 46), (10, 26, 143), (49, 80, 255), (200, 255, 46), (56, 225, 255)
SAND, SAND2, WHITE, ORANGE, PINK = (244, 227, 200), (226, 200, 160), (250, 250, 255), (232, 88, 42), (255, 138, 92)
TURQ, TURQ2, GREEN, ROCK = (40, 200, 220), (110, 230, 235), (60, 130, 70), (150, 120, 95)

def grad(top, bot, h=H):
    im = Image.new('RGB', (1, h))
    for y in range(h):
        t = y / (h - 1); im.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return im.resize((W, h))

def sun(d, cx, cy, r, col, sky):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
    for k in range(5):  # brand striped sun
        y = cy + r * 0.15 + k * r * 0.17; d.rectangle((cx - r, y, cx + r, y + r * 0.07), fill=sky)

def waves(d, y0, y1, col, f, sp=2, gap=46, amp=7, per=240, th=5):
    off = (f * sp) % per
    for i, y in enumerate(range(y0, y1, gap)):
        o = off if i % 2 == 0 else per - off
        pts = [(x, y + amp * math.sin(2 * math.pi * (x + o) / per)) for x in range(-20, W + 30, 10)]
        d.line(pts, fill=col, width=th)

def boat(d, x, y, s=1.0, sail=WHITE):
    d.polygon([(x - 40 * s, y), (x + 40 * s, y), (x + 28 * s, y + 16 * s), (x - 28 * s, y + 16 * s)], fill=WHITE)
    d.polygon([(x - 4 * s, y - 6 * s), (x - 4 * s, y - 90 * s), (x + 34 * s, y - 6 * s)], fill=sail)
    d.line([(x - 4 * s, y), (x - 4 * s, y - 95 * s)], fill=NIGHT, width=max(2, int(3 * s)))

def lighthouse(d, x, base, h, beam_on):
    w = h * 0.22
    d.polygon([(x - w / 2, base), (x + w / 2, base), (x + w * 0.32, base - h), (x - w * 0.32, base - h)], fill=WHITE)
    for k in range(2): yy = base - h * (0.35 + 0.3 * k); d.rectangle((x - w / 2, yy, x + w / 2, yy + h * 0.07), fill=ROYAL)
    d.rectangle((x - w * 0.36, base - h - h * 0.16, x + w * 0.36, base - h), fill=LIME if beam_on else WHITE)
    d.polygon([(x - w * 0.42, base - h - h * 0.16), (x + w * 0.42, base - h - h * 0.16), (x, base - h - h * 0.3)], fill=NIGHT)

HZ = 1150
day_sky = grad(ROYAL, CYAN, HZ)
dusk_sky = grad(NIGHT, ORANGE, HZ)

def frame(f):
    t = f / FPS
    im = Image.new('RGB', (W, H), DEEP); d = ImageDraw.Draw(im)
    if scene == 'island':  # aerial: island with turquoise rings
        im.paste(grad(DEEP, NIGHT), (0, 0)); d = ImageDraw.Draw(im)
        waves(d, 40, H, (30, 60, 190), f, sp=1, gap=60, amp=8)
        cx, cy = 540, 1450
        for r, c in ((430, TURQ), (360, TURQ2), (300, SAND)): d.ellipse((cx - r * 1.25, cy - r * 0.62, cx + r * 1.25, cy + r * 0.62), fill=c)
        d.ellipse((cx - 300, cy - 130, cx + 260, cy + 120), fill=GREEN); d.ellipse((cx - 120, cy - 60, cx + 200, cy + 90), fill=(80, 160, 80))
        ring = (f * 2) % 120
        d.ellipse((cx - 540 - ring, cy - 270 - ring // 2, cx + 540 + ring, cy + 270 + ring // 2), outline=CYAN, width=3)
        boat(d, 160 + (f * 2) % 900, 1880 - 0, 0.6)
    elif scene == 'spit':  # long thin sand spit, water both sides
        im.paste(day_sky, (0, 0)); d = ImageDraw.Draw(im); sun(d, 820, 520, 120, LIME, day_sky.getpixel((0, 520)))
        d.rectangle((0, HZ, W, H), fill=TURQ); waves(d, HZ + 30, H, TURQ2, f, gap=55)
        d.polygon([(W * 0.35, H), (W * 0.62, H), (W * 0.5, HZ + 10), (W * 0.47, HZ + 10)], fill=SAND)
        d.polygon([(W * 0.42, H), (W * 0.55, H), (W * 0.495, HZ + 40)], fill=SAND2)
        bob = int(4 * math.sin(t * 3)); boat(d, 210, 1330 + bob, 0.9); boat(d, 880, 1260 - bob, 0.6, CYAN)
    elif scene == 'longbeach':  # long curved beach, foam line moving in/out
        im.paste(day_sky, (0, 0)); d = ImageDraw.Draw(im); sun(d, 260, 560, 110, LIME, day_sky.getpixel((0, 560)))
        d.rectangle((0, HZ, W, H), fill=ROYAL); waves(d, HZ + 20, 1500, CYAN, f, gap=50)
        sw = int(18 * math.sin(t * 2.2))
        pts = [(x, 1480 + 120 * math.sin(x / 700) + sw) for x in range(0, W + 20, 20)]
        d.polygon(pts + [(W, H), (0, H)], fill=SAND)
        d.line(pts, fill=WHITE, width=10)
        d.polygon([(0, 1650), (W, 1580), (W, H), (0, H)], fill=SAND2)
    elif scene == 'capelight':  # lighthouse on flat cliffs at sunset
        im.paste(dusk_sky, (0, 0)); d = ImageDraw.Draw(im)
        sy = 900 + (f // 3); sun(d, 300, sy, 150, PINK, dusk_sky.getpixel((0, min(sy, HZ - 1))))
        d.rectangle((0, HZ, W, H), fill=NIGHT); waves(d, HZ + 20, H, DEEP, f, gap=45)
        d.polygon([(380, HZ + 60), (W, HZ - 40), (W, H), (300, H)], fill=(40, 30, 60))
        d.polygon([(330, HZ + 140), (W, HZ + 40), (W, HZ + 70), (340, HZ + 170)], fill=(70, 50, 80))
        on = (f // 12) % 2 == 0
        if on: d.polygon([(760, 820), (120, 700), (120, 820)], fill=(255, 240, 180))
        lighthouse(d, 770, HZ - 10, 330, on)
    elif scene == 'village':  # whitewashed square + fortress church
        im.paste(day_sky, (0, 0)); d = ImageDraw.Draw(im); sun(d, 860, 500 - (f // 4), 100, LIME, day_sky.getpixel((0, 480)))
        d.rectangle((0, HZ + 150, W, H), fill=SAND)
        for x, w, h in ((-20, 260, 200), (230, 200, 240), (760, 340, 190)): d.rectangle((x, HZ + 150 - h, x + w, HZ + 150), fill=WHITE)
        d.rectangle((410, HZ - 140, 760, HZ + 150), fill=WHITE)  # church block
        d.rectangle((560, HZ + 20, 610, HZ + 150), fill=NIGHT)
        d.rounded_rectangle((560, HZ - 10, 610, HZ + 50), 25, fill=NIGHT)
        for x in (60, 300, 840, 960): d.rectangle((x, HZ + 40, x + 50, HZ + 100), fill=ROYAL)
        for k in range(14):
            bx = (k * 83 + f * (1 + k % 3)) % (W + 80) - 40; by = HZ + 160 + (k * 37) % 120
            d.ellipse((bx, by, bx + 26, by + 26), fill=(230, 60, 150) if k % 2 else LIME)
        d.rectangle((0, H - 260, W, H), fill=SAND2)
    elif scene == 'cliffs':  # high plateau cliffs + lighthouse, sea far below
        im.paste(day_sky, (0, 0)); d = ImageDraw.Draw(im)
        d.rectangle((0, HZ, W, H), fill=DEEP); waves(d, HZ + 20, H, ROYAL, f, gap=48)
        d.polygon([(520, H), (600, HZ + 10), (W, HZ - 60), (W, H)], fill=ROCK)
        d.polygon([(600, HZ + 10), (W, HZ - 60), (W, HZ - 20), (610, HZ + 40)], fill=GREEN)
        on = (f // 12) % 2 == 0
        if on: d.polygon([(860, 800), (180, 640), (180, 760)], fill=(255, 250, 200))
        lighthouse(d, 870, HZ - 40, 300, on); boat(d, (f * 3) % (W + 200) - 100, 1700, 0.5)
    else:  # sunset sea from a boat
        im.paste(dusk_sky, (0, 0)); d = ImageDraw.Draw(im)
        sy = 880 + f // 2; sun(d, 540, sy, 190, PINK, dusk_sky.getpixel((0, min(sy, HZ - 1))))
        d.rectangle((0, HZ, W, H), fill=NIGHT); waves(d, HZ + 20, H, (60, 40, 110), f, gap=40)
        d.polygon([(0, HZ), (220, HZ - 50), (420, HZ)], fill=(30, 20, 60)); d.polygon([(700, HZ), (980, HZ - 80), (W, HZ - 30), (W, HZ)], fill=(30, 20, 60))
        d.polygon([(0, H), (0, 1700), (W, 1760), (W, H)], fill=(20, 15, 40))
    return im

p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-an', out], stdin=subprocess.PIPE)
for f in range(N): p.stdin.write(frame(f).tobytes())
p.stdin.close(); p.wait(); print('scene', scene, out)
