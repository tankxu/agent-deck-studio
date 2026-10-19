# Example deck: the method and the tool, presented with the tool itself.
# Every slide is plain Python composing helpers from tools/components.py.

CONFIG.update(
    title='Agent Deck Studio · 和 Agent 一起做演示',
    lang='zh-CN',
    document_id='agent-deck-studio-intro',
    studio_name='Agent Deck Studio',
    footer='Agent Deck Studio',
    brand_html='<div class="wordmark"><img src="assets/mark.svg" alt=""><span>Agent Deck Studio</span></div>',
)

# ================= 开场 =================
S('cover', 'Agent Deck Studio', '开场',
  '<div class="ds-cover-art-wrap">' + concept('cover', '封面', 'A person and a friendly abstract AI presence arranging floating translucent presentation slides in a calm studio at night; slides glow cobalt blue #0057FF with warm golden #FFC629 highlights; premium 3D editorial illustration, cinematic soft light, dark charcoal background, generous empty space on the left for a title, no text, no letters, no logos, landscape 16:9', 'ds-cover-art') + '</div><div class="ds-cover-shade"></div><div class="cover-brand">' + brand() + '</div><div class="ds-cover-copy">' + E('cover.eyebrow', 'METHOD · TOOL · OPEN SOURCE', 'p', 'ds-eyebrow') + E('cover.title', '和 Agent\n一起做演示', 'h1') + E('cover.sub', 'Agent 起草与修改，人定方向与取舍', 'p') + '</div>',
  'ink', '这份 deck 本身就是用 Agent Deck Studio 做的：写在 deck/deck.py，网页里改字自动回写 JSON，版本记录里能看到每一轮审阅提的问题。', '封面', '概念图 + 标题')
agenda = [('01', '为什么需要它', '一次性生成的 PPT 改不动'), ('02', '方法', '从资料到叙事、页面、审阅与修订'), ('03', '工具', '网页工作台、协同编辑、导出与自检'), ('04', '开始使用', '五条命令跑起来')]
S('agenda', '目录', '开场', top('agenda', 'CONTENTS') + H('agenda', '这份 deck 讲四件事') + '<div class="ds-agenda four">' + ''.join('<button data-chapter="ch' + n + '"><span>' + n + '</span>' + E('agenda.' + n + '.t', t, 'strong') + E('agenda.' + n + '.s', s, 'em') + '</button>' for n, t, s in agenda) + '</div>',
  'paper', '点击卡片可直接跳到对应章节。', '目录', '四张章节卡片')

# ================= 01 为什么 =================
chapter('ch01', '01', '为什么需要它', '一次生成的 deck，\n改不动', '汇报材料要反复改：叙事、数据、措辞、受众都会变', 'blue')
S('pain', '三种做法的对比', '为什么需要它', top('pain', 'THE PROBLEM') + H('pain', '做 deck，难在第五轮修改', '第一版谁都能做出来；难的是改了十轮还不乱') +
  '<div class="ds-three">' + ''.join('<div class="ds-three-col' + (' good' if i == 2 else '') + '">' + E('pain.' + str(i) + '.l', l, 'span', 'ds-kicker') + E('pain.' + str(i) + '.t', t, 'h3') + '<ul>' + ''.join(E(f'pain.{i}.{j}', x, 'li') for j, x in enumerate(items)) + '</ul></div>' for i, (l, t, items) in enumerate([
      ('手做 PPT', '慢，而且难以协作', ['每次改动都要手动排版', '数据和口径散在各处', '谁改了什么说不清']),
      ('AI 一次性生成', '快，但改不动', ['再改一次就要重新生成', '人工改过的字会被覆盖', '依据和审阅过程没有留下来']),
      ('Agent Deck Studio', '快，而且能一直改', ['Agent 改代码，人改网页上的字', '同一份 JSON，自动合并、冲突可选', '叙事、大纲、版本记录与 deck 同步'])])) + '</div>',
  'paper', '真实场景：给老板的 BP 从纯文字改成图文，历经十几轮“主次调整、口径修改、换 logo、加页删页”。一次性生成的方案每一轮都要推倒重来。', '对比', '三栏对比，第三栏高亮')
