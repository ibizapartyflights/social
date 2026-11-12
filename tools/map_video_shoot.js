const {chromium}=require('playwright');
(async()=>{const D=process.argv[2], frames=process.argv[3]?process.argv[3].split(',').map(Number):null;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+D+'/page.html');await p.waitForTimeout(500);
const N=frames||[...Array(498).keys()];
require('fs').mkdirSync(D+'/f',{recursive:true});
for(const f of N){await p.evaluate(t=>render(t),f/30);await p.screenshot({path:D+'/f/'+String(f).padStart(4,'0')+'.jpg',type:'jpeg',quality:94});}
await b.close()})();
