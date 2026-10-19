// Headless check of the in-page PDF export: opens ?pdftest=1 over CDP, waits until the
// page has built the PDF, saves it. Usage: node tools/qa-pdf.mjs out.pdf [pages] [url]
import {spawn} from 'node:child_process';
import {writeFileSync,mkdtempSync} from 'node:fs';
import {tmpdir} from 'node:os';import {join} from 'node:path';
const [out='deck-test.pdf',pages='',base='http://127.0.0.1:8793/']=process.argv.slice(2);
const chrome=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless=new','--disable-gpu','--remote-debugging-port=9333',`--user-data-dir=${mkdtempSync(join(tmpdir(),'qapdf-'))}`,'--window-size=1600,900','about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let target;for(let i=0;i<50&&!target;i++){await sleep(200);try{target=(await (await fetch('http://127.0.0.1:9333/json')).json()).find(t=>t.type==='page');}catch{}}
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
let id=0;const pending=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(pending.has(m.id)){pending.get(m.id)(m.result);pending.delete(m.id);}};
const send=(method,params={})=>new Promise(r=>{pending.set(++id,r);ws.send(JSON.stringify({id,method,params}));});
const evalJs=async expr=>(await send('Runtime.evaluate',{expression:expr,returnByValue:true}))?.result?.value;
// DECK_COOKIE=name=value logs in to the password-gated Pages copy.
if(process.env.DECK_COOKIE){const [name,...v]=process.env.DECK_COOKIE.split('=');await send('Network.setCookie',{name,value:v.join('='),url:base});}
await send('Page.navigate',{url:`${base}?pdftest=1${pages?'&pages='+pages:''}`});
const t0=Date.now();let title='';await send('Runtime.enable');
while(Date.now()-t0<Number(process.env.QA_TIMEOUT||240000)){await sleep(1000);title=await evalJs('document.title');if(title==='PDF-READY'||title==='PDF-ERROR')break;}
if(title!=='PDF-READY'){console.error(title||'timeout',await evalJs('document.body.dataset.pdfError||""'),'progress:',await evalJs('document.body.dataset.pdfProgress||""'),await evalJs('document.body.dataset.pdfError||""'));process.exit(1);}
const b64=await evalJs("document.getElementById('pdf-out').value.split(',')[1]");
writeFileSync(out,Buffer.from(b64,'base64'));
console.log(`PDF ${out}: ${await evalJs('document.body.dataset.pdfPages')} pages, ${(Buffer.from(b64,'base64').length/1048576).toFixed(1)} MB, ${((Date.now()-t0)/1000).toFixed(0)}s`);
ws.close();chrome.kill();