S('belief', '核心观点', '为什么需要它', '<div class="ds-statement"><div class="ds-top">' + E('belief.kicker', 'THE IDEA', 'span', 'ds-kicker') + brand() + '</div>' + E('belief.title', 'deck 是一份可以反复审的叙事，\n不是一次性产物', 'h2') + E('belief.body', '所以它应该像代码一样：有源文件、能生成、能回滚、能审阅，每一轮的问题和取舍都记下来。', 'p') + '<div class="ds-statement-row">' + ''.join('<div>' + E('belief.r' + str(i) + '.t', a, 'b') + E('belief.r' + str(i) + '.s', b, 'span') + '</div>' for i, (a, b) in enumerate([('源文件', 'deck.py + JSON，进 Git'), ('人和 Agent 同时改', '网页编辑与代码生成互不覆盖'), ('审阅留痕', '每版的问题与处理写进版本记录')])) + '</div></div>',
  'blue', '这一页是全片的主张：把演示当成可维护的源文件，而不是一次性的生成物。', '主张', '整页蓝底宣言')

# ================= 02 方法 =================
chapter('ch02', '02', '方法', '先定讲什么，\n再排每一页', '资料 → 叙事 → 大纲 → 页面 → 审阅 → 修订', 'ink', art=concept('ch02', '方法', 'An elegant flowing river of glowing documents transforming step by step into structured presentation slides, seen from above at dusk; cobalt blue #0057FF light and warm golden #FFC629 accents, premium 3D editorial illustration, dark background, empty space on the left, no text, no letters, no logos, landscape 16:9'))
S('workflow', '六步工作流', '方法', top('workflow', 'WORKFLOW') + H('workflow', '六步，每一步都有产出物') +
  flow('workflow.f', [('folder', '资料进仓库', '原稿、会议纪要、数据报告放进 sources/'), ('doc', '叙事主线', '几段话讲清先说什么、后说什么'), ('layers', '逐页大纲', '每页一个主张、一种画面'), ('edit', '页面', 'deck.py 用组件拼出来'), ('users', '角色审阅', '子 Agent 扮演听众挑毛病'), ('history', '修订留痕', '问题与处理写进版本记录')], 'six') +
  '<div class="ds-flow-note">' + E('workflow.note', '前两步决定 80% 的质量：叙事没定，页面越漂亮返工越多。', 'p') + '</div>',
  'paper', '实践中最常见的返工来自叙事主次没对齐，例如“重点应该在前面的合作方案，而不是后面的底座”。先在“叙事与大纲”工作区对齐，再动页面。', '方法', '六步流程')
S('principles', '六条原则', '方法', top('principles', 'PRINCIPLES') + H('principles', '做了十几轮修改后留下的六条原则') +
  '<div class="ds-feat six">' + ''.join(card('principles.' + str(i), ic, t, s) for i, (ic, t, s) in enumerate([
      ('folder', '资料先进仓库', 'Agent 只依据仓库里的原件写，不凭记忆和转述'),
      ('image', '以图为主', '截图、架构图、概念图；不连续放纯文字页'),
      ('eye', '示意和真实分开', '画出来的示意图标“示意”，不冒充真实数据'),
      ('chart', '口径写进讲稿', '数字从哪来、怎么算，放在每页讲稿里'),
      ('users', '先想听众是谁', '同一份数据，对老板和对技术讲法不同'),
      ('check', '人定取舍', 'Agent 提方案和问题，冲突的口径由人拍板')])) + '</div>',
  'paper', '这些原则来自一次真实的 BP 改造：数据口径被追问、示意图里的数字被当成真实统计、品牌 logo 用错。每一条都对应一次返工。', '原则', '六宫格卡片')
S('review', '角色审阅', '方法', top('review', 'ROLE REVIEW') + H('review', '让子 Agent 扮演听众，先挑一遍毛病') +
  '<div class="ds-review"><div class="ds-review-deck">' + ICON('layers') + E('review.deck', '当前版本', 'b') + E('review.decks', '逐页截图 + 讲稿 + 原始资料', 'span') + '</div><div class="ds-review-arrows">' + ICON('arrow') + '</div><div class="ds-review-roles">' + ''.join('<div class="ds-role">' + ICON(ic) + '<div>' + E('review.r' + str(i) + '.t', t, 'b') + E('review.r' + str(i) + '.s', s, 'p') + '</div></div>' for i, (ic, t, s) in enumerate([
      ('user', '出资人 / 老板', '只看图和数字；最在意“我能得到什么”，也会注意自己的项目有没有被贬低'),
      ('doc', '方案作者', '读完会议纪要，检查原意有没有讲到、有没有讲错'),
      ('code', '技术负责人', '核对产品现状：哪些已上线、哪些是规划、数字是否准确')])) + '</div><div class="ds-review-arrows">' + ICON('arrow') + '</div><div class="ds-review-out">' + ICON('history') + E('review.out', '问题清单 → 修改', 'b') + E('review.outs', '采纳与不采纳都写进版本记录', 'span') + '</div></div>' +
  E('review.foot', '关键：给审阅 Agent 完整的背景（谁在听、和谁有利益关系），并要求按严重程度排序、给出页码和改法。', 'p', 'ds-callout center'),
  'paper', '一次实际审阅中，“出资人”角色指出了 9 条严重问题，其中最重要的一条是：方案对出资人自己的项目用了“改版、重构还是重做”的措辞，读起来像在说它不行。这类问题作者自己很难看出来。', '方法', '审阅流程图')
