# intelligenism.club 页面生成标准

本文档定义 intelligenism.club 所有文章页面的生成规范。每次生成新页面时，必须遵循本标准，确保：
1. 视觉风格完全一致
2. build_pages.py 能正确抓取元信息生成 pages.json
3. 主页 index.html 能正确展示文章卡片和更新流

---

## 一、Meta 标签规范（build_pages.py 抓取依赖）

每个 HTML 文件的 `<head>` 中必须包含以下四项信息，缺一不可：

### 1.1 必填字段

```html
<title>文章完整标题</title>
<meta name="article-date" content="YYYY-MM-DD">
<meta name="article-category" content="doc|update|release">
<meta name="article-description" content="50字以内的简短描述，显示在主页卡片上。">
```

### 1.2 字段说明

| 字段 | 来源 | 格式要求 | 用途 |
|---|---|---|---|
| `<title>` | HTML title 标签 | 纯文本，不含 HTML 标签 | pages.json 的 `title` 字段；浏览器标签页标题 |
| `article-date` | meta 标签 | 严格 `YYYY-MM-DD` 格式 | pages.json 的 `date` 字段；更新流按此倒序排列 |
| `article-category` | meta 标签 | 三选一：`doc` / `update` / `release` | pages.json 的 `category` 字段；决定在主页哪个区域展示 |
| `article-description` | meta 标签 | 纯文本，建议50字以内，不含引号 | pages.json 的 `description` 字段；主页卡片/更新流的摘要 |

### 1.3 Category 分类规则

| Category | 含义 | 主页展示位置 |
|---|---|---|
| `doc` | 常驻文档页（如 IAF 架构、v4 协议规范） | 左侧 Modules 大框卡片，需手动在 index.html 中维护入口 |
| `update` | 更新动态/进展公告 | 右侧 Updates 滚动流，自动出现 |
| `release` | 版本发布公告 | 右侧 Updates 滚动流，自动出现 |

### 1.4 build_pages.py 抓取逻辑

脚本执行流程：
1. 扫描 `articles/` 目录下所有 `.html` 文件
2. 从每个文件中提取：文件名（去掉 .html 后缀）→ `id`
3. 用正则从文件内容提取：`<title>` → `title`
4. 用正则从文件内容提取：`<meta name="article-date" content="...">` → `date`
5. 用正则从文件内容提取：`<meta name="article-category" content="...">` → `category`
6. 用正则从文件内容提取：`<meta name="article-description" content="...">` → `description`
7. 按 date 倒序排列，输出 `pages.json`

**注意事项：**
- meta 标签的 `content` 值中不能包含英文双引号 `"`（会截断正则匹配）
- meta 标签的 `name` 和 `content` 属性顺序必须是 name 在前、content 在后
- 每个字段必须在单独一行上，不要合并到同一行

### 1.5 生成的 pages.json 格式示例

```json
[
  {
    "id": "iaf-architecture",
    "title": "Intelligenism Agent Framework (IAF)",
    "date": "2026-03-30",
    "category": "doc",
    "description": "A ~550-line Python agent framework built on Intelligenism theory. Possibility management, additive complexity, true parallel execution."
  },
  {
    "id": "iaf-v09-update",
    "title": "IAF v0.9 Progress Update",
    "date": "2026-03-30",
    "category": "update",
    "description": "Agent Layer and UI Layer complete. Dispatch and Scheduler in progress."
  }
]
```

---

## 二、文件命名规范

- 文件名全部小写英文，单词用短横线 `-` 连接
- 文件名即 pages.json 中的 `id`，应具有描述性
- 所有文章 HTML 文件放在 `articles/` 目录下

示例：
- `articles/iaf-architecture.html` → id: `iaf-architecture`
- `articles/iaf-v09-update.html` → id: `iaf-v09-update`
- `articles/v4-protocol.html` → id: `v4-protocol`

---

## 三、视觉风格规范

### 3.1 配色方案

