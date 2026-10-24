// Reels con movimiento: node tools/reel_motion.js spec.json outdir
// Por cada escena i genera  s{i}_bg.png (fondo sin texto) y s{i}_L{k}.png (capas de texto transparentes 1080x1920).
// Luego tools/reel_build.py anima las capas (fundido + deslizamiento) y une escenas con xfade cortos. Sin zoompan.
// Tipos de escena: hook (bloques de color + tipografía apilada de marca), photo, blocks (personajes isométricos propios), cta (sello + IBIZA SORTED).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); const out = process.argv[3]; fs.mkdirSync(out, { recursive: true });
const root = path.resolve(__dirname, '..');
const N = '#0E1726', O = '#E8582A', S = '#F4E3C8', C = '#4FE3FF', P = '#FF3D8B';
const pal = { N, O, S, C, P };
const col = v => pal[v] || v;
// ---- bloques isométricos (igual que reel_scenes.js) ----
const CC = Math.cos(Math.PI / 6), SS = 0.5; const PJ = (x, y, z) => [(x - y) * CC, (x + y) * SS - z];
const shade = (hex, f) => { const n = parseInt(hex.slice(1), 16); const c = [n >> 16, (n >> 8) & 255, n & 255].map(v => Math.max(0, Math.min(255, Math.round(v * f)))); return `rgb(${c.join(',')})`; };
const poly = (pts, fill) => `<polygon points="${pts.map(p => PJ(...p).map(v => v.toFixed(1)).join(',')).join(' ')}" fill="${fill}" stroke="rgba(0,0,0,.18)" stroke-width="1.5"/>`;
function box(x, y, z, w, d, h, c) { return { k: x + y + z + (w + d) / 2, s: poly([[x, y, z + h], [x + w, y, z + h], [x + w, y + d, z + h], [x, y + d, z + h]], shade(c, 1.12)) + poly([[x, y + d, z], [x + w, y + d, z], [x + w, y + d, z + h], [x, y + d, z + h]], shade(c, .92)) + poly([[x + w, y, z], [x + w, y + d, z], [x + w, y + d, z + h], [x + w, y, z + h]], shade(c, .72)) }; }
function character(ox, oy, o) {
  const b = [], skin = o.skin || '#F2C29B';
  b.push(box(ox + 4, oy + 6, 0, 10, 10, 34, o.legs || '#2B3A55'), box(ox + 18, oy + 6, 0, 10, 10, 34, o.legs || '#2B3A55'));
  b.push(box(ox + 2, oy + 4, 34, 28, 14, 38, o.shirt), box(ox - 8, oy + 6, 40, 10, 10, 32, skin), box(ox + 30, oy + 6, 40, 10, 10, 32, skin));
  b.push(box(ox + 2, oy, 72, 28, 22, 28, skin), box(ox + 2, oy, 98, 28, 22, 8, o.hair || '#4A2E1C'));
  if (o.hat) b.push(box(ox - 2, oy - 4, 106, 36, 30, 6, o.hat), box(ox + 6, oy + 2, 112, 20, 18, 10, o.hat));
  let s = b.sort((a, c) => a.k - c.k).map(v => v.s).join(''); const fy = oy + 22.2;
  if (o.shades) s += poly([[ox + 5, fy, 88], [ox + 27, fy, 88], [ox + 27, fy, 82], [ox + 5, fy, 82]], '#111');
  else s += poly([[ox + 8, fy, 89], [ox + 13, fy, 89], [ox + 13, fy, 84], [ox + 8, fy, 84]], '#1B1B1B') + poly([[ox + 19, fy, 89], [ox + 24, fy, 89], [ox + 24, fy, 84], [ox + 19, fy, 84]], '#1B1B1B');
  s += poly([[ox + 11, fy, 79], [ox + 21, fy, 79], [ox + 21, fy, 76], [ox + 11, fy, 76]], '#8A3B2B');
  return s;
}
const props = l => (l || []).map(p => box(p.x, p.y, p.z || 0, p.w, p.d, p.h, p.c)).sort((a, c) => a.k - c.k).map(v => v.s).join('');
const blockSvg = sc => `<svg viewBox="-150 -170 300 300" width="900" height="900">${poly([[-70, -70, 0], [110, -70, 0], [110, 110, 0], [-70, 110, 0]], sc.ground || S)}${props(sc.propsBack)}${(sc.chars || []).map(c => character(c.x, c.y, c)).join('')}${props(sc.props)}</svg>`;
// ---- piezas de marca ----
function badge(bg, fg, acc, size) {
  const r = 200, txt = 'IBIZA PARTY FLIGHTS • YOUR IBIZA DEAL HUNTERS • ';
  return `<svg width="${size}" height="${size}" viewBox="0 0 540 540"><defs><path id="cp" d="M270,270 m-${r},0 a${r},${r} 0 1,1 ${2 * r},0 a${r},${r} 0 1,1 -${2 * r},0"/><clipPath id="sc"><circle cx="270" cy="270" r="120"/></clipPath></defs>
  <circle cx="270" cy="270" r="262" fill="${bg}"/><text font-family="Poppins" font-weight="700" font-size="34" fill="${fg}"><textPath href="#cp" textLength="1245" lengthAdjust="spacing">${txt}</textPath></text>
  <circle cx="270" cy="270" r="120" fill="${acc}"/><g clip-path="url(#sc)" fill="${bg}">${[0, 1, 2, 3, 4].map(i => `<rect x="140" y="${282 + i * 22}" width="260" height="${5 + i * 3}"/>`).join('')}</g>
  <circle cx="270" cy="270" r="160" fill="none" stroke="${fg}" stroke-width="3"/></svg>`;
}
const waves = (fg, h = 520, n = 6) => { let p = ''; for (let i = 0; i < n; i++) { const y = 60 + i * 80; p += `<path d="M-60,${y} C200,${y - 110} 420,${y + 110} 640,${y} S1000,${y - 80} 1160,${y}" fill="none" stroke="${fg}" stroke-width="${30 - i * 3}" stroke-linecap="round"/>`; } return `<svg width="1080" height="${h}" viewBox="0 0 1080 ${h}">${p}</svg>`; };
const vert = (txt, c, top = 1080, h = 640) => `<div style="position:absolute;left:34px;top:${top}px;height:${h}px;text-align:center;writing-mode:vertical-rl;transform:rotate(180deg);font-weight:600;font-size:26px;letter-spacing:.16em;color:${c};text-transform:uppercase">${txt}</div>`;
const css = `*{margin:0;box-sizing:border-box}html,body{width:1080px;height:1920px;background:transparent}body{font-family:Poppins,'Noto Color Emoji',sans-serif;color:#fff;overflow:hidden}
.s{width:1080px;height:1920px;position:absolute;inset:0;background-size:cover;background-position:center;overflow:hidden}
.stack{position:absolute;left:84px;right:60px;font-weight:700;text-transform:uppercase;line-height:.86;letter-spacing:-.04em}
.box{position:absolute;left:84px;right:90px;top:360px}
.kicker{display:inline-block;font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:40px;padding:12px 28px;border-radius:8px;margin-bottom:30px}
h1{font-size:104px;line-height:.98;font-weight:700;letter-spacing:-.03em;text-shadow:0 4px 26px rgba(0,0,0,.5)}
.sub{display:inline-block;font-size:50px;margin-top:34px;font-weight:600;line-height:1.18;padding:18px 26px;border-radius:10px}
.art{position:absolute;left:90px;bottom:220px}`;
function sceneHtml(s) {
  const L = (k, html) => `<div data-l="${k}">${html}</div>`; let bg = '', fg = '';
  const kc = col(s.kbg || O), kt = col(s.kfg || '#fff');
  const textBox = (k0) => `<div class="box">${s.kicker ? L(k0, `<div class="kicker" style="background:${kc};color:${kt}">${s.kicker}</div>`) : ''}${L(k0 + 1, `<h1 style="color:${col(s.tc || '#fff')}">${s.title}</h1>`)}${s.sub ? L(k0 + 2, `<p class="sub" style="background:${col(s.sbg || 'rgba(14,23,38,.78)')};color:${col(s.sc || '#fff')}">${s.sub}</p>`) : ''}</div>`;
  if (s.type === 'hook') {
    const b = col(s.bg || N), f = col(s.fg || S), a = col(s.acc || O);
    bg = `<div class="s" style="background:${b}">${s.img ? `<div style="position:absolute;left:0;right:0;bottom:0;height:820px;background:url(file://${root}/assets/photos/${s.img}.jpg) center/cover"></div>` : `<div style="position:absolute;bottom:40px;left:0">${waves(col(s.wave || C), 640, 7)}</div>`}${vert(s.vert || 'Ibiza Party Flights — your Ibiza deal hunters', f, s.img ? 1150 : 560, s.img ? 640 : 600)}</div>`;
    fg = `<div class="stack" style="top:${s.top || 210}px;font-size:${s.fs || 150}px;color:${f}">${s.lines.map((l, i) => L(i, `<div style="${i === s.lines.length - 1 ? `color:${a}` : ''}">${l}</div>`)).join('')}</div>`;
    if (s.sub) fg += `<div style="position:absolute;left:84px;top:${s.subTop || 1000}px">${L(s.lines.length, `<p class="sub" style="background:${a};color:${b};margin:0">${s.sub}</p>`)}</div>`;
  } else if (s.type === 'blocks') {
    bg = `<div class="s" style="background:${col(s.bg || C)}"><div style="position:absolute;bottom:0;left:0">${waves(col(s.wave || '#FFFFFF33'), 600)}</div><div class="art">${blockSvg(s)}</div>${s.vert ? vert(s.vert, N, 700, 500) : ''}</div>`;
    fg = textBox(0);
  } else if (s.type === 'cta') {
    const b = col(s.bg || O), f = col(s.fg || N), a = col(s.acc || S);
    bg = `<div class="s" style="background:${b}"><div style="position:absolute;bottom:0;left:0;opacity:.35">${waves(f, 420, 5)}</div></div>`;
    fg = `<div class="stack" style="top:230px;font-size:${s.fs || 120}px;color:${f}">${L(0, s.title)}</div>
    <div style="position:absolute;left:84px;top:${s.subTop || 700}px;font-size:48px;font-weight:600;color:${f};right:80px">${L(1, s.sub || '')}</div>
    <div style="position:absolute;left:270px;top:900px">${L(2, badge(f, a, O === b ? S : O, 540))}</div>
    <div style="position:absolute;left:84px;right:84px;top:1500px;text-align:center">${L(3, `<div style="display:inline-block;background:${f};color:${a};font-weight:700;font-size:42px;padding:20px 34px;border-radius:10px;letter-spacing:.02em">FLY + PARTY + HOTEL = IBIZA SORTED</div><div style="margin-top:26px;color:${f};font-weight:700;font-size:40px">@ibizapartyflights · link in bio</div>`)}</div>`;
  } else {
    bg = `<div class="s" style="background-image:linear-gradient(180deg,rgba(14,23,38,.6) 0%,rgba(14,23,38,.25) 45%,rgba(14,23,38,.55) 100%),url(file://${root}/assets/photos/${s.img}.jpg);background-position:${s.pos || 'center'}"></div>`;
    fg = textBox(0);
  }
  return { bg, fg };
}
(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const pg = await br.newPage({ viewport: { width: 1080, height: 1920 } });
  const meta = [];
  for (let i = 0; i < spec.length; i++) {
    const { bg, fg } = sceneHtml(spec[i]);
    fs.writeFileSync(path.join(out, 'f.html'), `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${bg}<div id="fg" class="s">${fg}</div></body></html>`);
    await pg.goto('file://' + path.resolve(out, 'f.html'), { waitUntil: 'load' }); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(200);
    const n = await pg.evaluate(() => Math.max(-1, ...[...document.querySelectorAll('[data-l]')].map(e => +e.dataset.l)) + 1);
    await pg.evaluate(() => document.getElementById('fg').style.visibility = 'hidden');
    await pg.screenshot({ path: path.join(out, `s${i}_bg.png`) });
    await pg.evaluate(() => { document.getElementById('fg').style.visibility = ''; document.querySelectorAll('body>.s:not(#fg)').forEach(e => e.style.display = 'none'); });
    for (let k = 0; k < n; k++) {
      await pg.evaluate(k => document.querySelectorAll('[data-l]').forEach(e => e.style.visibility = (+e.dataset.l === k ? 'visible' : 'hidden')), k);
      await pg.screenshot({ path: path.join(out, `s${i}_L${k}.png`), omitBackground: true });
    }
    await pg.evaluate(() => document.querySelectorAll('[data-l]').forEach(e => e.style.visibility = 'visible'));
    meta.push({ layers: n, dur: spec[i].dur || 1.9, ...(spec[i].type === 'hook' ? { step: 0.1 } : {}) });
  }
  fs.writeFileSync(path.join(out, 'meta.json'), JSON.stringify(meta)); fs.unlinkSync(path.join(out, 'f.html')); await br.close();
})();
