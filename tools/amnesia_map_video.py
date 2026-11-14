#!/usr/bin/env python3
"""TikTok: "Amnesia Ibiza 2026 -> 2027: 4 things first-timers ask" on our own radar map (hook visible on frame 0),
end on Rubén's footage. Only own material (no stock, no club logos). Usage: python3 tools/amnesia_map_video.py out_dir
Output: reel_amnesia_tiktok.mp4 (no audio)."""
import sys
import subprocess, os, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = sys.argv[1].rstrip('/') + '/'; os.makedirs(D, exist_ok=True)
W, H = 1080, 1920
LIME, CYAN, INK, BLK = (200, 255, 46), (56, 225, 255), (255, 255, 255), (0, 0, 0)
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
PM = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
F = ImageFont.truetype
CL = '/home/claude/social/assets/clips/'
SEAL = '/home/claude/social/assets/brand/perfil_sello_oscuro.png'

# ---- steps (general, well-established facts only; no 2027 dates) ----
FACTS = [
  dict(n=0, t="AMNESIA IBIZA 2026 → 2027", s="4 things first-timers ask", lat=38.995, lon=1.420, tag='IBIZA'),
  dict(n=1, t="Where is it?", s="San Rafael, right in the middle of the island", lat=38.948, lon=1.409, tag='SANT RAFEL'),
  dict(n=2, t="Close to both party towns", s="A short ride from San Antonio and Ibiza Town", lat=38.980, lon=1.303, tag='SANT ANTONI'),
  dict(n=3, t="Two rooms, two vibes", s="The Main Room and the Terrace", lat=38.948, lon=1.409, tag='SANT RAFEL'),
  dict(n=4, t="2027 dates?", s="Not announced yet. Openings usually land late April–May", lat=38.948, lon=1.409, tag='SANT RAFEL'),
]
# ---- map page built from the site's island geometry ----
code = open('/home/claude/social/tools/web/mapbuild.py', encoding='utf-8').read()
ns = {}; exec(code[:code.index('def pin(')], ns)
P, ISLAND, ISLETS, cx, cy, MW, MH = (ns[k] for k in ('P', 'ISLAND', 'ISLETS', 'cx', 'cy', 'W', 'H'))
for f in FACTS: f['x'], f['y'] = P(f['lat'], f['lon'])
grid = ''.join(f'<line x1="{x}" y1="-200" x2="{x}" y2="{MH+200}"/>' for x in range(-60, MW + 120, 40)) + \
       ''.join(f'<line x1="-100" y1="{y}" x2="{MW+100}" y2="{y}"/>' for y in range(-200, MH + 220, 40))
