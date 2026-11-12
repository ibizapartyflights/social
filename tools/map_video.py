#!/usr/bin/env python3
"""TikTok video: Ibiza map with stay zones, beaches and clubs. Writes page.html next to this file."""
import os
SRC = '/home/claude/social/tools/web/mapbuild.py'
code = open(SRC, encoding='utf-8').read()
ns = {}
exec(code[:code.index('def pin(')], ns)          # geometry only: P, ISLAND, ISLETS, cx, cy, W, H
P, ISLAND, ISLETS, cx, cy, W, H = (ns[k] for k in ('P', 'ISLAND', 'ISLETS', 'cx', 'cy', 'W', 'H'))

# kind, label, lat, lon, label side
STAY = [("Playa d'en Bossa", 38.893, 1.412, 'l'), ('Ibiza Town', 38.910, 1.428, 'r'), ('Talamanca', 38.925, 1.463, 'r'),
        ('Sant Rafel', 38.967, 1.413, 'r'), ('San Antonio', 38.961, 1.313, 'rb'), ('Santa Eulària', 38.991, 1.531, 'l'),
        ('Portinatx', 39.106, 1.516, 'l')]
BEACH = [('Cala Comte', 38.966, 1.216, 'rb'), ('Cala Bassa', 38.972, 1.240, 'ra'), ('Cala Salada', 39.008, 1.297, 'r'),
         ("Cala d'Hort", 38.890, 1.222, 'r'), ('Ses Salines', 38.838, 1.407, 'r'), ('Benirràs', 39.092, 1.450, 'l'),
         ('Cala Llonga', 38.955, 1.522, 'l')]
CLUB = [('Ushuaïa · Hï', 38.882, 1.399, 'l'), ('DC-10', 38.872, 1.380, 'l'), ('Pacha', 38.922, 1.440, 'r'),
        ('Amnesia', 38.948, 1.408, 'r'), ('[UNVRS]', 38.958, 1.394, 'l'), ('Eden · Es Paradis', 38.980, 1.315, 'rb'),
        ('Ibiza Rocks', 38.992, 1.303, 'ra')]

def marks(items, kind):
    out = []
    for n, (name, lat, lon, side) in enumerate(items):
        x, y = P(lat, lon)
        if kind == 'stay':
            shape = '<rect class="mk" x="-6" y="-6" width="12" height="12"/>'
        elif kind == 'beach':
            shape = '<circle class="mk" r="6.5"/>'
        else:
            shape = '<rect class="mk" x="-5.5" y="-5.5" width="11" height="11" transform="rotate(45)"/>'
        dx, anchor = (13, 'start') if side.startswith('r') else (-13, 'end')
        dy = {'ra': -6, 'rb': 18}.get(side, 5)
        out.append(f'<g class="m {kind}" data-n="{n}" transform="translate({x},{y})"><circle class="ping" r="16"/>{shape}'
                   f'<text x="{dx}" y="{dy}" text-anchor="{anchor}">{name}</text></g>')
    return ''.join(out)

grid = ''.join(f'<line x1="{x}" y1="-200" x2="{x}" y2="{H+200}"/>' for x in range(-60, W + 120, 40)) + \
       ''.join(f'<line x1="-100" y1="{y}" x2="{W+100}" y2="{y}"/>' for y in range(-200, H + 220, 40))
rings = ''.join(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}"/>' for r in (80, 160, 240, 320, 400))
contours = ''.join(f'<use href="#isl" transform="translate({cx*(1-s):.1f},{cy*(1-s):.1f}) scale({s})" opacity="{o}"/>'
                   for s, o in ((.86, .5), (.7, .4), (.52, .32), (.34, .25)))
