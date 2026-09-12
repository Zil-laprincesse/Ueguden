# 工具链 · tools/

| 文件 | 语言 | 作用 |
| --- | --- | --- |
| [`dictionary.html`](dictionary.html) | HTML/JS | **在线词典**：单文件离线可用，直接双击打开，也可部署到 GitHub Pages |
| [`build_dict.py`](build_dict.py) | Python | 由 `词典第六版.docx` 生成 `dictionary/` 的 MD / CSV / JSON |
| [`docx2md.py`](docx2md.py) | Python | 通用 docx → Markdown 转换器（标题层级、表格、加粗、合并单元格） |
| [`manifest.json`](manifest.json) | JSON | `docx2md.py` 的转换清单：哪份 docx 转成哪个 md |
| [`assemble.py`](assemble.py) | Python | 归置既有 Markdown、源 docx 与笔记到仓库目录 |
| [`validate.py`](validate.py) | Python | **仓库自检**：词典字段、重复词、音标与词形合法性、表格列数、README 声明一致性 |
| [`gen_ipa.js`](gen_ipa.js) | Node | 由词形批量生成音标（`x→ks`、重音落在音节起音前） |
| [`build_novel_docx.js`](build_novel_docx.js) | Node | 由 `novel_ueguden_data.js` 生成小说双语对照 docx |
| [`novel_ueguden_data.js`](novel_ueguden_data.js) | JS | 《阈界·永夜之狂澜》第二卷的逐段双语数据源 |
| [`fix_novel_r3.js`](fix_novel_r3.js) | Node | 小说译文的第三轮批量订正脚本 |

## 环境

```bash
pip install -r requirements.txt     # Python 依赖（python-docx）
node --version                      # Node 仅用于 .js 工具，可选
```

## 常用命令

```bash
# 1. 重新生成全部规范文档（改 docx 后）
python tools/docx2md.py tools/manifest.json --base .

# 2. 重新生成词典三格式（改词典 docx 后）
python tools/build_dict.py "archive/docx/词典第六版.docx" dictionary

# 3. 归档既有 md / 源 docx / 笔记
python tools/assemble.py

# 4. 提交前自检
python tools/validate.py            # 结构性检查（默认）
python tools/validate.py --corpus   # 额外扫描语料：世界语残留 + 未收录词形
```

## validate.py 检查项

| 代号 | 检查 | 级别 |
| --- | --- | :---: |
| 结构 | JSON 字段完整、序号从 1 连续 | 错误 |
| 重复词 | 同一词形出现多次 | 错误 |
| IPA | 音标含字母表外字符／钝音符 `à ò`（音标里应写 `ˈ`） | 错误 |
| 词形 | 词形含《正字法规范》字母表外的字符 | 错误 |
| 表格 | Markdown 表格列数跳变（转换事故的信号） | 错误 |
| README | 声明词条数 / `DICT_REV` 与词典实际不一致 | 错误 |
| 词类 | `名` 与 `名词` 两套写法并存 | 提示 |
| 语料 | 世界语残留（`la`/`kaj`/`ne`…） | 提示 |
| 语料 | 剥离常见词缀后仍未收录的词形（新词候选） | 提示 |

退出码：`0` 干净或仅有提示 ｜ `1` 有错误（CI 会失败）。
加 `--strict` 时「只有提示」也返回 `1`，供本地严格自检使用。

## 关于 `dictionary.html`

单文件设计：CSS、JS、词库全部内嵌，无外部依赖，无网络请求。
内嵌词库以 `const RAW = \`…\`` 内联，`DICT_REV` 常量用于触发浏览器端缓存重建——
**改动词库后必须递增 `DICT_REV`**，否则使用者看到的是旧缓存。

### 已发布的站点

仓库已开启 GitHub Pages，源为 `main` 分支根目录，并放置了 `.nojekyll`
（关闭 Jekyll，避免带 front matter 的 `.md` 被改写成 `.html` 而使站内链接失效）。

| 地址 | 内容 |
| --- | --- |
| <https://zil-laprincesse.github.io/Ueguden/> | 入口页 `index.html`（仓库根目录） |
| <https://zil-laprincesse.github.io/Ueguden/tools/dictionary.html> | **在线词典** |

> ⚠️ GitHub 网页端**不会渲染**仓库里的 `.html`——点 `tools/dictionary.html` 只会看到源代码。
> 要"点开就能用"，必须走上面的 Pages 地址。
