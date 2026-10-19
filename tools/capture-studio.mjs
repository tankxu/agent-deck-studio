// Screenshots of the studio itself (editing mode, story workspace tabs) for docs and decks.
// Usage: node tools/capture-studio.mjs [outdir] [base]   — needs server.py running
import {spawn} from 'node:child_process';
import {writeFileSync,mkdirSync,mkdtempSync} from 'node:fs';
import {tmpdir} from 'node:os';import {join} from 'node:path';
const [out='assets/screens',base='http://127.0.0.1:8793/']=process.argv.slice(2);
mkdirSync(out,{recursive:true});
const chrome=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless=new','--disable-gpu','--hide-scrollbars','--remote-debugging-port=9335',`--user-data-dir=${mkdtempSync(join(tmpdir(),'cap-'))}`,'--window-size=1600,1000','about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let t;for(let i=0;i<50&&!t;i++){await sleep(200);try{t=(await (await fetch('http://127.0.0.1:9335/json')).json()).find(x=>x.type==='page')}catch{}}
const ws=new WebSocket(t.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
let id=0;const P=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);P.get(m.id)?.(m.result);P.delete(m.id)};
const send=(method,params={})=>new Promise(r=>{P.set(++id,r);ws.send(JSON.stringify({id,method,params}))});
const ev=x=>send('Runtime.evaluate',{expression:x,awaitPromise:true});
await send('Emulation.setDeviceMetricsOverride',{width:1600,height:1000,deviceScaleFactor:1,mobile:false});
const shot=async name=>{await sleep(700);writeFileSync(join(out,name),Buffer.from((await send('Page.captureScreenshot')).data,'base64'));console.log('saved',name);};
const go=async url=>{await send('Page.navigate',{url});await sleep(2500);};
// 1. editing mode on a content slide
await go(base+'#4');await ev("document.querySelector('#edit-toggle').click()");await ev("document.querySelector('[data-edit-id]:not(.ds-kicker)')?.closest('.slide.active') && document.querySelector('.slide.active h2[data-edit-id]')?.focus()");await shot('editing.png');
// 2–4. story workspace tabs
for(const [tab,name] of [['narrative','plan-narrative.png'],['outline','plan-outline.png'],['versions','versions.png']]){await go(`${base}?view=plan&tab=${tab}`);await shot(name);}
ws.close();chrome.kill();
