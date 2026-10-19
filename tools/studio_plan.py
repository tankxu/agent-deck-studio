# Story workspace (“叙事与大纲”): narrative (editable), page outline (generated from the slides),
# version history with the questions each round raised, and where each source point landed.
# Data lives in deck/narrative.py, deck/versions.py and deck/coverage.py (optional).

def _load(name, default):
    path = ROOT / 'deck' / name
    scope = {}
    if path.exists():
        exec(path.read_text(encoding='utf-8'), scope)
    return scope, default

_n, _ = _load('narrative.py', None)
NARRATIVE = _n.get('NARRATIVE', [])
THESIS = _n.get('THESIS', '')
RULE = _n.get('RULE', '')
VERSIONS = _load('versions.py', None)[0].get('VERSIONS', [])
COVERAGE = _load('coverage.py', None)[0].get('COVERAGE', [])

def P(key, value, tag='p', cls=''):
    return T('plan.' + key, value, tag, cls)

def plan_section(id, title, body):
    return '<section class="plan-section" id="plan-' + id + '"' + ('' if id == 'narrative' else ' hidden') + '><div class="plan-section-head"><h2>' + html.escape(title) + '</h2></div>' + body + '</section>'

def plan_field(label, value_html):
    return '<div class="plan-field"><span class="plan-field-label">' + label + '</span>' + value_html + '</div>'

def _p(text):
    return '<p>' + html.escape(text).replace('\n', '<br>') + '</p>'

page_no = {s['id']: i + 1 for i, s in enumerate(slides)}

narrative_html = (P('thesis', THESIS, 'p', 'plan-thesis') if THESIS else '') + ('<div class="plan-editing-rule">' + P('rule', RULE) + '</div>' if RULE else '') + '<div class="plan-acts">' + ''.join(
    '<article><span class="plan-step">' + f'{i + 1:02d}' + '</span><div>' + P('narrative.' + id + '.title', title, 'h3') + P('narrative.' + id + '.body', body) + plan_field('讲述重点', P('narrative.' + id + '.note', note)) + '</div></article>'
    for i, (id, title, body, note) in enumerate(NARRATIVE)) + '</div>'

chapters = list(dict.fromkeys(s.get('chapter', s['section']) for s in slides))
outline_html = '<p class="plan-auto-note">由演示页自动生成：页面文字在演示里点“编辑文字”修改，讲稿与依据见每页“讲稿”。</p><div class="plan-chapter-links">' + ''.join(
    '<button data-plan-anchor="plan-page-' + str(next(i + 1 for i, s in enumerate(slides) if s.get('chapter', s['section']) == c)) + '">' + html.escape(c) + '</button>' for c in chapters) + '</div>'
for i, s in enumerate(slides, 1):
    fields = [('讲述要点', s.get('notes', '')), ('画面', s.get('visual', '')), ('依据', s.get('origin', ''))]
    outline_html += '<article class="plan-page" id="plan-page-' + str(i) + '"><div class="plan-page-number">' + f'{i:02d}' + '<small>' + html.escape(s.get('kind', '')) + '</small></div><div class="plan-page-copy"><span class="plan-kicker">' + html.escape(s.get('chapter', s['section'])) + '</span><h3>' + html.escape(s['name']) + '</h3>' + ''.join(plan_field(label, _p(value)) for label, value in fields if value) + '</div></article>'

def _questions(qs):
    return ''.join('<li><b>' + html.escape(who) + '</b>' + html.escape(q) + ('<em>处理：' + html.escape(a) + '</em>' if a else '') + '</li>' for who, q, a in qs)
versions_html = '<div class="plan-versions">' + ''.join(
    '<article class="plan-version"><div class="plan-version-head"><span>' + html.escape(v['version']) + '</span><time>' + html.escape(v['date']) + '</time></div><h3>' + html.escape(v['title']) + '</h3><ul class="plan-version-changes">' + ''.join('<li>' + html.escape(c) + '</li>' for c in v['changes']) + '</ul>' + ('<h4>提出的问题</h4><ul class="plan-version-questions">' + _questions(v['questions']) + '</ul>' if v.get('questions') else '') + '</article>'
    for v in reversed(VERSIONS)) + '</div>'

coverage_html = '<p class="plan-auto-note">原始资料的每个要点落在哪一页（页码随演示自动更新）。</p><div class="plan-coverage">' + ''.join(
    '<article><h3>' + html.escape(a) + '</h3><span class="plan-page-ref">第 ' + '、'.join(f'{page_no[x]:02d}' for x in ids if x in page_no) + ' 页</span>' + _p(b) + '</article>' for a, ids, b in COVERAGE) + '</div>'

tabs = [('narrative', '叙事主线', narrative_html), ('outline', f'逐页大纲 <span>{len(slides)}</span>', outline_html), ('versions', f'版本记录 <span>{len(VERSIONS)}</span>', versions_html)] + ([('coverage', '依据对应', coverage_html)] if COVERAGE else [])
plan_html = ('<main id="planning-panel" hidden><div class="plan-top"><div><span class="plan-kicker">STORY WORKSPACE</span><h1>叙事与大纲</h1><p>先确认讲什么，再编排页面。</p></div><span class="plan-draft-label">'
    + ('当前版本 ' + html.escape(VERSIONS[-1]['version']) + '<br>' if VERSIONS else '') + '演示 ' + str(len(slides)) + ' 页</span></div>'
    + '<div class="plan-tabs" role="tablist" aria-label="内容规划">' + ''.join(f'<button role="tab" aria-selected="{"true" if i == 0 else "false"}" data-plan-view="{id}">{label}</button>' for i, (id, label, _) in enumerate(tabs)) + '<span>点击顶部“编辑文字”，修改自动存入本地 JSON</span></div>'
    + ''.join(plan_section(id, label.split(' <')[0], body) for id, label, body in tabs) + '</main>')

old['planning'] = {'version': VERSIONS[-1]['version'] if VERSIONS else '', 'pageCount': len(slides), 'narrativeOrder': [x[0] for x in NARRATIVE], 'sections': [t[0] for t in tabs]}
old['versions'] = VERSIONS
old['conceptPrompts'] = CONCEPT_PROMPTS
