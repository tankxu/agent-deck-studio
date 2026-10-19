# Version history shown in the studio's “版本记录” tab. questions: (who, question, resolution).
VERSIONS = [
    {'version': 'v1', 'date': '2026-10-19', 'title': '从一份真实汇报 deck 中抽出工具与方法',
     'changes': ['工作台网页、协同编辑、播放、PDF 与网页导出、无头自检工具独立成仓库',
                 '通用版式组件库（components.css + tools/components.py）',
                 '方法论文档 docs/METHOD.md；本示例 deck 介绍思路与工具'],
     'questions': [('作者', '原项目里的资料、数据和产品截图能不能带过来？', '不带：仓库从零开始，只保留通用代码；示例 deck 只讲方法和工具'),
                   ('自检', '标题换行不显示、工作区打开后演示区没隐藏', '抽取样式时漏了属性选择器和注释后的规则，已修正抽取并补回'),
                   ('自检', '截图常漏掉大图', 'qa-shots 改为一个浏览器逐页打开，等图片解码完成再截'),
                   ('自检', '蓝底页上的蓝色标志看不清', '深色与蓝色页面上标志改为白色')]},
]
