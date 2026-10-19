"""Build index.html and deck-content.json from deck/deck.py.

Run: python3 tools/build.py
The deck file composes slides from helpers in tools/components.py. Every visible string goes
through T(key, default) so it is editable in the browser and stored in deck-content.json.
"""
from pathlib import Path
import html, json, os, re

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'deck-content.json'
old = json.loads(CONTENT.read_text(encoding='utf-8')) if CONTENT.exists() else {}
old.setdefault('schemaVersion', 1)
texts = dict(old.get('texts', {}))
previous_defaults = old.get('defaults', {})
defaults = {}
slides = []
CONFIG = {'title': 'Untitled deck', 'lang': 'zh-CN', 'document_id': 'deck', 'studio_name': 'Agent Deck Studio', 'footer': ''}

def T(key, value, tag='span', cls=''):
    """Editable text. A JSON value still equal to its previous default was never edited by hand,
    so it follows the new default; hand edits are kept."""
    if key in texts and key in previous_defaults and texts[key] == previous_defaults[key]:
        texts[key] = value
    defaults[key] = value
    value = texts.setdefault(key, value)
    return f'<{tag} data-edit-id="{key}"' + (f' class="{cls}"' if cls else '') + '>' + html.escape(value).replace('\n', '<br>') + f'</{tag}>'

def add(id, name, section, content, theme='paper', notes='', sources=None, **meta):
    footer = '<footer class="slide-bottom"><span>' + html.escape(CONFIG['footer']) + '</span><span>00</span></footer>'
    slides.append({'id': id, 'name': name, 'section': section, 'notes': notes, 'sources': sources or [], **meta,
                   'html': f'<section class="slide {theme}" data-page-id="{id}" data-name="{html.escape(name)}" aria-label="{html.escape(name)}">' + content + footer + '</section>'})

exec((ROOT / 'tools/components.py').read_text(encoding='utf-8'))
exec((ROOT / 'deck/deck.py').read_text(encoding='utf-8'))

# Page numbers, first-slide visibility and chapter links come from the final order only.
for i, s in enumerate(slides):
    s['html'] = re.sub(r'(<footer class="slide-bottom"><span>[^<]*</span><span>)\d+(</span>)', lambda m: m[1] + f'{i + 1:02d}' + m[2], s['html'], count=1)
    s['html'] = s['html'].replace('<section class="slide ', '<section class="slide ' + ('active ' if i == 0 else ''), 1)
    s['html'] = s['html'].replace('aria-label="', f'aria-label="第{i + 1}页：', 1)
    for j, t in enumerate(slides):
        s['html'] = s['html'].replace('data-chapter="' + t['id'] + '"', 'data-slide="' + str(j) + '"')

exec((ROOT / 'tools/studio_plan.py').read_text(encoding='utf-8'))

options = ''.join(f'<option value="{i}">{i + 1:02d} · {html.escape(s["name"])}</option>' for i, s in enumerate(slides))
menu = ''.join(f'<button data-slide="{i}"><span>{i + 1:02d}</span><strong>{html.escape(s["name"])}</strong><small>{html.escape(s["section"])}</small></button>' for i, s in enumerate(slides))
html_doc='''<!doctype html><html lang="'''+CONFIG['lang']+'''"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(CONFIG['title'])+'''</title><link rel="stylesheet" href="studio.css"><link rel="stylesheet" href="components.css"></head><body data-document-id="'''+CONFIG['document_id']+'''"><header class="viewer-head"><a class="viewer-brand" href="#1">'''+html.escape(CONFIG['studio_name'])+'''<span>DECK STUDIO</span></a><div class="tools"><span id="save-status" role="status" aria-live="polite">正在读取 JSON…</span><button id="planning-toggle" aria-pressed="false">叙事与大纲</button><button id="edit-toggle" aria-pressed="false">编辑文字</button><button id="reload-json">重读 JSON</button><button id="export-html">导出网页</button><button id="export-pdf">导出 PDF</button><button id="notes-toggle">讲稿</button><button id="fullscreen" aria-label="全屏播放">▶ 播放</button></div></header><main class="viewport"><div class="frame"><div class="deck">'''+''.join(s['html'] for s in slides)+'''</div></div></main><footer class="viewer-nav"><div class="nav-label"><span class="live-dot"></span><span id="slide-label"></span></div><div class="nav-center"><button id="outline-toggle">目录</button><select id="slide-select" aria-label="跳转页面">'''+options+'''</select><span class="hint">← → 翻页 · 点击截图放大</span></div><div class="arrows"><button id="prev" aria-label="上一页">←</button><span id="page-count"></span><button id="next" aria-label="下一页">→</button></div></footer>'''+plan_html+'''<div class="editor-tip" id="editor-tip" hidden>点击文字编辑 · 自动保存到本地 deck-content.json <button id="finish-edit">完成编辑</button></div><dialog id="outline-dialog"><div class="dialog-head"><h2>目录</h2><button data-close="outline-dialog">关闭</button></div><div class="outline-grid">'''+menu+'''</div></dialog><dialog id="notes-dialog"><div class="dialog-head"><h2 id="notes-title">讲稿备注</h2><button data-close="notes-dialog">关闭</button></div><p id="notes-body"></p><div id="notes-sources"></div></dialog><dialog id="image-dialog"><button class="image-close" data-close="image-dialog">关闭 ×</button><img id="zoom-image" alt="图片放大"><p id="zoom-caption"></p></dialog><dialog id="conflict-dialog"><h2>这段文字在 JSON 中也有修改</h2><p>其他修改已保留，请选择如何处理冲突内容。</p><pre id="conflict-details"></pre><div><button id="use-disk">使用 JSON 内容</button><button id="use-current">保留网页修改</button></div></dialog><script id="deck-metadata" type="application/json">'''+json.dumps([{k:v for k,v in s.items() if k!='html'} for s in slides],ensure_ascii=False).replace('</','<\\/')+'''</script><button id="play-exit" aria-label="退出播放" title="退出播放（Esc）">×</button><script src="app.js"></script></body></html>'''
(ROOT / 'index.html').write_text(html_doc, encoding='utf-8')
active = list(dict.fromkeys(re.findall(r'data-edit-id="([^"]+)"', ''.join(s['html'] for s in slides) + plan_html)))
old.update(title=CONFIG['title'], texts=texts, defaults={k: v for k, v in defaults.items()},
           slides=[{k: v for k, v in s.items() if k != 'html'} for s in slides], activeTextKeys=active)
tmp = ROOT / '.deck-build.tmp'
tmp.write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
os.replace(tmp, CONTENT)
print(f'{len(slides)} pages; {len(active)} editable fields')
