#!/usr/bin/env python3
"""Adds the Christmas sleigh fly-by and the hanging Santa to the homepage hero (only in Christmas mode).
Usage: santa_anim.py <index.html>"""
import sys
p = sys.argv[1]
h = open(p, encoding='utf-8').read()
assert 'xsleigh' not in h, 'already added'

CSS = '''
/* ---- Christmas: sleigh fly-by + hanging Santa ---- */
.xsleigh,.xsanta,.xgift{display:none}
.xmas .xsleigh{display:block;position:absolute;z-index:4;top:14%;left:0;width:clamp(240px,34vw,520px);pointer-events:none;
  transform:translateX(110vw);will-change:transform;filter:drop-shadow(0 0 18px rgba(56,225,255,.35))}
.xmas .xsleigh img{display:block;width:100%;height:auto}
.xmas .xsleigh::after{content:"";position:absolute;left:96%;top:48%;width:38vw;height:3px;border-radius:3px;
  background:linear-gradient(90deg,rgba(200,255,46,.9),rgba(56,225,255,.5) 40%,transparent);filter:blur(1px)}
.xmas .xsanta{display:block;position:absolute;z-index:3;width:auto;height:.8em;pointer-events:none;opacity:0;
  transform-origin:50% 4%;filter:drop-shadow(0 8px 14px rgba(0,0,0,.35))}
.xmas .xsanta.on{opacity:1}\n@media (max-width:860px){.xmas .xsanta{height:.52em}}
.xmas .xgift{display:block;position:absolute;z-index:4;width:22px;height:22px;pointer-events:none;border-radius:3px}
.xgift::before,.xgift::after{content:"";position:absolute;background:#C8FF2E}
.xgift::before{left:42%;top:0;bottom:0;width:16%}.xgift::after{top:42%;left:0;right:0;height:16%}
@media (prefers-reduced-motion:no-preference){
  .xmas .xsanta.on{animation:xdrop .7s cubic-bezier(.3,1.5,.5,1) both, xswing 2.6s ease-in-out .7s infinite}
  @keyframes xdrop{from{transform:translateY(-60%) rotate(-12deg);opacity:0}to{transform:translateY(0) rotate(0);opacity:1}}
  @keyframes xswing{0%,100%{transform:rotate(5deg)}50%{transform:rotate(-5deg)}}
}
'''

def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)

i = h.rindex('</style>'); h = h[:i] + CSS + h[i:]
# sleigh lives in the hero; Santa lives inside the 3D word so he moves with it
rep('<div class="inner stage" aria-hidden="true"><div class="puffy" id="puffy">',
    '<div class="xsleigh" id="xsleigh" aria-hidden="true"><img src="img/xmas/sleigh.webp" alt="" width="760" height="468" loading="lazy" decoding="async"></div>'
    '<div class="inner stage" aria-hidden="true"><div class="puffy" id="puffy">'
    '<img class="xsanta" id="xsanta" src="img/xmas/santa.webp" alt="" width="232" height="420" loading="lazy" decoding="async">')

JS = '''
    // sleigh fly-by, falling gifts and Santa hanging from the "z"
    (function(){
      const hero = document.getElementById("hero"), sl = document.getElementById("xsleigh"),
            pf = document.getElementById("puffy"), sa = document.getElementById("xsanta");
      if (!hero || !sl || !pf || !sa) return;
      function placeSanta(){
        const face = pf.querySelector(".face"); const t = face && face.firstChild; if (!t) return;
        const r = document.createRange(); r.setStart(t, 3); r.setEnd(t, 4);          // the "z"
        const z = r.getBoundingClientRect(), b = pf.getBoundingClientRect(); if (!z.width) return;
        const sc = pf.offsetWidth / b.width || 1;                                     // undo 3D scale
        sa.style.left = ((z.left - b.left + z.width / 2) * sc - sa.offsetWidth / 2) + "px";
        sa.style.top = ((z.bottom - b.top) * sc - sa.offsetHeight * 0.06) + "px";    // hands on the bottom of the z
      }
      function showSanta(){ placeSanta(); sa.classList.add("on"); }
      (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(placeSanta);
      addEventListener("resize", placeSanta);
      sa.addEventListener("load", placeSanta);
      if (reduce){ showSanta(); return; }
      function gifts(x, y){
        const cols = ["#FF3D6E", "#38E1FF", "#3150FF"];
        for (let k = 0; k < 3; k++){
          const g = document.createElement("i"); g.className = "xgift"; g.style.background = cols[k];
          g.style.left = (x + k * 26 - 26) + "px"; g.style.top = y + "px"; hero.appendChild(g);
          g.animate([{transform:"translateY(0) rotate(0)", opacity:1},
                     {transform:"translateY(" + (hero.clientHeight * .32) + "px) rotate(" + (k % 2 ? 220 : -200) + "deg)", opacity:0}],
                    {duration:1500 + k * 180, easing:"cubic-bezier(.45,0,.9,.6)", fill:"forwards"}).onfinish = () => g.remove();
        }
      }
      let flying = false, first = true;
      function fly(){
        if (flying) return; flying = true;
        const W = innerWidth, w = sl.offsetWidth, dur = Math.max(3800, W * 3.2);
        const a = sl.animate([{transform:"translateX(" + (W + 40) + "px) translateY(0)"},
                              {transform:"translateX(" + (W * .45 - w / 2) + "px) translateY(-14px)", offset:.5},
                              {transform:"translateX(" + (-w - 60) + "px) translateY(6px)"}],
                             {duration:dur, easing:"linear"});
        setTimeout(() => { const s = sl.getBoundingClientRect(), hb = hero.getBoundingClientRect();
                           gifts(s.left - hb.left + s.width * .72, s.top - hb.top + s.height * .55);
                           if (first){ setTimeout(showSanta, 700); first = false; } }, dur * .5);
        a.onfinish = () => { flying = false; };
      }
      // flies once per visit, then Santa stays hanging from the "z"
      let seen = false;
      new IntersectionObserver((es, ob) => es.forEach(e => {
        if (e.isIntersecting && !seen){ seen = true; ob.disconnect(); setTimeout(fly, 1400); }
      }), {threshold:.4}).observe(hero);
    })();
'''
rep('    document.documentElement.classList.add("xmas");\n',
    '    document.documentElement.classList.add("xmas");\n' + JS)
open(p, 'w', encoding='utf-8').write(h)
print('ok')
