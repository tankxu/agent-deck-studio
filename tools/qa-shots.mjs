// Screenshot every slide at 1600×900, waiting until the slide's images have loaded.
// Usage: node tools/qa-shots.mjs [outdir] [first] [last] [base]   — needs server.py running
import {spawn} from 'node:child_process';
import {writeFileSync,mkdirSync,mkdtempSync,readFileSync} from 'node:fs';
import {tmpdir} from 'node:os';import {join} from 'node:path';
const total=JSON.parse(readFileSync('deck-content.json','utf8')).slides.length;
const [out='.qa',first='1',last=String(total),base=process.env.DECK_URL||'http://127.0.0.1:8793/']=process.argv.slice(2);
mkdirSync(out,{recursive:true});
const chrome=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless=new','--disable-gpu','--hide-scrollbars','--remote-debugging-port=9337',`--user-data-dir=${mkdtempSync(join(tmpdir(),'shots-'))}`,'--window-size=1600,900','about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let t;for(let i=0;i<50&&!t;i++){await sleep(200);try{t=(await (await fetch('http://127.0.0.1:9337/json')).json()).find(x=>x.type==='page')}catch{}}
const ws=new WebSocket(t.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
let id=0;const P=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);P.get(m.id)?.(m.result);P.delete(m.id)};
const send=(method,params={})=>new Promise(r=>{P.set(++id,r);ws.send(JSON.stringify({id,method,params}))});
const value=async x=>(await send('Runtime.evaluate',{expression:x,returnByValue:true}))?.result?.value;
await send('Emulation.setDeviceMetricsOverride',{width:1600,height:900,deviceScaleFactor:1,mobile:false});
for(let n=Number(first);n<=Number(last);n++){
  await send('Page.navigate',{url:`${base}?shot=${n}#${n}`});
  for(let i=0;i<60;i++){await sleep(150);if(await value("document.body?.classList.contains('shot')&&document.fonts.status==='loaded'"))break;}
  // complete ≠ painted: wait for every image on the slide to decode before capturing.
  await send('Runtime.evaluate',{expression:"Promise.all([...document.querySelectorAll('.slide.active img')].map(i=>i.decode().catch(()=>{})))",awaitPromise:true});
  await sleep(150);
  writeFileSync(join(out,String(n).padStart(2,'0')+'.png'),Buffer.from((await send('Page.captureScreenshot')).data,'base64'));
}
console.log(`shots: ${out} (${first}–${last})`);ws.close();chrome.kill();
