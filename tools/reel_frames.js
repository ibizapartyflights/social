const { chromium } = require('playwright'); const fs=require('fs');
const logo=`<svg width="64" height="64" viewBox="0 0 30 30"><circle cx="15" cy="15" r="14.2" fill="#0E1726" stroke="#fff" stroke-width="1.6"/><circle cx="15" cy="17" r="6.5" fill="#E8582A"/></svg>`;
const scenes=[
 {img:"hotel_playa",kicker:"Ibiza 2027",title:"Where to stay in Ibiza for clubbing 🏝️",sub:"4 areas in 15 seconds"},
 {img:"piscina",num:"1",kicker:"Playa d'en Bossa",title:"Next to Ushuaïa & Hï Ibiza",sub:"Big club nights on foot"},
 {img:"luces_club",num:"2",kicker:"Ibiza Town",title:"Near Pacha & the marina",sub:"Party + food + old town"},
 {img:"hamacas",num:"3",kicker:"Sant Rafel",title:"Closest to [UNVRS] & Amnesia",sub:"Quieter, inland"},
 {img:"playa_gente",num:"4",kicker:"San Antonio",title:"Sunset bars & pool parties",sub:"Usually the cheapest"},
 {cta:true,title:"Save this 📌",sub:"Compare hotels by area<br>Link in bio · @ibizapartyflights"}];
const css=`*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;font-family:Poppins,sans-serif;color:#fff}
.s{width:1080px;height:1920px;position:relative;background-size:cover;background-position:center}
.brand{position:absolute;top:150px;left:80px;display:flex;align-items:center;gap:18px;font-weight:700;font-size:38px;text-shadow:0 2px 10px rgba(0,0,0,.4)}
.box{position:absolute;left:80px;right:140px;top:640px}
.kicker{color:#FF8A5C;font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-size:40px;margin-bottom:20px;text-shadow:0 2px 10px rgba(0,0,0,.5)}
h1{font-size:104px;line-height:1.03;font-weight:700;letter-spacing:-.02em;text-shadow:0 4px 24px rgba(0,0,0,.45)}
.sub{font-size:48px;margin-top:30px;font-weight:500;text-shadow:0 2px 12px rgba(0,0,0,.5)}
.num{width:110px;height:110px;border-radius:50%;background:#E8582A;font-size:58px;font-weight:700;display:flex;align-items:center;justify-content:center;margin-bottom:30px}
.cta{background:#E8582A}.cta h1{font-size:130px}.url{display:inline-block;margin-top:50px;background:#0E1726;font-weight:700;font-size:50px;padding:26px 40px;border-radius:20px}`;
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1920}});
for(let i=0;i<scenes.length;i++){const s=scenes[i];
 const bg=s.cta?``:`style="background-image:linear-gradient(180deg,rgba(14,23,38,.35) 0%,rgba(14,23,38,.55) 45%,rgba(14,23,38,.35) 100%),url(file://${process.cwd()}/${s.img}.jpg)"`;
 const inner=s.cta?`<div class="box"><h1>${s.title}</h1><p class="sub">${s.sub}</p><div class="url">ibizapartyflights.co.uk</div></div>`:
  `<div class="box">${s.num?`<div class="num">${s.num}</div>`:""}<div class="kicker">${s.kicker}</div><h1>${s.title}</h1><p class="sub">${s.sub}</p></div>`;
 fs.writeFileSync('f.html',`<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body><div class="s ${s.cta?'cta':''}" ${bg}><div class="brand">${logo}Ibiza Party Flights</div>${inner}</div></body></html>`);
 await p.goto('file://'+process.cwd()+'/f.html',{waitUntil:'load'});await p.waitForTimeout(200);await p.screenshot({path:`s${i}.png`});}
await b.close();})();
