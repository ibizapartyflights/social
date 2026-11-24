#!/usr/bin/env python3
"""Adds a Christmas layer to the homepage. It switches itself on from 1 Dec to 6 Jan (UK time),
or any day with ?xmas=1 (and off with ?xmas=0). No characters or cartoons: lights, snow, copy.
Usage: xmas.py <index.html>"""
import sys
p = sys.argv[1]
h = open(p, encoding='utf-8').read()
assert 'id="xmas-snow"' not in h, 'already added'

CSS = '''
/* ---- Christmas layer (html.xmas) ---- */
#xmas-snow{position:fixed;inset:0;z-index:3;pointer-events:none;display:none}
.xmas #xmas-snow{display:block}
.xlights{display:none;position:fixed;left:0;right:0;top:0;height:26px;z-index:60;pointer-events:none}
.xmas .xlights{display:block}
.xlights svg{display:block;width:100%;height:26px}
.xlights path{fill:none;stroke:rgba(242,242,242,.35);stroke-width:1}
.xlights circle{filter:drop-shadow(0 0 4px currentColor)}
.xlights .a{color:#C8FF2E;fill:#C8FF2E}.xlights .b{color:#38E1FF;fill:#38E1FF}.xlights .c{color:#FF3D6E;fill:#FF3D6E}
@media (prefers-reduced-motion:no-preference){
  .xlights .a{animation:twA 2.4s ease-in-out infinite}.xlights .b{animation:twA 2.4s ease-in-out .8s infinite}.xlights .c{animation:twA 2.4s ease-in-out 1.6s infinite}
  @keyframes twA{0%,100%{opacity:1}50%{opacity:.25}}
}
.xbadge{display:none}
.xmas .xbadge{display:inline-flex;align-items:center;gap:10px;margin:0 0 14px;padding:7px 12px;background:#C8FF2E;color:#000;font:600 12px var(--mono);letter-spacing:.06em;text-transform:uppercase}
.xmas .xbadge{margin-bottom:10px}
@media (min-width:861px) and (max-height:900px){.xmas .puffy{font-size:clamp(80px,min(16vw,21vh),210px)}}
.xbadge i{width:9px;height:9px;background:#FF3D6E;transform:rotate(45deg);display:block}
.xnote{display:none}
.xmas .xnote{display:block;margin-top:14px;padding:12px 14px;border:1px dashed rgba(200,255,46,.6);font:500 12.5px/1.5 var(--mono);color:#E9FFC0}
.xmas .xnote b{color:#C8FF2E}
.xmas #hero{background:radial-gradient(ellipse 70% 50% at 50% 45%,rgba(255,61,110,.18),transparent 60%),radial-gradient(ellipse 90% 60% at 50% 60%,#2a3fff 0%,#0A1A8F 55%,#06106A 100%)}
.xmas #finale .xfin{display:block}
.xfin{display:none;margin-top:10px;font:600 13px var(--mono);letter-spacing:.08em;color:#C8FF2E;text-transform:uppercase}
'''

LIGHTS = []
n = 26
for k in range(n):
    x = 2 + k * (96 / (n - 1)); y = 10 + (6 if k % 2 else 0)
    LIGHTS.append(f'<circle class="{"abc"[k % 3]}" cx="{x:.2f}%" cy="{y + 6}" r="3.2"/>')
WIRE = 'M0,8 ' + ' '.join(f'Q{(2 + (k - .5) * (96 / (n - 1))):.2f},{20 if k % 2 else 4} {(2 + k * (96 / (n - 1))):.2f},{10 + (6 if k % 2 else 0)}' for k in range(1, n))
# a % path isn't valid in SVG path data, so draw the wire with a viewBox of 0..100
WIRE = 'M0,9 ' + ' '.join(f'Q{(2 + (k - .5) * (96 / (n - 1))):.2f},{19 if k % 2 else 5} {(2 + k * (96 / (n - 1))):.2f},{9 + (6 if k % 2 else 0)}' for k in range(1, n)) + ' L100,9'
HTML_TOP = ('<div class="xlights" aria-hidden="true"><svg viewBox="0 0 100 26" preserveAspectRatio="none">'
            f'<path d="{WIRE}" vector-effect="non-scaling-stroke"/></svg>'
            '<svg style="position:absolute;inset:0" width="100%" height="26">' + ''.join(LIGHTS) + '</svg></div>\n'
            '<canvas id="xmas-snow" aria-hidden="true"></canvas>\n')

JS = '''
  // ---- Christmas layer: on 1 Dec – 6 Jan (UK), or forced with ?xmas=1 / ?xmas=0 ----
  (function(){
    const q = new URLSearchParams(location.search).get("xmas");
    const d = new Date(new Date().toLocaleString("en-US",{timeZone:"Europe/London"}));
    const m = d.getMonth(), day = d.getDate();
    const season = (m === 11) || (m === 0 && day <= 6);
    if (!(q === "1" || (season && q !== "0"))) return;
    document.documentElement.classList.add("xmas");
    const c = document.getElementById("xmas-snow"); if (!c || reduce) return;
    const x = c.getContext("2d"); let W, H, flakes = [];
    const cols = ["255,255,255","200,255,46","56,225,255"];
    function size(){ W = c.width = innerWidth; H = c.height = innerHeight;
      const n = Math.round(Math.min(90, W * H / 16000));
      flakes = Array.from({length:n}, () => ({x:Math.random()*W, y:Math.random()*H, r:Math.random()*1.8+.6, s:Math.random()*.5+.25, w:Math.random()*Math.PI*2, c:cols[Math.random() < .7 ? 0 : (Math.random() < .5 ? 1 : 2)], a:Math.random()*.5+.35})); }
    size(); addEventListener("resize", size);
    (function tick(){
      x.clearRect(0,0,W,H);
      for (const f of flakes){ f.y += f.s; f.w += .012; f.x += Math.sin(f.w) * .35;
        if (f.y > H + 4){ f.y = -4; f.x = Math.random()*W; }
        x.beginPath(); x.arc(f.x, f.y, f.r, 0, Math.PI*2); x.fillStyle = "rgba(" + f.c + "," + f.a + ")"; x.fill(); }
      if (!document.hidden) requestAnimationFrame(tick); else setTimeout(() => requestAnimationFrame(tick), 500);
    })();
  })();
'''

def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)

i = h.rindex('</style>'); h = h[:i] + CSS + h[i:]
rep('<header class="top">', HTML_TOP + '<header class="top">')
rep('<div class="inner"><h1 id="scramble"', '<div class="inner"><span class="xbadge"><i></i>Christmas list idea · Ibiza 2027</span><h1 id="scramble"')
# festive note under the hero CTA buttons

rep('<h2 class="scr">See you in 2027</h2>', '<h2 class="scr">See you in 2027</h2><span class="xfin">Merry Christmas from Ibiza Party Flights · sort the 2027 plan with the group</span>')
rep("  // screen-to-screen transitions\n", JS + "\n  // screen-to-screen transitions\n")
open(p, 'w', encoding='utf-8').write(h)
print('ok')
