// Render reel scenes 1080x1920 from a JSON spec: node tools/reel_scenes.js spec.json outdir
// Scene types: photo (img in assets/photos), blocks (own isometric block characters), cta (brand end screen).
// No brand/logo top-left: the brand goes only on the final CTA screen.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); const out = process.argv[3]; fs.mkdirSync(out, { recursive: true });
const root = path.resolve(__dirname, '..');
const logo = `<svg width="120" height="120" viewBox="0 0 30 30"><circle cx="15" cy="15" r="14.2" fill="#0E1726" stroke="#fff" stroke-width="1.2"/><circle cx="15" cy="17" r="6.5" fill="#E8582A"/></svg>`;
// ---- isometric block helpers ----
const C = Math.cos(Math.PI / 6), S = 0.5;
const P = (x, y, z) => [(x - y) * C, (x + y) * S - z];
const shade = (hex, f) => { const n = parseInt(hex.slice(1), 16); const c = [n >> 16, (n >> 8) & 255, n & 255].map(v => Math.max(0, Math.min(255, Math.round(v * f)))); return `rgb(${c.join(',')})`; };
const poly = (pts, fill) => `<polygon points="${pts.map(p => P(...p).map(v => v.toFixed(1)).join(',')).join(' ')}" fill="${fill}" stroke="rgba(0,0,0,.18)" stroke-width="1.5"/>`;
function box(x, y, z, w, d, h, col) {
  return { k: x + y + z + (w + d) / 2, s:
    poly([[x, y, z + h], [x + w, y, z + h], [x + w, y + d, z + h], [x, y + d, z + h]], shade(col, 1.12)) +
    poly([[x, y + d, z], [x + w, y + d, z], [x + w, y + d, z + h], [x, y + d, z + h]], shade(col, .92)) +
    poly([[x + w, y, z], [x + w, y + d, z], [x + w, y + d, z + h], [x + w, y, z + h]], shade(col, .72)) };
}
// character standing at (ox,oy); face on +y side
function character(ox, oy, o) {
  const b = [], skin = o.skin || '#F2C29B';
  b.push(box(ox + 4, oy + 6, 0, 10, 10, 34, o.legs || '#2B3A55'));
  b.push(box(ox + 18, oy + 6, 0, 10, 10, 34, o.legs || '#2B3A55'));
  b.push(box(ox + 2, oy + 4, 34, 28, 14, 38, o.shirt));
  b.push(box(ox - 8, oy + 6, 40, 10, 10, 32, skin));
  b.push(box(ox + 30, oy + 6, 40, 10, 10, 32, skin));
  b.push(box(ox + 2, oy, 72, 28, 22, 28, skin));
  b.push(box(ox + 2, oy, 98, 28, 22, 8, o.hair || '#4A2E1C'));
  if (o.hat) b.push(box(ox - 2, oy - 4, 106, 36, 30, 6, o.hat), box(ox + 6, oy + 2, 112, 20, 18, 10, o.hat));
  let s = b.sort((a, c) => a.k - c.k).map(v => v.s).join('');
  const fy = oy + 22.2; // face plane
  if (o.shades) s += poly([[ox + 5, fy, 88], [ox + 27, fy, 88], [ox + 27, fy, 82], [ox + 5, fy, 82]], '#111');
  else s += poly([[ox + 8, fy, 89], [ox + 13, fy, 89], [ox + 13, fy, 84], [ox + 8, fy, 84]], '#1B1B1B') + poly([[ox + 19, fy, 89], [ox + 24, fy, 89], [ox + 24, fy, 84], [ox + 19, fy, 84]], '#1B1B1B');
  s += poly([[ox + 11, fy, 79], [ox + 21, fy, 79], [ox + 21, fy, 76], [ox + 11, fy, 76]], '#8A3B2B');
  return s;
}
function props(list) { return (list || []).map(p => box(p.x, p.y, p.z || 0, p.w, p.d, p.h, p.c)).sort((a, c) => a.k - c.k).map(v => v.s).join(''); }
function blockSvg(sc) {
  const chars = sc.chars.map(c => character(c.x, c.y, c)).join('');
  const ground = poly([[-70, -70, 0], [110, -70, 0], [110, 110, 0], [-70, 110, 0]], sc.ground || '#F4D9A6');
  return `<svg viewBox="-150 -170 300 300" width="900" height="900">${ground}${props(sc.propsBack)}${chars}${props(sc.props)}</svg>`;
}
const css = `*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;font-family:Poppins,'Noto Color Emoji',sans-serif;color:#fff;overflow:hidden}
.s{width:1080px;height:1920px;position:relative;background-size:cover;background-position:center}
.box{position:absolute;left:80px;right:100px;top:330px}
.kicker{display:inline-block;background:#E8582A;color:#fff;font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:40px;padding:10px 26px;border-radius:14px;margin-bottom:28px}
.kicker.alt{background:#fff;color:#0E1726}
h1{font-size:100px;line-height:1.04;font-weight:700;letter-spacing:-.02em;text-shadow:0 4px 24px rgba(0,0,0,.45)}
.sub{font-size:52px;margin-top:30px;font-weight:600;line-height:1.2;text-shadow:0 2px 12px rgba(0,0,0,.55)}
.art{position:absolute;left:90px;bottom:250px}
.blocks{background:linear-gradient(180deg,#1B7FB8 0%,#5FC3E4 55%,#FFD8A8 100%)}
.cta{background:#E8582A;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.cta h1{font-size:110px;padding:0 70px}.cta .sub{padding:0 80px}
.brand{margin-top:70px;display:flex;flex-direction:column;align-items:center;gap:22px;font-weight:700;font-size:54px}
.tag{font-size:38px;font-weight:600;opacity:.95}.formula{margin-top:16px;background:#0E1726;font-size:40px;padding:18px 34px;border-radius:18px;letter-spacing:.03em}`;
(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const pg = await br.newPage({ viewport: { width: 1080, height: 1920 } });
  for (let i = 0; i < spec.length; i++) {
    const s = spec[i]; let body;
    const text = `<div class="box">${s.kicker ? `<div class="kicker ${s.alt ? 'alt' : ''}">${s.kicker}</div>` : ''}<h1>${s.title}</h1>${s.sub ? `<p class="sub">${s.sub}</p>` : ''}</div>`;
    if (s.type === 'cta') body = `<div class="s cta"><h1>${s.title}</h1><p class="sub">${s.sub || ''}</p><div class="brand">${logo}<div>Ibiza Party Flights</div><div class="tag">Your Ibiza deal hunters</div><div class="formula">FLY + PARTY + HOTEL = IBIZA SORTED</div><div class="tag">@ibizapartyflights · link in bio</div></div></div>`;
    else if (s.type === 'blocks') body = `<div class="s blocks">${text}<div class="art">${blockSvg(s)}</div></div>`;
    else body = `<div class="s" style="background-image:linear-gradient(180deg,rgba(14,23,38,.55) 0%,rgba(14,23,38,.35) 50%,rgba(14,23,38,.6) 100%),url(file://${root}/assets/photos/${s.img}.jpg)">${text}</div>`;
    fs.writeFileSync(path.join(out, 'f.html'), `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${body}</body></html>`);
    await pg.goto('file://' + path.resolve(out, 'f.html'), { waitUntil: 'load' }); await pg.waitForTimeout(250);
    await pg.screenshot({ path: path.join(out, `s${i}.png`) });
  }
  fs.unlinkSync(path.join(out, 'f.html')); await br.close();
})();
