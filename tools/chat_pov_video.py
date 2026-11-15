#!/usr/bin/env python3
"""TikTok: POV group-chat skit, 100% own graphics (brand colours, invented first names, no app UI copy, no stock).
Hook readable on frame 0 (headline + first 2 messages), bubbles pop every ~1.4 s, end card. Usage:
python3 tools/chat_pov_video.py spec.json out_dir   -> <name>_tiktok.mp4 (no audio)
spec: {name, chip, hook: [line,...], group, msgs: [[who|"", text, t], ...] (who "" = system line),
       end_big, end_mid, end_chip, dur}"""
import sys, os, json, subprocess, base64
spec = json.load(open(sys.argv[1])); D = sys.argv[2].rstrip('/') + '/'; os.makedirs(D + 'f', exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
seal = base64.b64encode(open(ROOT + '/assets/brand/perfil_sello_oscuro.png', 'rb').read()).decode()
COL = ['#C8FF2E', '#38E1FF', '#FF8A5C', '#B9A2FF', '#FFD84D']
names = []
for w, _, _ in spec['msgs']:
    if w and w not in names: names.append(w)
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url(file:///usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf);font-weight:700}}
@font-face{{font-family:P;src:url(file:///usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf);font-weight:500}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{font-family:P,'Noto Color Emoji';color:#fff;background:#04072E}}
#bg{{position:absolute;inset:-300px;background:radial-gradient(circle at 30% 40%,#3150FF 0,#0A1A8F 30%,transparent 60%),radial-gradient(circle at 75% 70%,#7B3CFF 0,transparent 45%),#04072E}}
#top{{position:absolute;left:64px;right:64px;top:300px}}
.chip{{display:inline-block;background:#C8FF2E;color:#000;font:700 38px 'DejaVu Sans Mono',monospace;padding:8px 18px}}
h1{{font:700 92px/1.0 P;text-transform:uppercase;letter-spacing:-.02em;margin-top:22px;text-shadow:0 4px 0 #000}}
h1 .l{{color:#C8FF2E}}
#panel{{position:absolute;left:54px;right:54px;top:760px;height:990px;border-radius:44px;background:rgba(4,7,46,.78);border:3px solid rgba(56,225,255,.5);overflow:hidden}}
#gh{{height:110px;display:flex;align-items:center;gap:22px;padding:0 34px;border-bottom:2px solid rgba(56,225,255,.3);background:#0A1A8F;position:relative;z-index:2}}
#gh .av{{width:70px;height:70px;border-radius:50%;background:#C8FF2E;color:#000;display:flex;align-items:center;justify-content:center;font:700 40px P}}
#gh b{{font:700 40px P}}#gh small{{display:block;font:500 26px P;color:#38E1FF}}
#feed{{position:absolute;left:0;right:0;top:110px;padding:24px 30px;display:flex;flex-direction:column;gap:18px}}
.m{{max-width:82%;padding:16px 26px 18px;border-radius:30px;background:#fff;color:#04072E;font:500 42px/1.25 P,'Noto Color Emoji';transform-origin:left bottom}}
.m .w{{display:block;font:700 28px P;margin-bottom:2px}}
.sys{{align-self:center;font:500 32px P;color:#C8FF2E;background:rgba(200,255,46,.12);padding:10px 26px;border-radius:30px}}
#end{{position:absolute;inset:0;z-index:10;background:#04072E;opacity:0;padding:420px 64px 0}}
#end img{{width:200px;border-radius:50%}}#end h2{{font:700 120px/1 P;color:#C8FF2E;margin-top:40px;text-transform:uppercase}}
#end p{{font:700 64px/1.15 P;margin-top:26px}}#end .chip{{margin-top:40px;background:#fff}}#end .h{{font:500 44px P;color:#38E1FF;margin-top:30px}}
</style></head><body><div id="bg"></div>
<div id="top"><span class="chip">{spec['chip']}</span><h1>{'<br>'.join(spec['hook'])}</h1></div>
<div id="panel"><div id="gh"><div class="av">{spec['group'][0]}</div><div><b>{spec['group']}</b><small>{', '.join(names)}, you</small></div></div><div id="feed"></div></div>
<div id="end"><img src="data:image/png;base64,{seal}"><h2>{spec['end_big']}</h2><p>{spec['end_mid']}</p><span class="chip">{spec['end_chip']}</span><div class="h">@ibizapartyflights</div></div>
<script>
const M={json.dumps(spec['msgs'], ensure_ascii=False)}, NM={json.dumps(names)}, C={json.dumps(COL)}, END={spec['dur']}-2.4;
const feed=document.getElementById('feed');
M.forEach(([w,t])=>{{const d=document.createElement('div');if(!w){{d.className='sys';d.textContent=t}}else{{d.className='m';
 const n=document.createElement('span');n.className='w';n.textContent=w;n.style.color=['#3150FF','#0A8FB0','#D9481E','#6B4BD8','#9A7A00'][NM.indexOf(w)%5];d.appendChild(n);d.appendChild(document.createTextNode(t))}}
 d.style.display='none';feed.appendChild(d)}});
const e=t=>{{t=Math.max(0,Math.min(1,t));return 1-Math.pow(1-t,3)}};
window.render=function(T){{
  document.getElementById('bg').style.transform='translate('+(Math.sin(T*.7)*80)+'px,'+(Math.cos(T*.5)*60)+'px) rotate('+(T*4)+'deg)';
  [...feed.children].forEach((d,i)=>{{const t0=M[i][2];if(T>=t0){{d.style.display='';const k=t0<=0?1:e((T-t0)/.25);d.style.transform='scale('+(.6+.4*k)+')';d.style.opacity=k}}else d.style.display='none'}});
  const over=feed.scrollHeight+24-(990-110); feed.style.top=(110-Math.max(0,over))+'px';
  const k=e((T-END)/.3); document.getElementById('end').style.opacity=T>=END?k:0;
}};
</script></body></html>'''
open(D + 'chat.html', 'w', encoding='utf-8').write(page)
N = int(spec['dur'] * 30)
js = f'''const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});
await p.goto('file://{D}chat.html');await p.waitForTimeout(500);
for(let g=0;g<{N};g++){{await p.evaluate(T=>render(T),g/30);await p.screenshot({{path:'{D}f/'+String(g).padStart(4,'0')+'.jpg',type:'jpeg',quality:93}});}}
await b.close()}})();'''
open(D + 'shoot.js', 'w').write(js)
subprocess.run(['node', D + 'shoot.js'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-i', D + 'f/%04d.jpg', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p',
                '-r', '30', '-movflags', '+faststart', D + spec['name'] + '_tiktok.mp4'], check=True)
print('done', spec['name'])
