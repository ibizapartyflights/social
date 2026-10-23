const { chromium } = require('playwright'); const fs=require('fs');
const N='#0E1726', O='#E8582A', S='#F4E3C8', C='#4FE3FF', P='#FF3D8B';
// circular badge
function badge(bg,fg,acc,size=540){
 const r=200, txt='IBIZA PARTY FLIGHTS • YOUR IBIZA DEAL HUNTERS • ';
 return `<svg width="${size}" height="${size}" viewBox="0 0 540 540"><rect width="540" height="540" fill="${bg}"/>
 <defs><path id="cp" d="M270,270 m-${r},0 a${r},${r} 0 1,1 ${2*r},0 a${r},${r} 0 1,1 -${2*r},0"/>
 <clipPath id="sc"><circle cx="270" cy="270" r="120"/></clipPath></defs>
 <text font-family="Poppins" font-weight="700" font-size="34" fill="${fg}"><textPath href="#cp" textLength="1245" lengthAdjust="spacing">${txt}</textPath></text>
 <circle cx="270" cy="270" r="120" fill="${acc}"/>
 <g clip-path="url(#sc)" fill="${bg}">${[0,1,2,3,4].map(i=>`<rect x="140" y="${282+i*22}" width="260" height="${5+i*3}"/>`).join('')}</g>
 <circle cx="270" cy="270" r="160" fill="none" stroke="${fg}" stroke-width="3"/>
 </svg>`;}
function waves(bg,fg,n=7){ let p=''; for(let i=0;i<n;i++){const y=80+i*70; p+=`<path d="M-40,${y} C120,${y-90} 260,${y+90} 420,${y} S700,${y-60} 600,${y}" fill="none" stroke="${fg}" stroke-width="${26-i*2}" stroke-linecap="round"/>`;} return `<svg width="540" height="540" viewBox="0 0 540 540"><rect width="540" height="540" fill="${bg}"/>${p}</svg>`;}
const stack=(bg,fg,lines,fs=118,acc)=>`<div style="width:540px;height:540px;background:${bg};color:${fg};font-family:Poppins;font-weight:700;font-size:${fs}px;line-height:.86;letter-spacing:-.04em;padding:34px 30px;display:flex;flex-direction:column;justify-content:center;text-transform:uppercase">${lines.map((l,i)=>`<div style="${acc&&i===lines.length-1?`color:${acc}`:''}">${l}</div>`).join('')}</div>`;
const vert=(bg,fg,big,small)=>`<div style="width:540px;height:540px;flex:none;background:${bg};color:${fg};font-family:Poppins;position:relative;overflow:hidden"><div style="position:absolute;left:18px;top:20px;bottom:20px;writing-mode:vertical-rl;transform:rotate(180deg);font-weight:600;font-size:22px;letter-spacing:.12em">${small}</div><div style="position:absolute;right:30px;top:40px;font-weight:700;font-size:96px;line-height:.9;letter-spacing:-.04em;text-align:right">${big}</div></div>`;
const tiles=[
 stack(N,S,['IBI-','ZA','PAR-','TY'],128,O),
 badge(S,N,O),
 vert(O,N,'FLY<br>+<br>PARTY<br>+<br>HOTEL','IBIZA PARTY FLIGHTS — 2027'),
 waves(N,C),
 waves(O,N),
 vert(N,S,'IBIZA<br>SOR-<br>TED','YOUR IBIZA DEAL HUNTERS'),
 badge(N,S,O),
 stack(C,N,['DEAL','HUN-','TERS'],120,O),
];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:2160,height:1080}});
const html=`<!doctype html><html><head><meta charset="utf-8"><style>*{margin:0}body{display:grid;grid-template-columns:repeat(4,540px);grid-auto-rows:540px;width:2160px} body>*{overflow:hidden;width:540px;height:540px}</style></head><body>${tiles.join('')}</body></html>`;
fs.writeFileSync('b.html',html);await p.goto('file://'+process.cwd()+'/b.html');await p.waitForTimeout(400);await p.screenshot({path:'sistema_marca.png'});
await p.setViewportSize({width:1080,height:1080});
for(const [k,t] of [['perfil_sello_claro',badge(S,N,O,1080)],['perfil_sello_oscuro',badge(N,S,O,1080)]]){fs.writeFileSync('p.html',`<!doctype html><html><head><meta charset="utf-8"><style>*{margin:0}</style></head><body>${t}</body></html>`);await p.goto('file://'+process.cwd()+'/p.html');await p.waitForTimeout(300);await p.screenshot({path:k+'.png'});}
await b.close();})();