```css
:root {
    --bg-deep: #0c0c18;           /* 页面背景 */
    --bg-surface: #141428;        /* 次级背景 */
    --bg-card: #1a1a32;           /* 卡片/表格背景 */
    --bg-card-hover: #22224a;     /* 卡片 hover */
    --border-dim: #2a2a4a;        /* 边框/分割线 */
    --border-glow: #00e5a0;       /* 发光边框 */
    --text-bright: #f5f5f0;       /* 正文文字（高对比度近白色） */
    --text-primary: #e0e0e8;      /* 主要文字 */
    --text-secondary: #8888a0;    /* 次要文字 */
    --text-dim: #55556a;          /* 暗淡文字（meta 信息等） */
    --accent-cyan: #00e5a0;       /* 主强调色（标题、链接、边框发光） */
    --accent-gold: #f0c866;       /* 次强调色（子标题、外链） */
    --accent-blue: #5b8def;       /* 蓝色强调（更新流 hover） */
    --accent-pink: #e06090;       /* 粉色强调（保留） */
    --bold-color: #ffd866;        /* 加粗文字颜色（鲜金黄色） */
}
```

### 3.2 字体

```css
--font-pixel: 'VT323', monospace;                              /* 像素风标题 */
--font-mono: 'Share Tech Mono', 'IBM Plex Mono', monospace;    /* 等宽显示 */
--font-body: 'IBM Plex Mono', monospace;                       /* 正文 */
```

Google Fonts 导入（每个页面 head 中必须包含）：
```css
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=VT323&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
```

### 3.3 文字层级与对比度规则

| 元素 | 字体 | 大小 | 颜色 | 说明 |
|---|---|---|---|---|
| 文章大标题 h1 | VT323 (pixel) | clamp(2rem, 5vw, 3rem) | `--accent-cyan` #00e5a0 | 带 text-shadow 发光效果 |
| 章节标题 h2 | VT323 (pixel) | 1.8rem | `--accent-cyan` #00e5a0 | 底部有 1px border-dim 分割线 |
| 子标题 h3 | VT323 (pixel) | 1.35rem | `--accent-gold` #f0c866 | 无分割线 |
| 正文 p | IBM Plex Mono | 0.9rem | `--text-bright` #f5f5f0 | line-height: 1.8 |
| 加粗 strong | IBM Plex Mono | 继承 | `--bold-color` #ffd866 | 鲜金黄色，与正文白色形成区分 |
| 行内代码 code | Share Tech Mono | 0.85rem | `--accent-cyan` + 半透明背景 | |
| meta/日期 | Share Tech Mono | 0.75rem | `--text-dim` #55556a | |
| 列表项 li 中的 strong | IBM Plex Mono | 继承 | `--accent-gold` #f0c866 | |

### 3.4 特殊组件样式

**引用块 blockquote：**
- 左边框 3px solid `--accent-gold`
- 背景 rgba(240,200,102,0.06)
- 来源署名用 `<span class="quote-source">` 包裹，金色斜体

**高亮框 highlight-box：**
- 背景 `--bg-card`
- 边框 1px solid `--accent-cyan`
- 用于重要结论或核心设计原则

**代码块 pre：**
- 背景 #0e0e1c
- 边框 1px solid `--border-dim`
- 文字颜色 #c8c8d0

**表格 table：**
- 表头背景 `--bg-card`，文字 `--accent-cyan`
- 偶数行 rgba(26,26,50,0.5) 交替色
- 第一列文字用 `--accent-gold` 金色
- 用 `<div class="table-wrap">` 包裹确保手机端可横向滚动

**状态列表（Current Status 等）：**
- 用 `class="status-list"` 取消默认列表样式
- 已完成项用 `class="status-done"` 青绿色
- 进行中用 `class="status-wip"` 金色

### 3.5 扫描线效果

所有页面保持 CRT 扫描线叠加层：
```css
body::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px);
    pointer-events: none;
    z-index: 9999;
}
```

---

## 四、页面结构模板

### 4.1 整体布局