S('versions-shot', '版本记录', '方法', top('versions-shot', 'VERSION HISTORY') +
  '<div class="ds-split"><div class="ds-split-copy">' + E('versions-shot.title', '每一版改了什么，\n是谁提的问题', 'h2', 'ds-title') + E('versions-shot.body', '版本记录写在 deck/versions.py，在工作台的“版本记录”里展示。每条问题记下提问人、问题和处理；没采纳的也写明原因。', 'p', 'ds-lead') + tags('versions-shot.tags', ['提问人', '问题', '处理', '没采纳的原因']) + '</div><div class="ds-split-art">' + screen('versions.png', '工作台 · 版本记录') + '</div></div>',
  'paper', '版本记录让下一轮审阅的人知道哪些问题已经讨论过、为什么那样定，避免反复争论同一件事。', '展示', '文字 + 工作台截图')
S('images', '三种图怎么分工', '方法', top('images', 'VISUALS') + H('images', '三种图，三种来源') +
  '<div class="ds-three">' + ''.join('<div class="ds-three-col">' + '<div class="ds-three-ic">' + ICON(ic) + '</div>' + E('images.' + str(i) + '.l', l, 'span', 'ds-kicker') + E('images.' + str(i) + '.t', t, 'h3') + E('images.' + str(i) + '.s', s, 'p') + '</div>' for i, (ic, l, t, s) in enumerate([
      ('code', '示意图 · 架构图', 'Agent 用 HTML / SVG 画', '流程、架构、手机界面示意；可编辑、跟随配色；标注“示意”'),
      ('spark', '概念图', '图像模型生成', '在 deck.py 里写提示词，统一风格，生成后放 assets/concept/'),
      ('camera', '截图', '来自真实产品', '证明“已经做出来了”；演示数据要标明，不当业务规模')])) + '</div>',
  'paper', '概念图的提示词集中写在 concept() 调用里，构建时汇总到 deck-content.json 的 conceptPrompts，交给图像模型批量生成。', '方法', '三栏')
S('qa', '截图自检', '方法', top('qa', 'SELF-CHECK') +
  '<div class="ds-split rev"><div class="ds-split-art">' + screen('sheet.png', '自检联系表：每页截图拼在一起') + '</div><div class="ds-split-copy">' + E('qa.title', '改完先截图，\n自己看一遍', 'h2', 'ds-title') + E('qa.body', '每轮修改后逐页截图、拼成联系表，检查文字溢出、空白过多、图片没加载、品牌用错。Agent 能看图，就能自己发现大部分排版问题。', 'p', 'ds-lead') + code('qa.cmd', 'tools/qa-shots.sh\ntools/qa-sheet.sh') + '</div></div>',
  'paper', '实践中自检发现过：收尾页大标题被旧样式盖住、示意图数字像真实统计、logo 用错版本。', '方法', '联系表截图 + 命令')

# ================= 03 工具 =================
chapter('ch03', '03', '工具', '一个网页工作台，\n人和 Agent 同时改', '源文件生成网页；网页上的修改回写同一份 JSON', 'ink', art=concept('ch03', '工具', 'A clean futuristic workbench floating in a dark studio, with a large glowing slide canvas, small editing panels and a stack of version cards orbiting around it; cobalt blue #0057FF and warm golden #FFC629 light, premium 3D editorial illustration, empty space on the left, no text, no letters, no logos, landscape 16:9'))
S('arch', '架构', '工具', top('arch', 'ARCHITECTURE') + H('arch', '三个文件，一条回路') +
  '<div class="ds-arch">' + ''.join('<div class="ds-arch-box ' + c + '">' + ICON(ic) + E('arch.' + k + '.t', t, 'b') + E('arch.' + k + '.s', s, 'span') + '</div>' for k, c, ic, t, s in [
      ('a', 'a', 'code', 'deck/deck.py', 'Agent 写页面：组件 + 默认文字'),
      ('b', 'b', 'terminal', 'tools/build.py', '生成 index.html 与 deck-content.json'),
      ('c', 'c', 'doc', 'deck-content.json', '所有可编辑文字的唯一来源'),
      ('d', 'd', 'globe', '浏览器工作台', '点“编辑文字”直接改，自动保存'),
      ('e', 'e', 'sync', 'server.py', '本地保存接口：原子写入、冲突检测')]) +
  '<svg class="ds-arch-lines" viewBox="0 0 1440 520" preserveAspectRatio="none"><g fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 8"><path d="M300 120 H560"/><path d="M880 120 H1140"/><path d="M1290 190 V330 H1000"/><path d="M850 400 H440"/><path d="M290 330 V190" /></g></svg></div>',
  'paper', '构建时，JSON 里的文字优先；页面结构来自 deck.py。浏览器每 2.5 秒读回 JSON，Agent 直接改 JSON 也会出现在网页上。', '架构', '五个节点的回路图')
