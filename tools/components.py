# Slide helpers. Each returns an HTML string; layouts are styled by components.css (scoped to .ds).
# Conventions: `k` is an editable-text key prefix; every visible string goes through E()/T().

def E(k, v, tag='span', cls=''):
    """Editable text under the deck's own namespace."""
    return T('d.' + k, v, tag, cls)

def esc(s):
    return html.escape(s)

def brand():
    return CONFIG.get('brand_html') or '<div class="wordmark"><span>' + esc(CONFIG['studio_name']) + '</span></div>'

def S(id, name, section, body, theme='paper', notes='', kind='内容', visual='', origin=''):
    """Add one slide. `kind`, `visual` and `origin` feed the auto-generated outline in the studio."""
    add(id, name, section, body, theme + ' ds', notes, [], kind=kind, visual=visual, origin=origin, chapter=section)

def top(id, kicker):
    return '<div class="ds-top">' + E(id + '.kicker', kicker, 'span', 'ds-kicker') + brand() + '</div>'

def H(id, title, sub=''):
    return '<header class="ds-head">' + E(id + '.title', title, 'h2') + (E(id + '.sub', sub, 'p') if sub else '') + '</header>'

def img(src, alt, cls=''):
    return f'<img class="{cls}" src="assets/{src}" alt="{esc(alt)}">'

def shot(src, label, cls=''):
    """Screenshot that opens full size on click."""
    return f'<figure class="ds-shot {cls}"><button class="zoom-shot" aria-label="放大：{esc(label)}"><img src="assets/{src}" alt="{esc(label)}"></button><figcaption>{esc(label)}</figcaption></figure>'

def phone_img(src, label, cls=''):
    return f'<figure class="ds-phone-shot {cls}"><button class="zoom-shot" aria-label="放大：{esc(label)}"><img src="assets/{src}" alt="{esc(label)}"></button><figcaption>{esc(label)}</figcaption></figure>'

CONCEPT_PROMPTS = {}
def concept(key, label, prompt, cls=''):
    """Concept-art slot: shows assets/concept/<key>.jpg when present, else a labelled placeholder.
    Prompts are collected into deck-content.json (conceptPrompts) for an image model to render."""
    CONCEPT_PROMPTS[key] = prompt
    if (ROOT / 'assets/concept' / (key + '.jpg')).exists():
        return f'<figure class="ds-concept {cls}"><img src="assets/concept/{key}.jpg" alt="{esc(label)}"></figure>'
    return f'<figure class="ds-concept ds-concept-pending {cls}"><span>{esc(label)}</span><small>概念图待生成</small></figure>'

def chapter(id, n, label, title, sub, theme='ink', art=''):
    body = ('<div class="ds-chapter-art">' + art + '</div>' if art else '') + '<div class="cover-brand">' + brand() + '</div><div class="ds-chapter-n">' + n + '</div><div class="ds-chapter-copy">' + E(id + '.label', label, 'p', 'ds-eyebrow') + E(id + '.title', title, 'h2') + E(id + '.sub', sub, 'p') + '</div>'
    S(id, label, label, body, theme, sub, '章节', '章节页：编号、标题与一句说明')

def num(k, n, label, cls=''):
    return '<div class="ds-num ' + cls + '">' + E(k + '.n', n, 'strong') + E(k + '.l', label, 'span') + '</div>'