SEAL = open('/tmp/claude-0/-home-claude/66b6d558-d986-5edb-84a4-47ec5aa45195/scratchpad/mapvid/seal.b64').read().strip()

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#05093F}}
body{{font-family:Poppins,sans-serif;color:#F2F2F2;position:relative;
  background:radial-gradient(ellipse 90% 55% at 45% 50%,#0A1A8F 0%,#071270 45%,#04072E 100%)}}
.mono{{font-family:'DejaVu Sans Mono',monospace}}
#top{{position:absolute;left:60px;right:60px;top:170px}}
.kick{{display:inline-block;background:#C8FF2E;color:#000;font:700 30px 'DejaVu Sans Mono',monospace;padding:8px 16px;letter-spacing:.04em}}
.kick.cy{{background:#38E1FF}}.kick.wh{{background:#fff}}
h1{{font-weight:800;font-size:92px;line-height:.95;letter-spacing:-.02em;text-transform:uppercase;margin-top:18px}}
h1 em{{font-style:normal;color:#C8FF2E}}
.sub{{font-weight:600;font-size:36px;color:#38E1FF;margin-top:14px}}
.scene{{position:absolute;left:0;right:0;top:0;opacity:0}}
#mapbox{{position:absolute;left:-30px;top:480px;width:1110px}}
svg{{display:block;width:100%;height:auto;overflow:visible}}
.seagrid line{{stroke:#38E1FF;stroke-opacity:.08;stroke-width:.8}}
.rings circle{{fill:none;stroke:#38E1FF;stroke-opacity:.14;stroke-dasharray:2 7}}
.shadow{{fill:#000;opacity:.4}}
.coast{{fill:none;stroke:#38E1FF;stroke-width:1.8}}
.contours use{{fill:none;stroke:#C8FF2E;stroke-width:.9}}
.islets ellipse{{fill:#3150FF;fill-opacity:.5;stroke:#38E1FF;stroke-width:1}}
.m text{{font:700 15px Poppins,sans-serif;fill:#fff;paint-order:stroke;stroke:#05093F;stroke-width:4px;stroke-linejoin:round}}
.m .mk{{stroke:#05093F;stroke-width:1.5}}
.m.stay .mk{{fill:#C8FF2E}}.m.beach .mk{{fill:#fff}}.m.club .mk{{fill:#38E1FF}}
.m .ping{{fill:none;stroke-width:1.6;opacity:0}}
.m.stay .ping{{stroke:#C8FF2E}}.m.beach .ping{{stroke:#fff}}.m.club .ping{{stroke:#38E1FF}}
.m{{opacity:0}}
#legend{{position:absolute;left:60px;right:60px;top:1500px;display:flex;gap:16px;flex-wrap:wrap}}
.lg{{display:flex;align-items:center;gap:12px;font:700 28px 'DejaVu Sans Mono',monospace;padding:10px 16px;border:2px solid #2A3A9F;background:rgba(5,9,63,.7);opacity:.3}}
.lg i{{display:block;width:20px;height:20px}}
.lg.s i{{background:#C8FF2E}}.lg.b i{{background:#fff;border-radius:50%}}.lg.c i{{background:#38E1FF;transform:rotate(45deg) scale(.85)}}
#readout{{position:absolute;left:64px;top:1450px;font:700 26px 'DejaVu Sans Mono',monospace;color:#C8FF2E}}
#seal{{position:absolute;right:56px;top:66px;width:120px;height:120px;opacity:0}}
#scan{{position:absolute;left:60px;top:110px;font:700 26px 'DejaVu Sans Mono',monospace;color:#38E1FF;opacity:.9}}
</style></head><body>
<div id="scan" class="mono">&gt; scan --island IBIZA</div>
<img id="seal" src="data:image/png;base64,{SEAL}" alt="">
<div id="top">
  <div class="scene" id="s0"><span class="kick">IBIZA 2027</span><h1>Save this<br>before you<br><em>book Ibiza</em></h1><div class="sub">The island, decoded in 15 seconds</div></div>
  <div class="scene" id="s1"><span class="kick">01 · STAY</span><h1>Where to<br><em>stay</em></h1><div class="sub">Pick your base by the clubs you want</div></div>
  <div class="scene" id="s2"><span class="kick wh">02 · BEACHES</span><h1>Where to<br><em>swim</em></h1><div class="sub">Sunset coves west, salt flats south</div></div>
  <div class="scene" id="s3"><span class="kick cy">03 · CLUBS</span><h1>Where to<br><em>party</em></h1><div class="sub">Superclubs inland, day parties by the sea</div></div>
  <div class="scene" id="s4"><span class="kick">SAVE IT</span><h1>Send this to<br>the <em>group chat</em></h1><div class="sub">Follow for more Ibiza 2027 tips</div></div>
</div>
<div id="mapbox"><svg viewBox="0 0 {W} {H}">
  <defs>
    <path id="isl" d="{ISLAND}"/>
    <clipPath id="islClip"><use href="#isl"/></clipPath>
    <linearGradient id="islFill" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3150FF" stop-opacity=".6"/><stop offset=".55" stop-color="#0A1A8F" stop-opacity=".8"/><stop offset="1" stop-color="#7B3CFF" stop-opacity=".55"/></linearGradient>
    <pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#38E1FF" fill-opacity=".35"/></pattern>
    <linearGradient id="sweepG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C8FF2E" stop-opacity="0"/><stop offset="1" stop-color="#C8FF2E" stop-opacity=".4"/></linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <g class="seagrid">{grid}</g><g class="rings" id="rings">{rings}</g>
  <g id="land" opacity="0">
    <use href="#isl" class="shadow" transform="translate(0,10)"/>
    <use href="#isl" fill="url(#islFill)"/>
    <g clip-path="url(#islClip)"><rect width="{W}" height="{H}" fill="url(#dots)"/><g class="contours">{contours}</g>
      <g id="sweep" style="transform-origin:{cx:.0f}px {cy:.0f}px"><path d="M{cx:.0f},{cy:.0f} L{cx+420:.0f},{cy-80:.0f} A428,428 0 0 1 {cx+420:.0f},{cy+80:.0f}Z" fill="url(#sweepG)"/></g></g>
    <g class="islets">{ISLETS}</g>
  </g>
  <use href="#isl" class="coast" id="coast" filter="url(#glow)" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000"/>
  <g id="stay">{marks(STAY, 'stay')}</g><g id="beach">{marks(BEACH, 'beach')}</g><g id="club">{marks(CLUB, 'club')}</g>
</svg></div>
<div id="readout">38.98°N 1.43°E</div>
<div id="legend"><div class="lg s" id="l1"><i></i>STAY</div><div class="lg b" id="l2"><i></i>BEACHES</div><div class="lg c" id="l3"><i></i>CLUBS</div></div>
<script>
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)), ease=t=>{{t=clamp(t);return t*t*(3-2*t)}};
const SC=[[0,2.4],[2.4,6.2],[6.2,10],[10,13.8],[13.8,16.6]];
const groups=[null,'stay','beach','club'];
function sceneA(i,t){{const [a,b]=SC[i];return Math.min(ease((t-a)/.35), i===SC.length-1?1:ease((b-t)/.3))}}
window.render=function(t){{
  for(let i=0;i<SC.length;i++){{const el=document.getElementById('s'+i),a=sceneA(i,t);el.style.opacity=a;el.style.transform='translateY('+((1-a)*30)+'px)';}}
  document.getElementById('coast').setAttribute('stroke-dashoffset',1000*(1-ease(t/1.4)));
  document.getElementById('land').setAttribute('opacity',ease((t-.5)/.9));
  document.getElementById('sweep').style.transform='rotate('+(t*72)+'deg)';
  document.getElementById('seal').style.opacity=ease((t-.3)/.6);
  document.getElementById('seal').style.transform='rotate('+(-t*20)+'deg)';
  const cur=t<SC[1][0]?0:t<SC[2][0]?1:t<SC[3][0]?2:t<SC[4][0]?3:4;
  groups.forEach((g,gi)=>{{ if(!g) return;
    const start=SC[gi][0]+.25, ms=[...document.querySelectorAll('#'+g+' .m')];
    ms.forEach((m,n)=>{{ const t0=start+n*.32, a=ease((t-t0)/.25);
      let dim = (cur===gi||cur===4)?1:(cur>gi?.28:0);
      m.style.opacity=Math.min(a,1)*dim;
      const pop = 1+.6*Math.max(0,1-(t-t0)/.3)*(t>t0?1:0);
      m.querySelector('.mk').setAttribute('transform',(g==='club'?'rotate(45) ':'')+'scale('+pop+')');
      const ph=((t-t0)%1.6)/1.6; const ping=m.querySelector('.ping');
      if(t>t0 && (cur===gi||cur===4)){{ping.setAttribute('r',6+ph*22);ping.style.opacity=(1-ph)*.9}} else ping.style.opacity=0;
      m.querySelector('text').style.opacity=(cur===gi||cur===4&&g!=='beach')?1:(cur===4?1:0);
    }});
    const lg=document.getElementById('l'+gi); lg.style.opacity=(cur===gi||cur===4)?1:(cur>gi?.55:.3);
    lg.style.borderColor=(cur===gi)?'#fff':'#2A3A9F';
  }});
  // in the final scene keep only some labels to avoid clutter
  if(cur===4) document.querySelectorAll('.m text').forEach(x=>x.style.opacity=0);
  const ro=[38.98+.06*Math.sin(t*.9),1.43+.08*Math.cos(t*.7)];
  document.getElementById('readout').textContent=ro[0].toFixed(3)+'°N '+ro[1].toFixed(3)+'°E';
}};
render(0);
</script></body></html>'''
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page.html'), 'w', encoding='utf-8').write(html)
print('ok')