S('coedit', '协同编辑', '工具', top('coedit', 'CO-EDITING') +
  '<div class="ds-split"><div class="ds-split-copy">' + E('coedit.title', '网页改字，\nAgent 改结构', 'h2', 'ds-title') + '<div class="ds-rows">' + ''.join('<div>' + E('coedit.' + str(i) + '.t', t, 'b') + E('coedit.' + str(i) + '.s', s, 'span') + '</div>' for i, (t, s) in enumerate([
      ('自动保存', '点“编辑文字”，改完 0.4 秒写入 JSON'), ('外部修改自动读回', 'Agent 或编辑器改了 JSON，网页 2.5 秒内同步'), ('不同字段自动合并', '同一字段两边都改了，让人选保留哪一份'), ('导出离线网页', '文字、图片、字体打包成一个 HTML')])) + '</div></div><div class="ds-split-art">' + screen('editing.png', '编辑文字模式') + '</div></div>',
  'paper', '保存接口只接受同源请求、限制大小，写入用临时文件再原子替换，避免半写入的 JSON。', '功能', '功能列表 + 编辑模式截图')
S('defaults', '默认值跟踪', '工具', top('defaults', 'SAFE REBUILDS') + H('defaults', 'Agent 改默认文字，不会覆盖人改过的字') +
  '<div class="ds-vs"><div class="ds-vs-col">' + E('defaults.a.l', '没人改过', 'span', 'ds-mini') + E('defaults.a.t', 'JSON 里的值 = 上一次的默认值', 'h3') + '<div class="ds-pair"><span>旧默认</span><b>“每次活动拉来新用户”</b></div><div class="ds-pair new"><span>新默认</span><b>“有活动的那一周，新增用户”</b></div>' + E('defaults.a.s', '→ 跟随新默认值更新', 'p', 'ds-vs-result') + '</div><div class="ds-vs-col dark">' + E('defaults.b.l', '人改过', 'span', 'ds-mini') + E('defaults.b.t', 'JSON 里的值 ≠ 上一次的默认值', 'h3') + '<div class="ds-pair"><span>人工修改</span><b>“活动周新增约一万人”</b></div><div class="ds-pair new"><span>新默认</span><b>“有活动的那一周，新增用户”</b></div>' + E('defaults.b.s', '→ 保留人工修改', 'p', 'ds-vs-result') + '</div></div>',
  'paper', '构建时记住每个文字键上一次的默认值（deck-content.json 的 defaults）。这解决了“Agent 改了 deck.py，页面却没变”和“重建把人改的字冲掉”这两个常见问题。', '机制', '左右对比')
S('workspace', '叙事与大纲工作区', '工具', top('workspace', 'STORY WORKSPACE') + H('workspace', '叙事、大纲、版本，在同一个页面里') +
  '<div class="ds-gallery three">' + screen('plan-narrative.png', '叙事主线（可编辑）') + screen('plan-outline.png', '逐页大纲（由页面自动生成）') + screen('versions.png', '版本记录（含提出的问题）') + '</div>',
  'paper', '大纲不再单独维护：每页的讲述要点、画面和依据都写在 deck.py 的 S() 调用里，工作区自动汇总。', '展示', '三张截图')
S('components', '组件库', '工具', top('components', 'COMPONENTS') + H('components', '30 多种版式组件，拼出不重复的页面') +
  '<div class="ds-chipwall">' + ''.join('<span>' + esc(x) + '</span>' for x in ['封面', '章节页', '目录卡片', '左右图文', '大数字墙', '柱状图', '横向条形图', '环形图', '流程', '宣言页', '双栏对比', '三栏对比', '六宫格', '中心辐射图', '旅程', '时间线', '台阶', '截图拼墙', '手机截图', '概念图整页', '代码块', '标签', '团队', '诉求']) + '</div>' +
  E('components.foot', '每个组件 = components.css 里一组样式 + tools/components.py 里一个函数', 'p', 'ds-callout center'),
  'paper', '组件来自一份 50 多页的真实汇报 deck，去掉了业务内容后整理成通用版式。', '展示', '组件标签墙')