ICONS = {'chat':'<path d="M4 5h16v11H9l-5 4z"/>','users':'<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14.3c3 .1 5.5 2.5 5.5 5.7"/>','user':'<circle cx="12" cy="8" r="3.6"/><path d="M5 20c0-3.9 3.1-7 7-7s7 3.1 7 7"/>','apps':'<rect x="4" y="4" width="7" height="7" rx="2"/><rect x="13" y="4" width="7" height="7" rx="2"/><rect x="4" y="13" width="7" height="7" rx="2"/><rect x="13" y="13" width="7" height="7" rx="2"/>','bot':'<rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01"/>','shield':'<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>','bolt':'<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>','key':'<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M16 7l3 3"/>','flag':'<path d="M5 21V4M5 4h12l-2 4 2 4H5"/>','chart':'<path d="M4 19V5M4 19h16M8 15v-4M12 15V8M16 15v-6"/>','check':'<path d="M5 12.5l4.5 4.5L19 7"/>','eye':'<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>','code':'<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>','spark':'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>','lock':'<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/>','arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>','doc':'<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>','image':'<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-9 8"/>','layers':'<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>','play':'<path d="M7 4l13 8-13 8z"/>','download':'<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>','history':'<path d="M3 12a9 9 0 103-6.7L3 8"/><path d="M3 3v5h5M12 7v5l3 2"/>','edit':'<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M14 6l4 4"/>','sync':'<path d="M20 12a8 8 0 01-14 5.3M4 12a8 8 0 0114-5.3"/><path d="M18 3v4h-4M6 21v-4h4"/>','camera':'<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>','search':'<circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/>','folder':'<path d="M3 6h7l2 2h9v11H3z"/>','terminal':'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3M12 15h5"/>','globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>'}
def ICON(name):
    return '<svg class="ds-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[name] + '</svg>'

def flow(k, steps, cls=''):
    """Horizontal process: steps = [(icon, title, sub)]."""
    out = '<div class="ds-flow ' + cls + '">'
    for i, (ic, a, b) in enumerate(steps):
        out += ('<i class="ds-flow-arrow">' + ICON('arrow') + '</i>' if i else '') + '<div class="ds-step"><div class="ds-step-ic">' + ICON(ic) + '</div>' + E(f'{k}.{i}.t', a, 'b') + E(f'{k}.{i}.s', b, 'span') + '</div>'
    return out + '</div>'

def bars(k, items, cls=''):
    """Vertical bar chart: items = [(label, value, value_label)]."""
    m = max(v for _, v, _ in items)
    return '<div class="ds-bars ' + cls + '">' + ''.join('<div class="ds-bar"><span class="ds-bar-v">' + E(f'{k}.{i}.v', vl, 'b') + '</span><i style="height:' + f'{max(3, v / m * 100):.1f}' + '%"></i>' + E(f'{k}.{i}.l', lab, 'span') + '</div>' for i, (lab, v, vl) in enumerate(items)) + '</div>'

def hbars(k, items, cls=''):
    m = max(v for _, v, _ in items)
    return '<div class="ds-hbars ' + cls + '">' + ''.join('<div class="ds-hbar">' + E(f'{k}.{i}.l', lab, 'span') + '<div><i style="width:' + f'{v / m * 100:.1f}' + '%"></i></div>' + E(f'{k}.{i}.v', vl, 'b') + '</div>' for i, (lab, v, vl) in enumerate(items)) + '</div>'

def donuts(k, items):
    """Percent rings: items = [(percent, value_label, label)]."""
    return '<div class="ds-donuts">' + ''.join('<div class="ds-donut" style="--p:' + str(p) + '">' + E(f'{k}.{i}.v', v, 'b') + E(f'{k}.{i}.l', l, 'span') + '</div>' for i, (p, v, l) in enumerate(items)) + '</div>'

def card(k, ic, t, s, cls=''):
    return '<div class="ds-card ' + cls + '"><div class="ds-card-ic">' + ICON(ic) + '</div>' + E(k + '.t', t, 'h3') + E(k + '.s', s, 'p') + '</div>'

def tags(k, items):
    return '<div class="ds-tags">' + ''.join(E(f'{k}.{i}', x, 'span', 'ds-tag') for i, x in enumerate(items)) + '</div>'

def code(k, text):
    """Monospace block for commands; editable like any other text."""
    return '<div class="ds-code">' + E(k, text, 'pre') + '</div>'

def screen(file, label, cls=''):
    """Screenshot slot under assets/screens/: the image once captured (tools/capture-studio.mjs), a placeholder before."""
    if (ROOT / 'assets/screens' / file).exists():
        return shot('screens/' + file, label, cls)
    return f'<figure class="ds-concept ds-concept-pending {cls}"><span>{esc(label)}</span><small>截图待生成</small></figure>'
