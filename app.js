const slides=[...document.querySelectorAll('.slide')];
const tabs=[...document.querySelectorAll('[data-slide]')];
const status=document.querySelector('#save-status');
const fields=[...document.querySelectorAll('[data-edit-id]')];
const dirty=new Set();
const defaults={};
let current=0,editing=false,saveTimer,serverValues={},revision='',connected=false,inflight=null,conflict=null,ready=false;
let slideMetadata=JSON.parse(document.querySelector('#deck-metadata').textContent);
const textOf=el=>el.innerText.replace(/\r/g,'');
fields.forEach(el=>{el.querySelectorAll('br').forEach(br=>br.replaceWith(document.createTextNode('\n')));defaults[el.dataset.editId]=textOf(el);el.spellcheck=false;});
function setStatus(message){status.textContent=message;}
function snapshot(){return Object.fromEntries(fields.map(el=>[el.dataset.editId,textOf(el)]));}
function applyDocument(doc){for(const el of fields){const key=el.dataset.editId;if(!dirty.has(key)&&typeof doc.texts[key]==='string'){el.textContent=doc.texts[key];serverValues[key]=doc.texts[key];}}revision=doc.revision||revision;if(Array.isArray(doc.slides)){slideMetadata=doc.slides;document.querySelector('#deck-metadata').textContent=JSON.stringify(doc.slides).replace(/<\//g,'<\\/');}}
async function loadJSON(manual=false){if(inflight||conflict)return;if(manual&&dirty.size){await save();if(dirty.size)return;}try{const response=await fetch('/api/content',{cache:'no-store'});if(!response.ok)throw Error('读取失败');const doc=await response.json();const changed=revision&&revision!==doc.revision;applyDocument(doc);connected=true;if(manual||changed)setStatus('已读取本地 JSON');return doc;}catch{if(manual)setStatus('读取失败，未覆盖页面内容');return null;}}
function openConflict(data){conflict=data;document.querySelector('#conflict-details').textContent=data.conflicts.map(key=>`${key}\nJSON：${data.document.texts[key]??'（无）'}\n网页：${snapshot()[key]??''}`).join('\n\n');document.querySelector('#conflict-dialog').showModal();setStatus('存在冲突，等待选择');}
async function save(){clearTimeout(saveTimer);if(!ready||conflict)return false;if(inflight){await inflight;return dirty.size&&!conflict?save():!dirty.size;}if(!dirty.size)return true;if(!connected){setStatus('离线修改，请导出网页保存');return false;}
 const values=snapshot();const changes=Object.fromEntries([...dirty].map(key=>[key,{before:serverValues[key]??null,after:values[key]}]));setStatus('正在写入 JSON…');
 inflight=(async()=>{try{const response=await fetch('/api/content',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({changes}),keepalive:true});const doc=await response.json();if(response.status===409){openConflict(doc);return false;}if(!response.ok)throw Error(doc.error||'写入失败');for(const [key,change] of Object.entries(changes)){serverValues[key]=doc.texts[key];if(snapshot()[key]===change.after)dirty.delete(key);}applyDocument(doc);setStatus(dirty.size?'正在保存后续修改…':'已保存至本地 JSON');return true;}catch{setStatus('JSON 保存失败，请重试或导出');return false;}})();
 const result=await inflight;inflight=null;if(result&&dirty.size)return save();return result;
}
for(const [id,useDisk] of [['use-disk',true],['use-current',false]])document.querySelector('#'+id).onclick=async()=>{const data=conflict;conflict=null;for(const key of data.conflicts){serverValues[key]=data.document.texts[key];if(useDisk)dirty.delete(key);}applyDocument(data.document);document.querySelector('#conflict-dialog').close();await save();setStatus(dirty.size?'有修改尚未保存':'已保存至本地 JSON');};
document.querySelector('#conflict-dialog').addEventListener('cancel',e=>e.preventDefault());
function setEditing(value){if(!ready)return;editing=value;document.body.classList.toggle('editing',value);fields.forEach(el=>{el.contentEditable=value?'plaintext-only':'false';if(value){el.setAttribute('tabindex','0');el.setAttribute('aria-label','编辑：'+textOf(el).slice(0,25))}else{el.removeAttribute('tabindex');el.removeAttribute('aria-label')}});document.querySelector('#edit-toggle').textContent=value?'完成编辑':'编辑文字';document.querySelector('#edit-toggle').setAttribute('aria-pressed',String(value));document.querySelector('#editor-tip').hidden=!value;if(!value){document.activeElement?.blur();save();}else setStatus(connected?'点击文字，自动保存到 JSON':'离线编辑，导出网页可保存');}
fields.forEach(el=>{el.addEventListener('input',()=>{dirty.add(el.dataset.editId);setStatus('有修改，正在保存…');clearTimeout(saveTimer);saveTimer=setTimeout(save,400)});el.addEventListener('blur',()=>{if(editing)save()});el.addEventListener('paste',e=>{if(!editing)return;e.preventDefault();document.execCommand('insertText',false,e.clipboardData.getData('text/plain'))});});
function fit(){const view=document.querySelector('.viewport');const style=getComputedStyle(view);const scale=Math.min((view.clientWidth-parseFloat(style.paddingLeft)-parseFloat(style.paddingRight))/1600,view.clientHeight/900);document.querySelector('.frame').style.width=`${1600*scale}px`;document.querySelector('.frame').style.height=`${900*scale}px`;document.querySelector('.deck').style.transform=`scale(${scale})`;}
function show(n){current=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>{s.classList.toggle('active',i===current);s.setAttribute('aria-hidden',String(i!==current));});tabs.forEach((t,i)=>{t.classList.toggle('selected',i===current);t.setAttribute('aria-current',i===current?'page':'false')});document.querySelector('#slide-label').textContent=slides[current].dataset.name;document.querySelector('#page-count').textContent=`${String(current+1).padStart(2,'0')} / ${String(slides.length).padStart(2,'0')}`;document.querySelector('#slide-select').value=String(current);document.querySelector('#prev').disabled=current===0;document.querySelector('#next').disabled=current===slides.length-1;history.replaceState(null,'',`#${current+1}`);}
tabs.forEach(t=>t.onclick=()=>{show(+t.dataset.slide);document.querySelector('#outline-dialog').close();});document.querySelector('#slide-select').onchange=e=>show(+e.target.value);document.querySelector('#prev').onclick=()=>show(current-1);document.querySelector('#next').onclick=()=>show(current+1);
document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();save();return}if(document.body.classList.contains('planning-mode'))return;if(e.target.isContentEditable||['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)||e.target.closest('button,a,dialog'))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(current-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key.toLowerCase()==='f')toggleFullscreen()});
// Play mode: full screen with no viewer chrome; × appears near the top-right corner, Esc exits.
function startPlay(){if(editing)setEditing(false);document.body.classList.add('playing');fit();const el=document.documentElement;if(el.requestFullscreen&&!document.fullscreenElement)el.requestFullscreen().catch(()=>{}).finally(fit);}
function exitPlay(){document.body.classList.remove('playing','play-idle');document.querySelector('#play-exit').classList.remove('show');if(document.fullscreenElement)document.exitFullscreen().catch(()=>{});fit();}
async function toggleFullscreen(){document.body.classList.contains('playing')?exitPlay():startPlay();}document.querySelector('#fullscreen').onclick=toggleFullscreen;
document.querySelector('#edit-toggle').onclick=()=>setEditing(!editing);document.querySelector('#finish-edit').onclick=()=>setEditing(false);document.querySelector('#reload-json').onclick=()=>loadJSON(true);
async function readAsset(url){const response=await fetch(url);if(!response.ok)throw Error('资源读取失败');return response;}
async function asDataURL(url){const blob=await(await readAsset(url)).blob();return new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=reject;reader.readAsDataURL(blob);});}
document.querySelector('#export-html').onclick=async()=>{const button=document.querySelector('#export-html');button.disabled=true;await save();setStatus('正在打包网页与配图…');try{const clone=document.documentElement.cloneNode(true);clone.querySelector('body').classList.remove('editing');clone.querySelectorAll('[data-edit-id]').forEach(el=>{el.removeAttribute('contenteditable');el.removeAttribute('tabindex');el.removeAttribute('aria-label');});clone.querySelector('#editor-tip').hidden=true;clone.querySelectorAll('dialog').forEach(dialog=>dialog.removeAttribute('open'));clone.querySelector('#edit-toggle').textContent='编辑文字';clone.querySelector('#edit-toggle').setAttribute('aria-pressed','false');clone.querySelector('#export-html').removeAttribute('disabled');clone.querySelector('#save-status').textContent='离线副本';
 const stylesheet=document.querySelector('link[rel=stylesheet]');if(stylesheet){let css=await(await readAsset(stylesheet.href)).text();const paths=[...css.matchAll(/url\(["']?([^"')]+)["']?\)/g)].map(m=>m[1]);for(const path of new Set(paths)){if(!path.startsWith('data:'))css=css.split(path).join(await asDataURL(new URL(path,stylesheet.href).href));}const style=document.createElement('style');style.textContent=css;clone.querySelector('link[rel=stylesheet]').replaceWith(style);}
 await Promise.all([...clone.querySelectorAll('img')].map(async img=>{if(img.getAttribute('src')&&!img.src.startsWith('data:'))img.src=await asDataURL(img.src)}));
 const source=document.querySelector('script[src]');if(source){const script=document.createElement('script');script.textContent=await(await readAsset(source.src)).text();clone.querySelector('script[src]').replaceWith(script);}
 const blob=new Blob(['<!doctype html>\n'+clone.outerHTML],{type:'text/html;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=(document.title.split('·')[0].trim()||'deck')+'.html';a.click();setTimeout(()=>URL.revokeObjectURL(url),30000);setStatus('已导出文字、字体及配图');}catch(e){console.error(e);setStatus('导出失败，请重试');}finally{button.disabled=false;}};
window.addEventListener('beforeunload',e=>{if(dirty.size){save();e.preventDefault();e.returnValue='';}});window.addEventListener('resize',fit);document.addEventListener('fullscreenchange',fit);show((Number(location.hash.slice(1))||1)-1);fit();
async function initialize(){setStatus('正在读取本地 JSON…');document.querySelector('#edit-toggle').disabled=true;if(location.protocol==='file:'){serverValues=snapshot();ready=true;document.querySelector('#edit-toggle').disabled=false;document.querySelector('#reload-json').hidden=true;document.querySelector('#editor-tip').firstChild.textContent='离线编辑 · 修改后请导出网页保存 ';setStatus('离线副本，修改后请导出');return;}
 const doc=await loadJSON();if(!doc){setStatus('JSON 读取失败，编辑暂不可用');return;}
 ready=true;document.querySelector('#edit-toggle').disabled=false;if(!dirty.size)setStatus('已连接本地 deck-content.json');setInterval(()=>{if(!document.hidden&&!inflight&&!conflict)loadJSON();},2500);
}
initialize();

// Presentation navigation, source notes, and full-size screenshot inspection.
document.querySelector('#outline-toggle').onclick=()=>document.querySelector('#outline-dialog').showModal();
document.querySelector('#notes-toggle').onclick=()=>{const meta=slideMetadata.find(x=>x.id===slides[current].dataset.pageId)||{};document.querySelector('#notes-title').textContent=`${String(current+1).padStart(2,'0')} · ${meta.name||'讲稿备注'}`;document.querySelector('#notes-body').textContent=meta.notes||'暂无备注';const sources=document.querySelector('#notes-sources');sources.replaceChildren();for(const source of meta.sources||[]){const a=document.createElement('a');a.textContent=source.title;a.href=source.url;a.target='_blank';a.rel='noopener noreferrer';sources.append(a)}document.querySelector('#notes-dialog').showModal();};
document.querySelectorAll('[data-close]').forEach(button=>button.onclick=()=>document.getElementById(button.dataset.close).close());
document.querySelectorAll('.zoom-shot').forEach(button=>button.onclick=()=>{if(editing)return;const img=button.querySelector('img');document.querySelector('#zoom-image').src=img.src;document.querySelector('#zoom-image').alt=img.alt;document.querySelector('#zoom-caption').textContent=img.alt;document.querySelector('#image-dialog').showModal();});
let touchStart=null;document.querySelector('.frame').addEventListener('touchstart',e=>{if(!editing&&e.touches.length===1)touchStart=[e.touches[0].clientX,e.touches[0].clientY];else touchStart=null;},{passive:true});document.querySelector('.frame').addEventListener('touchend',e=>{if(!touchStart||editing)return;const dx=e.changedTouches[0].clientX-touchStart[0],dy=e.changedTouches[0].clientY-touchStart[1];if(Math.abs(dx)>65&&Math.abs(dx)>Math.abs(dy)*1.5)show(current+(dx<0?1:-1));touchStart=null;},{passive:true});

// Story planning is part of this studio and shares the same JSON save/conflict flow.
const planningPanel=document.querySelector('#planning-panel');
const planningToggle=document.querySelector('#planning-toggle');
function selectPlanView(view){
 const chosen=['narrative','outline','versions','coverage','research'].includes(view)?view:'narrative';
 document.querySelectorAll('[data-plan-view]').forEach(button=>button.setAttribute('aria-selected',String(button.dataset.planView===chosen)));
 document.querySelectorAll('.plan-section').forEach(section=>section.hidden=section.id!=='plan-'+chosen);
 const url=new URL(location.href);url.searchParams.set('tab',chosen);history.replaceState(null,'',url);
 planningPanel.scrollTop=0;
}
function setPlanning(open){
 document.body.classList.toggle('planning-mode',open);planningPanel.hidden=!open;
 planningToggle.setAttribute('aria-pressed',String(open));planningToggle.textContent=open?'返回演示':'叙事与大纲';
 const url=new URL(location.href);if(open)url.searchParams.set('view','plan');else{url.searchParams.delete('view');url.searchParams.delete('tab');}history.replaceState(null,'',url);
 document.querySelector('#export-html').hidden=open;document.querySelector('#notes-toggle').hidden=open;
 if(!open)fit();
}
planningToggle.onclick=()=>setPlanning(!document.body.classList.contains('planning-mode'));
document.querySelectorAll('[data-plan-view]').forEach(button=>button.onclick=()=>selectPlanView(button.dataset.planView));
document.querySelectorAll('[data-plan-anchor]').forEach(button=>button.onclick=()=>document.getElementById(button.dataset.planAnchor).scrollIntoView({behavior:'smooth',block:'start'}));
const initialPlanView=new URLSearchParams(location.search);if(initialPlanView.get('view')==='plan'){setPlanning(true);selectPlanView(initialPlanView.get('tab'));}
// PDF export renders in the page itself: each slide is drawn through SVG foreignObject
// (the browser's own layout, so masks, object-fit and fonts match the screen), rasterised
// to JPEG and packed into a 16:9 PDF by the small writer below. No print dialog, no libraries.
const PDF_SCALE=2,PDF_W=1600,PDF_H=900;
const assetCache=new Map();
function inlineAsset(url){const abs=new URL(url,location.href).href;if(!assetCache.has(abs))assetCache.set(abs,asDataURL(abs).catch(()=>url));return assetCache.get(abs);}
async function inlineCssUrls(css,base){
 const urls=[...new Set([...css.matchAll(/url\(\s*["']?([^"')]+)["']?\s*\)/g)].map(m=>m[1]).filter(u=>!u.startsWith('data:')))];
 const map=Object.fromEntries(await Promise.all(urls.map(async u=>[u,await inlineAsset(new URL(u,base).href)])));
 return css.replace(/url\(\s*["']?([^"')]+)["']?\s*\)/g,(m,u)=>map[u]?`url("${map[u]}")`:m);
}
let pdfCssPromise=null;
function deckCss(){
 pdfCssPromise??=Promise.all([...document.querySelectorAll('link[rel=stylesheet]')].map(async link=>inlineCssUrls(await (await readAsset(link.href)).text(),link.href))).then(parts=>parts.join('\n'));
 return pdfCssPromise;
}
async function slideToJpeg(slide,css){
 const clone=slide.cloneNode(true);
 clone.classList.add('active');clone.style.display='block';clone.style.position='relative';
 clone.querySelectorAll('[contenteditable]').forEach(el=>el.removeAttribute('contenteditable'));
 await Promise.all([...clone.querySelectorAll('img')].map(async img=>{img.removeAttribute('loading');img.src=await inlineAsset(img.getAttribute('src'));}));
 const holder=document.createElement('div');holder.setAttribute('xmlns','http://www.w3.org/1999/xhtml');holder.className='deck';
 holder.style.cssText=`width:${PDF_W}px;height:${PDF_H}px;position:relative;transform:none`;holder.appendChild(clone);
 const style=document.createElement('style');style.textContent=css;
 const xhtml=new XMLSerializer().serializeToString(holder);const cssText=new XMLSerializer().serializeToString(style);
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${PDF_W}" height="${PDF_H}"><foreignObject x="0" y="0" width="100%" height="100%"><div xmlns="http://www.w3.org/1999/xhtml">${cssText}${xhtml}</div></foreignObject></svg>`;
 const img=new Image();img.decoding='sync';
 // data: URL, not blob: — Chrome taints the canvas for blob-loaded foreignObject SVGs.
 img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);
 const loaded=new Promise((ok,fail)=>{img.onload=ok;img.onerror=()=>fail(Error('页面渲染失败'));});
 await Promise.race([img.decode().catch(()=>loaded),new Promise((_,fail)=>setTimeout(()=>fail(Error('页面渲染超时')),30000))]);
 const canvas=document.createElement('canvas');canvas.width=PDF_W*PDF_SCALE;canvas.height=PDF_H*PDF_SCALE;
 const ctx=canvas.getContext('2d');ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);
 // Safari can paint foreignObject images a frame late; a second draw is cheap insurance.
 ctx.drawImage(img,0,0,canvas.width,canvas.height);await new Promise(r=>setTimeout(r,30));ctx.drawImage(img,0,0,canvas.width,canvas.height);
 const blob=await new Promise((ok,fail)=>canvas.toBlob(b=>b?ok(b):fail(Error('无法生成图片')),'image/jpeg',0.9));
 return {bytes:new Uint8Array(await blob.arrayBuffer()),w:canvas.width,h:canvas.height};
}
// Minimal PDF writer: one full-bleed DCT (JPEG) image per page, page size 1200×675 pt (16:9).
function buildPdf(pages){
 const enc=new TextEncoder(),chunks=[],offsets=[];let size=0;
 const push=part=>{const b=typeof part==='string'?enc.encode(part):part;chunks.push(b);size+=b.length;};
 const obj=(n,body)=>{offsets[n]=size;push(`${n} 0 obj\n`);body();push('\nendobj\n');};
 const PW=1200,PH=675,n=pages.length,kids=[];
 push('%PDF-1.4\n%\xE2\xE3\xCF\xD3\n');
 for(let i=0;i<n;i++)kids.push(`${3+i*3} 0 R`);
 obj(1,()=>push('<< /Type /Catalog /Pages 2 0 R >>'));
 obj(2,()=>push(`<< /Type /Pages /Count ${n} /Kids [${kids.join(' ')}] >>`));
 pages.forEach((pg,i)=>{
  const page=3+i*3,content=page+1,image=page+2,stream=`q ${PW} 0 0 ${PH} 0 0 cm /Im0 Do Q`;
  obj(page,()=>push(`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${PW} ${PH}] /Resources << /XObject << /Im0 ${image} 0 R >> >> /Contents ${content} 0 R >>`));
  obj(content,()=>{push(`<< /Length ${stream.length} >>\nstream\n`);push(stream);push('\nendstream');});
  obj(image,()=>{push(`<< /Type /XObject /Subtype /Image /Width ${pg.w} /Height ${pg.h} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${pg.bytes.length} >>\nstream\n`);push(pg.bytes);push('\nendstream');});
 });
 const total=3+n*3,xref=size;
 push(`xref\n0 ${total}\n0000000000 65535 f \n`);
 for(let i=1;i<total;i++)push(String(offsets[i]).padStart(10,'0')+' 00000 n \n');
 push(`trailer\n<< /Size ${total} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`);
 return new Blob(chunks,{type:'application/pdf'});
}
async function renderDeckPdf(onProgress=()=>{}){
 const css=await deckCss(),pages=[];
 for(const [i,slide] of slides.entries()){onProgress(i+1,slides.length);pages.push(await slideToJpeg(slide,css));}
 return buildPdf(pages);
}
window.renderDeckPdf=renderDeckPdf;
document.querySelector('#export-pdf')?.addEventListener('click',async()=>{
 const button=document.querySelector('#export-pdf');if(button.disabled)return;
 if(editing)setEditing(false);button.disabled=true;
 try{
  const pdf=await renderDeckPdf((i,n)=>setStatus(`正在生成 PDF ${i}/${n}…`));
  const a=document.createElement('a');a.href=URL.createObjectURL(pdf);a.download=''+(document.title.split('·')[0].trim()||'deck')+'.pdf';
  document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),60000);
  setStatus(`PDF 已生成 · ${(pdf.size/1048576).toFixed(1)} MB`);
 }catch(error){console.error(error);setStatus('PDF 生成失败：'+(error.message||error));}
 finally{button.disabled=false;}
});
// ?pdftest=1 (headless QA): renders the PDF and exposes size and page images for checking.
if(new URLSearchParams(location.search).get('pdftest'))(async()=>{try{
 const n=Number(new URLSearchParams(location.search).get('pages'))||slides.length;
 const css=await deckCss(),pages=[];
 for(const [i,slide] of [...slides].slice(0,n).entries()){document.body.dataset.pdfProgress=i+1;pages.push(await slideToJpeg(slide,css));}
 const pdf=buildPdf(pages);
 document.body.dataset.pdfBytes=pdf.size;document.body.dataset.pdfPages=pages.length;
 const b64=await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result);fr.readAsDataURL(pdf);});
 const out=document.createElement('textarea');out.id='pdf-out';out.value=b64;document.body.appendChild(out);
 document.title='PDF-READY';
}catch(error){document.body.dataset.pdfError=String(error&&error.stack||error);document.title='PDF-ERROR';}})();
// ?print=1 lays every slide out for headless PDF export (tools/export-pdf.sh).
if(new URLSearchParams(location.search).get('print'))document.body.classList.add('print-all');
// QA capture mode: ?shot=N renders slide N alone at 1600×900 for headless screenshots.
(()=>{const n=Number(new URLSearchParams(location.search).get('shot'));if(!n)return;document.body.classList.add('shot');show(n-1);})();

// Leaving browser full screen (Esc, system gesture) also leaves play mode.
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement&&document.body.classList.contains('playing'))exitPlay();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.body.classList.contains('playing')){e.preventDefault();exitPlay();}});
document.querySelector('#play-exit').onclick=exitPlay;
let playIdle;
document.addEventListener('mousemove',e=>{if(!document.body.classList.contains('playing'))return;
 document.querySelector('#play-exit').classList.toggle('show',e.clientX>innerWidth-160&&e.clientY<160);
 document.body.classList.remove('play-idle');clearTimeout(playIdle);playIdle=setTimeout(()=>document.body.classList.add('play-idle'),2000);});