rings = ''.join(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}"/>' for r in (80, 160, 240, 320, 400))
contours = ''.join(f'<use href="#isl" transform="translate({cx*(1-s):.1f},{cy*(1-s):.1f}) scale({s})" opacity="{o}"/>' for s, o in ((.86,.5),(.7,.4),(.52,.32),(.34,.25)))
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{font-family:Poppins,sans-serif;color:#fff;background:radial-gradient(ellipse 90% 55% at 45% 55%,#0A1A8F 0%,#071270 45%,#04072E 100%)}}
#top{{position:absolute;left:64px;right:64px;top:330px}}
.prog{{display:flex;gap:12px;margin-bottom:30px}}.prog i{{display:block;width:34px;height:12px;background:rgba(255,255,255,.35)}}.prog i.on{{background:#C8FF2E}}
.num{{display:inline-block;background:#C8FF2E;color:#000;font:800 120px Poppins;line-height:1;padding:14px 28px 6px}}
h1{{font:800 96px/1.04 Poppins;text-transform:uppercase;margin-top:26px;letter-spacing:-.01em}}
.sub{{font:600 46px/1.25 Poppins;color:#38E1FF;margin-top:18px}}
#map{{position:absolute;left:-20px;top:850px;width:1100px}}
svg{{display:block;width:100%;height:auto;overflow:visible}}
.seagrid line{{stroke:#38E1FF;stroke-opacity:.08;stroke-width:.8}}.rings circle{{fill:none;stroke:#38E1FF;stroke-opacity:.14;stroke-dasharray:2 7}}
.shadow{{fill:#000;opacity:.4}}.coast{{fill:none;stroke:#38E1FF;stroke-width:1.8}}.contours use{{fill:none;stroke:#C8FF2E;stroke-width:.9}}
.islets ellipse{{fill:#3150FF;fill-opacity:.5;stroke:#38E1FF;stroke-width:1}}
#mk rect{{fill:#C8FF2E;stroke:#04072E;stroke-width:2}}#mk circle{{fill:none;stroke:#C8FF2E;stroke-width:2}}
#mk text{{font:700 17px 'DejaVu Sans Mono',monospace;fill:#fff;paint-order:stroke;stroke:#04072E;stroke-width:5px;stroke-linejoin:round}}
#cross line{{stroke:#C8FF2E;stroke-opacity:.5;stroke-width:1;stroke-dasharray:3 5}}
#ro{{position:absolute;left:64px;top:1790px;font:700 30px 'DejaVu Sans Mono',monospace;color:#C8FF2E}}
</style></head><body>
<div id="top"><div class="prog" id="prog"><i></i><i></i><i></i><i></i></div><span class="num" id="num">1/4</span><h1 id="t"></h1><div class="sub" id="s"></div></div>
<div id="map"><svg viewBox="0 0 {MW} {MH}"><defs><path id="isl" d="{ISLAND}"/><clipPath id="ic"><use href="#isl"/></clipPath>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3150FF" stop-opacity=".6"/><stop offset=".55" stop-color="#0A1A8F" stop-opacity=".8"/><stop offset="1" stop-color="#7B3CFF" stop-opacity=".55"/></linearGradient>
<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#38E1FF" fill-opacity=".35"/></pattern>
<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C8FF2E" stop-opacity="0"/><stop offset="1" stop-color="#C8FF2E" stop-opacity=".4"/></linearGradient>
<filter id="gl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g class="seagrid">{grid}</g><g class="rings">{rings}</g>
<use href="#isl" class="shadow" transform="translate(0,10)"/><use href="#isl" fill="url(#g)"/>
<g clip-path="url(#ic)"><rect width="{MW}" height="{MH}" fill="url(#dots)"/><g class="contours">{contours}</g>
<g id="sweep" style="transform-origin:{cx:.0f}px {cy:.0f}px"><path d="M{cx:.0f},{cy:.0f} L{cx+420:.0f},{cy-80:.0f} A428,428 0 0 1 {cx+420:.0f},{cy+80:.0f}Z" fill="url(#sw)"/></g></g>
<use href="#isl" class="coast" filter="url(#gl)"/><g class="islets">{ISLETS}</g>
<g id="cross"><line id="cx" x1="-100" x2="{MW+100}"/><line id="cy" y1="-100" y2="{MH+100}"/></g>
<g id="mk"><circle id="p1" r="10"/><circle id="p2" r="10"/><rect x="-8" y="-8" width="16" height="16" transform="rotate(45)"/><text id="lab" x="16" y="-14"></text></g>
</svg></div><div id="ro"></div>
<script>
const FACTS={json.dumps(FACTS, ensure_ascii=False)};
const e=t=>{{t=Math.max(0,Math.min(1,t));return t*t*(3-2*t)}};
window.render=function(i,t,T){{ // fact index, time within fact, global time
  const f=FACTS[i]; const prev=i?FACTS[i-1]:f; if(i==0){{t=t+0.5}} const k=e(t/.45);
  const x=prev.x+(f.x-prev.x)*k, y=prev.y+(f.y-prev.y)*k;
  document.getElementById('num').textContent=f.n?f.n+'/4':'FIRST-TIMERS';document.getElementById('num').style.fontSize=f.n?'120px':'64px';document.getElementById('t').style.fontSize=f.n?'96px':'118px';document.getElementById('prog').style.visibility=f.n?'visible':'hidden';
  document.getElementById('t').textContent=f.t; document.getElementById('s').textContent=f.s;
  [...document.querySelectorAll('#prog i')].forEach((el,j)=>el.className=j<f.n?'on':'');
  document.getElementById('mk').setAttribute('transform','translate('+x+','+y+')');
  document.getElementById('lab').textContent=f.tag; document.getElementById('lab').setAttribute('text-anchor', f.x>{MW*0.6}?'end':'start');
  document.getElementById('lab').setAttribute('x', f.x>{MW*0.6}?-16:16);
  for(const [id,off] of [['p1',0],['p2',.6]]){{const ph=((t+off)%1.2)/1.2;const c=document.getElementById(id);c.setAttribute('r',8+ph*30);c.style.opacity=1-ph}}
  ['cx','cy'].forEach(id=>{{const l=document.getElementById(id); if(id==='cx'){{l.setAttribute('y1',y);l.setAttribute('y2',y)}}else{{l.setAttribute('x1',x);l.setAttribute('x2',x)}}}});
  document.getElementById('sweep').style.transform='rotate('+(T*72)+'deg)';
  document.getElementById('ro').textContent='> locate '+f.tag.replace(' ','_')+'  '+f.lat.toFixed(3)+'°N '+f.lon.toFixed(3)+'°E';
}};
</script></body></html>'''
open(D + 'map.html', 'w', encoding='utf-8').write(page)

# ---- capture map frames ----
FR = 57  # 1.9 s per fact
js = f'''const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});
await p.goto('file://{D}map.html');await p.waitForTimeout(400);require('fs').mkdirSync('{D}mf',{{recursive:true}});let g=0;
for(let i=0;i<5;i++)for(let f=0;f<(i?{FR}:60);f++){{await p.evaluate(([i,t,T])=>render(i,t,T),[i,f/30,g/30]);await p.screenshot({{path:'{D}mf/'+String(g).padStart(4,'0')+'.jpg',type:'jpeg',quality:93}});g++;}}
await b.close()}})();'''
open(D + 'shoot.js', 'w').write(js)
subprocess.run(['node', D + 'shoot.js'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-i', D + 'mf/%04d.jpg', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', D + 'p1.mp4'], check=True)

# ---- footage parts ----
def shade(im, y0, y1, a=185):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, y0, W, y1), fill=a)
    im.paste(Image.new('RGBA', (W, H), (0, 0, 0, 255)), (0, 0), m.filter(ImageFilter.GaussianBlur(90)))
def st(d, xy, s, font, fill, sw=6): d.text(xy, s, font=font, fill=fill, stroke_width=sw, stroke_fill=BLK)
def chip(d, x, y, s, font, bg, fg=BLK):
    w = d.textlength(s, font=font); d.rectangle((x, y, x + w + 36, y + font.size + 22), fill=bg); d.text((x + 18, y + 8), s, font=font, fill=fg)

im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 330, 1180); d = ImageDraw.Draw(im)
chip(d, 70, 380, 'FRIDAY · 18:00 UK', F(MONO, 42), LIME)
for k, (s, c) in enumerate((("IT'S FRIDAY", INK), ('AND IBIZA', LIME), ('KNOWS IT', INK))):
    st(d, (62, 480 + k * 152), s, F(PB, 140), c, 7)
st(d, (68, 960), "5 things you didn't know", F(PM, 56), CYAN, 4)
st(d, (68, 1030), 'about the island', F(PM, 56), CYAN, 4)
im.save(D + 'o_hook.png')
im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shade(im, 330, 1220, 200); d = ImageDraw.Draw(im)
seal = Image.open(SEAL).convert('RGBA').resize((180, 180), Image.LANCZOS); _m = Image.new('L', (180, 180), 0); ImageDraw.Draw(_m).ellipse((0, 0, 179, 179), fill=255); seal.putalpha(_m); im.paste(seal, (70, 380), seal)
st(d, (62, 590), 'FOLLOW', F(PB, 140), LIME, 7)
st(d, (68, 760), "We'll post the 2027 dates", F(PB, 56), INK, 5); st(d, (68, 840), 'the moment they are confirmed', F(PB, 56), INK, 5)
chip(d, 70, 960, 'IBIZA CLUBS · 2027', F(MONO, 44), INK)
st(d, (70, 1060), '@ibizapartyflights', F(PM, 44), CYAN, 4)
im.save(D + 'o_end.png')

def footage(src, ss, du, png, out, punch=True):
    z = "1+0.10*max(0\\,1-t/0.45)" if punch else "1"
    fc = (f"[0:v]setpts=PTS-STARTPTS,fps=30,scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':force_original_aspect_ratio=increase:eval=frame,"
          f"crop=1080:1920,eq=contrast=1.08:saturation=1.12,setsar=1[v];[1:v]format=rgba,fps=30[t];[v][t]overlay=0:0:shortest=1,format=yuv420p[o]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(du), '-i', src, '-loop', '1', '-t', str(du), '-i', png,
                    '-filter_complex', fc, '-map', '[o]', '-c:v', 'libx264', '-crf', '17', '-r', '30', out], check=True)
footage(CL + 'lasers_cyan_0896.mp4', 52.6, 2.4, D + 'o_end.png', D + 'p2.mp4', punch=False)

open(D + 'list.txt', 'w').write(''.join(f"file '{D}p{i}.mp4'\n" for i in (1, 2)))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', D + 'list.txt', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
                '-r', '30', '-movflags', '+faststart', D + 'reel_amnesia_tiktok.mp4'], check=True)
print('done')
