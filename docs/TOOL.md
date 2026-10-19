# 工具说明

## 构建

`python3 tools/build.py` 依次执行：

1. 读取 `deck-content.json`（不存在则新建）；
2. 运行 `tools/components.py`（组件函数）和 `deck/deck.py`（页面）；
3. 编页码，把 `data-chapter="<页面 id>"` 换成真实页码；
4. 运行 `tools/studio_plan.py`，生成“叙事与大纲”工作区；
5. 写出 `index.html` 和 `deck-content.json`（先写临时文件再原子替换）。

### 可编辑文字与默认值跟踪

页面上每段文字都通过 `T(key, 默认值)`（deck 里用 `E(key, 默认值)`，它会自动加上 `d.` 前缀）输出。输出的元素带 `data-edit-id`，网页上可以直接编辑。

`deck-content.json` 的 `texts` 保存当前值，`defaults` 保存上一次构建时的默认值。构建时的规则：

- `texts[key]` 还等于 `defaults[key]`：说明没人改过，更新为 `deck.py` 里的新默认值；
- 不相等：说明人改过，保留。

所以 Agent 改了 `deck.py` 里的文字，页面会跟着更新；人在网页上改过的字也不会被冲掉。

## deck.py 的基本写法

```python
CONFIG.update(title='我的方案 · 2026', footer='我的方案',
              brand_html='<div class="wordmark"><img src="assets/mark.svg" alt=""><span>我的方案</span></div>')

chapter('ch01', '01', '第一章', '章节大标题', '一句说明', 'blue')
S('growth', '用户增长', '第一章',
  top('growth', 'GROWTH') + H('growth', '每上一个项目，就来一波新用户', '副标题') +
  '<div class="ds-chart-wrap">' + bars('growth.bars', [('4 月', 20417, '20,417'), ('5 月', 13846, '13,846')]) + '</div>',
  theme='paper',                       # paper | ink | blue
  notes='口径：每月新注册，剔除机器人账户。',
  kind='数据', visual='月度柱状图', origin='数据报告 2026-10-18')
```

`S()` 的 `notes`、`visual`、`origin` 会进入工作区的“逐页大纲”和每页的“讲稿”。

## 组件

| 函数 | 用途 |
|---|---|
| `chapter(id, n, label, title, sub, theme, art)` | 章节页，可带整幅概念图 |
| `top(id, kicker)` / `H(id, title, sub)` | 页眉小标与标题 |
| `num(k, n, label)` | 大数字 + 说明（放进 `.ds-hero-grid`、`.ds-case-nums`） |
| `bars` / `hbars` / `donuts` | 柱状图、横向条形图、环形图 |
| `flow(k, steps)` | 横向流程，`steps=[(图标, 标题, 说明)]` |
| `card(k, icon, t, s)` | 卡片，放进 `.ds-feat`（`.six` / `.three`） |
| `tags(k, items)` / `code(k, text)` | 标签、代码块 |
| `img` / `shot` / `phone_img` / `screen` | 图片、可放大截图、手机截图、工作台截图槽 |
| `concept(key, label, prompt)` | 概念图槽：有图显示图，没图显示占位并收集提示词 |
| `ICON(name)` | 线性图标，名称见 `ICONS` |

可直接使用的版式类（见 `components.css`）：`ds-split`、`ds-hero-nums`、`ds-chart-wrap`、`ds-two`、`ds-case`、`ds-statement`、`ds-cb`、`ds-three`、`ds-musts`、`ds-feat`、`ds-eco`、`ds-journey`、`ds-loop`、`ds-stairs`、`ds-road`、`ds-vs`、`ds-gallery`、`ds-phones`、`ds-team`、`ds-ask`、`ds-vision`、`ds-review`、`ds-arch`、`ds-chipwall`。可以参照 `deck/deck.py` 里的用法。

## 本地服务

`python3 server.py --port 8793`

- `GET /api/content`：返回 `deck-content.json` 和修订号；
- `POST /api/content`：提交 `{changes: {key: {before, after}}}`。服务端只接受同源请求，并限制数据大小；如果某个字段当前值既不等于 `before` 也不等于 `after`，返回 409 和冲突字段，交给网页让人选择。

## 自检与导出

| 命令 | 说明 |
|---|---|
| `tools/qa-shots.sh [dir] [first] [last]` | 逐页 1600×900 截图，等图片解码完成再截 |
| `tools/qa-sheet.sh [dir]` | 每 12 页拼一张联系表 |
| `node tools/qa-pdf.mjs out.pdf` | 通过 Chrome 调试协议调用页面里的 PDF 渲染并取回文件 |
| `tools/export-pdf.sh out.pdf` | 命令行导出 PDF（与网页按钮同一个渲染器） |
| `node tools/capture-studio.mjs` | 截工作台界面（编辑模式、工作区各页） |

以上脚本默认访问 `http://127.0.0.1:8793/`，可用 `DECK_URL` 环境变量改地址。

页面参数：`?shot=N` 只渲染第 N 页（用于截图）；`?view=plan&tab=versions` 直接打开工作区的某一页；`?pdftest=1` 生成 PDF 供自检脚本读取。

## PDF 导出原理

每页复制一份，把其中的图片、字体和 CSS 里的 `url()` 都转成内嵌数据，放进 SVG 的 `foreignObject`，用浏览器自己的排版画到 canvas 上（2 倍分辨率），再转成 JPEG。最后由一个约 30 行的 PDF 写入器，把每页 JPEG 按 1200×675 pt 拼成文件。SVG 用 data: 地址加载，因为 Chrome 会把 blob: 地址加载的 foreignObject 画布标记为不可导出。已在 Chrome 实测，Safari 未测。
