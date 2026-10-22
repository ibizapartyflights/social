const { chromium } = require('playwright'); const sets = require('./slides.js'); const fs=require('fs');
const css = `*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;font-family:Poppins,sans-serif}
.s{width:1080px;height:1350px;position:relative;overflow:hidden;color:#fff;padding:72px}
.cover{background-size:cover;background-position:center}
.card{background:#0E1726}.ctaS{background:#E8582A}
.brand{display:flex;align-items:center;gap:16px;font-weight:700;font-size:32px}
.ctaS .brand svg circle:first-child{fill:#0E1726}
.bottom{position:absolute;left:72px;right:72px;bottom:110px}
.kicker{color:#FF8A5C;font-weight:600;letter-spacing:.12em;text-transform:uppercase;font-size:30px;margin-bottom:18px}
h1{font-size:92px;line-height:1.02;font-weight:700;letter-spacing:-.02em}
.sub{font-size:38px;margin-top:26px;opacity:.95}
.swipe{margin-top:36px;font-size:30px;font-weight:600;color:#FF8A5C}
.mid{position:absolute;left:72px;right:72px;top:50%;transform:translateY(-50%)}
h2{font-size:80px;line-height:1.05;font-weight:700;letter-spacing:-.02em;margin-bottom:40px}
.body{font-size:40px;line-height:1.45;color:#D7DEE8}.body p{margin-bottom:26px}.body b{color:#fff}
.ctaS .body{color:#fff}.ctaS h2{color:#fff}
ol{padding-left:0;list-style:none;counter-reset:i}ol li{counter-increment:i;margin-bottom:34px;padding-left:96px;position:relative}
ol li:before{content:counter(i);position:absolute;left:0;top:0;width:68px;height:68px;border-radius:50%;background:#E8582A;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;font-size:36px}
.tag{width:96px;height:96px;border-radius:50%;background:#E8582A;font-size:48px;font-weight:700;display:flex;align-items:center;justify-content:center;margin-bottom:30px}
.ad{font-size:30px;color:#9AA6B8}
.url{display:inline-block;margin-top:20px;background:#0E1726;color:#fff;font-weight:700;font-size:42px;padding:22px 34px;border-radius:18px}
.small{margin-top:22px;font-size:32px;font-weight:600}
.num{position:absolute;right:72px;bottom:56px;font-size:28px;opacity:.7;font-weight:600}`;
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1350}});
fs.mkdirSync('out',{recursive:true});
for(const [k,slides] of Object.entries(sets)){ for(let i=0;i<slides.length;i++){
 fs.writeFileSync('tmp.html',`<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${slides[i]}</body></html>`); await p.goto('file://'+process.cwd()+'/tmp.html',{waitUntil:'load'});
 await p.waitForTimeout(150); await p.screenshot({path:`out/${k}_${i+1}.jpg`,type:'jpeg',quality:86});}}
await b.close(); console.log(fs.readdirSync('out').join(' '));})();