S('export', '播放与导出', '工具', top('export', 'PLAY & EXPORT') + H('export', '播放、导出 PDF、导出网页') +
  '<div class="ds-feat three">' + ''.join(card('export.' + str(i), ic, t, s, 'f1' if i == 0 else '') for i, (ic, t, s) in enumerate([
      ('play', '播放', '全屏只显示幻灯片；右上角浮出 ×，Esc 退出；光标静止自动隐藏'),
      ('download', '导出 PDF', '页面里逐页渲染、直接下载，16:9，和屏幕一致；50 页约 10 秒'),
      ('globe', '导出网页', '单个 HTML 离线打开，仍可编辑，适合发给别人')])) + '</div>',
  'paper', 'PDF 不走打印对话框：每页通过 SVG foreignObject 用浏览器自己的排版渲染成图，再用一个很小的 PDF 写入器拼成文件，不依赖第三方库。', '功能', '三张功能卡')
S('qa-tools', '自检工具', '工具', top('qa-tools', 'HEADLESS QA') + H('qa-tools', '给 Agent 的眼睛：无头浏览器自检') +
  '<div class="ds-feat three">' + ''.join(card('qa-tools.' + str(i), ic, t, s) for i, (ic, t, s) in enumerate([
      ('camera', 'qa-shots.sh', '逐页 1600×900 截图，空白页自动重试'),
      ('apps', 'qa-sheet.sh', '每 12 页拼一张联系表，一眼看完整套'),
      ('download', 'qa-pdf.mjs', '通过 Chrome 调试协议生成 PDF 并取回，验证导出')])) + '</div>',
  'paper', '截图依赖本机 Chrome；?shot=N 参数让页面只渲染第 N 页。', '功能', '三张工具卡')

# ================= 04 开始 =================
chapter('ch04', '04', '开始使用', '五条命令\n跑起来', '复制模板、写 deck.py、构建、打开工作台', 'blue')
S('quickstart', '快速开始', '开始使用', top('quickstart', 'QUICK START') +
  '<div class="ds-split"><div class="ds-split-copy">' + E('quickstart.title', '从这份 deck 开始改', 'h2', 'ds-title') + E('quickstart.body', '把 deck/ 目录换成你的内容：deck.py 写页面，narrative.py 写叙事，versions.py 记版本。也可以直接让 Agent 读 docs/METHOD.md 按方法来。', 'p', 'ds-lead') + '</div>' +
  code('quickstart.cmd', 'git clone <repo> my-deck && cd my-deck\npython3 tools/build.py\npython3 server.py --port 8793\nopen http://127.0.0.1:8793\ntools/qa-shots.sh && tools/qa-sheet.sh') + '</div>',
  'paper', '依赖：Python 3.10+、本机 Chrome（截图与 PDF 自检）、Node 22+（qa-pdf.mjs）。网页本身不依赖任何第三方库。', '使用', '说明 + 代码块')
S('prompt', '交给 Agent 的第一句话', '开始使用', top('prompt', 'FIRST PROMPT') + H('prompt', '交给 Agent 的第一句话') +
  code('prompt.text', '读 docs/METHOD.md。资料在 sources/：BP 原文、会议纪要、数据报告。\n先在 deck/narrative.py 写叙事主线给我确认，\n再在 deck/deck.py 排页面；每轮改完跑 qa 截图自己检查，\n然后派一个子 Agent 扮演听众挑毛病，问题和处理记进 versions.py。') +
  E('prompt.foot', '人做的事：给资料、确认叙事、拍板有冲突的口径。', 'p', 'ds-callout center'),
  'paper', '这是实际使用中最有效的开头：先让 Agent 交出叙事给人确认，再排版。', '使用', '代码块')
S('finale', '结束', '开始使用', '<div class="ds-cover-art-wrap">' + concept('cover', '封面', CONCEPT_PROMPTS.get('cover', ''), 'ds-cover-art') + '</div><div class="ds-cover-shade"></div><div class="cover-brand">' + brand() + '</div><div class="ds-cover-copy">' + E('finale.title', '让 Agent 起草，\n让人做决定', 'h1') + E('finale.sub', 'Agent Deck Studio · MIT License', 'p') + '</div>',
  'ink', '收尾。', '收尾', '回到封面视觉')