```
top-bar（sticky 导航栏）
  ├── nav-links: ← Home | 页内锚点链接...
  └── theory-link: 📖 Intelligenism 理论全书 ↗（指向 intelligenism.org）

article（max-width: 860px，居中）
  ├── article-header
  │   ├── h1.article-title（像素字体，青绿色）
  │   ├── p.article-tagline（等宽字体，金色，加粗关键信息）
  │   └── p.article-meta（日期 + badge 标签）
  ├── 正文内容（h2/h3/p/ul/table/blockquote/pre/highlight-box）
  └── Links 章节

footer
  ├── INTELLIGENISM.CLUB — Built by Minghai Zhuo
  └── .org | GitHub
```

### 4.2 导航栏规则

- 左侧第一个链接始终是 `← Home`，指向 `/`（回主页）
- 其余链接为页内锚点，根据文章内容的主要章节设定
- 右侧始终是 `📖 Intelligenism 理论全书 ↗` 外链

### 4.3 章节分割

- 每个 h2 章节之间用 `<hr>` 分割（渐变透明分割线）
- h2 上方 margin 56px，下方 20px
- h3 上方 margin 36px，下方 14px

---

## 五、响应式规则

- 文章最大宽度 860px，居中
- 手机端（≤600px）：padding 缩小，标题字号缩小，导航栏竖排换行
- 表格用 `<div class="table-wrap">` 包裹，手机端可横向滚动
- 代码块 `overflow-x: auto` 确保不会撑破布局

---

## 六、完整 HTML 骨架模板

生成新页面时，复制以下骨架，替换标记为 `{{...}}` 的占位内容：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{文章完整标题}}</title>
    <meta name="article-date" content="{{YYYY-MM-DD}}">
    <meta name="article-category" content="{{doc|update|release}}">
    <meta name="article-description" content="{{50字以内简短描述}}">
    <style>
        /* 完整 CSS 从 iaf-architecture.html 复制，不做任何修改 */
    </style>
</head>
<body>

    <nav class="top-bar">
        <div class="top-bar-inner">
            <div class="nav-links">
                <a href="/">← Home</a>
                <!-- 根据文章内容添加页内锚点 -->
            </div>
            <a href="https://intelligenism.org" target="_blank" rel="noopener" class="theory-link">
                📖 Intelligenism 理论全书 ↗
            </a>
        </div>
    </nav>

    <article class="article">

        <header class="article-header">
            <h1 class="article-title">{{文章标题}}</h1>
            <p class="article-tagline">{{一句话概要，金色加粗}}</p>
            <p class="article-meta">{{YYYY-MM-DD}} <span class="badge">{{版本号或标签}}</span></p>
        </header>

        <!-- 正文内容 -->

    </article>

    <footer class="footer">
        <p class="footer-text">
            INTELLIGENISM.CLUB — Built by
            <a href="https://intelligenism.org" target="_blank" rel="noopener">Minghai Zhuo</a>
        </p>
        <div class="footer-links">
            <a href="https://intelligenism.org" target="_blank" rel="noopener" class="footer-text" style="color: var(--text-secondary);">.org</a>
            <a href="https://github.com/IntelligenismCommercialDevelopment-LLC" target="_blank" rel="noopener" class="footer-text" style="color: var(--text-secondary);">GitHub</a>
        </div>
    </footer>

</body>
</html>
```

---

## 七、Checklist（每次生成页面前检查）

- [ ] `<title>` 标签已填写，内容为纯文本
- [ ] `<meta name="article-date">` 已填写，格式为 YYYY-MM-DD
- [ ] `<meta name="article-category">` 已填写，值为 doc / update / release 三选一
- [ ] `<meta name="article-description">` 已填写，content 中无英文双引号
- [ ] 文件名为小写英文 + 短横线，放在 articles/ 目录下
- [ ] CSS 完整复制自 iaf-architecture.html，未做修改
- [ ] 导航栏左侧第一项为 `← Home`，右侧为 intelligenism.org 外链
- [ ] footer 内容与模板一致
- [ ] 所有表格用 `<div class="table-wrap">` 包裹
- [ ] 引用块来源用 `<span class="quote-source">` 包裹
- [ ] 重要结论用 `<div class="highlight-box">` 包裹
- [ ] 本地双击打开确认显示正常
