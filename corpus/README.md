# 语料库 · corpus/

维古登语的**应用实例**：用这门语言实际写出来的作品。
规范说明「应该怎么写」，语料说明「实际怎么写」——两者互为校验。

## 目录

| 体裁 | 文件 | 说明 |
| --- | --- | --- |
| 诗歌 `poems/` | [`the-internationale.md`](poems/the-internationale.md) | 《国际歌》维古登语译文（**诗歌体**） |
| 诗歌 `poems/` | [`dithyramb.md`](poems/dithyramb.md) | 酒神颂（**诗歌体**创作） |
| 书信 `letters/` | [`letter-to-the-beloved.md`](letters/letter-to-the-beloved.md) | 《致爱的信》（**常规体**） |
| 书信 `letters/` | [`written-in-a-letter.md`](letters/written-in-a-letter.md) | 《在信里写给你》（**常规体**） |
| 书信 `letters/` | [`farewell-letter.md`](letters/farewell-letter.md) | 《告别信》（**常规体** · 中文原文对照） |
| 小说 `novel/` | [`threshold-endless-night-vol2.md`](novel/threshold-endless-night-vol2.md) | 《阈界·永夜之狂澜》第二卷（**双语对照**） |

## 体裁与规范

| 体裁 | 适用的规范 | 注意 |
| --- | --- | --- |
| 常规体（默认） | `docs/04-morphology.md`、`docs/06-syntax.md` | 6 格 × 单复数；标准音系 |
| 诗歌体 | `docs/09-poetic-register.md`、`docs/10-poetic-tables.md` | 42 位变格 + 21 位变位；取消送气；节律重音 |
| 小说译文 | 另见 [`docs/15-rewrite-spec-v2.md`](../docs/15-rewrite-spec-v2.md) | 必须严格 SOV，**清除世界语残留**（`la`、`de`、`kaj`、`ĉu`、独立助动词） |

**诗歌体与常规体禁止混用**。混用时以常规体为准。

## 与原始文档的关系

本目录的文件由 `archive/docx/` 中对应的 `.docx` 转换而来，仅做结构化（标题、表格），
不改动任何原文。双语对照的排版、字体等视觉信息请查原始文档。

## 添加新语料

1. 放入对应体裁子目录，文件名用小写连字符（如 `elegy-for-autumn.md`）。
2. 文件头加 YAML front matter：`title` / `author` / `register`（`standard` 或 `poetic`）/ `source`。
3. 若为译文，正文按「维古登语行 → 原文行」交替排列（与 `novel/` 一致），方便逐句对照。
4. 提交前跑 `python tools/validate.py --corpus`：它会报告两件事——
   **世界语残留**（`la` / `kaj` / `ne` / 独立助动词，按重写规范必须清零）
   与**剥离常见词缀后仍未收录的词形**（新词候选）。

## 已知问题

`tools/validate.py --corpus` 当前在语料中检出 **68 处世界语残留**（集中在小说篇）。
这不是提取错误，而是语料本身的历史状态：小说译文写于严格 SOV 规范确立之前。
修正方法见 [`docs/15-rewrite-spec-v2.md`](../docs/15-rewrite-spec-v2.md)，
重写稿见 `archive/notes/_rewrite_c1.txt`、`_rewrite_c2.txt`。

**词形检出的口径**：报告里「未收录词形」多为**屈折形式与派生词**——词典收的是词根或不定式形
（`kontaktar`），正文用的是变位形（`kontaktçenaiom`），剥词缀脚本够不到，属正常噪音；
另有专名音译。`2026-09-26` 起扫描字符集与《正字法规范》字母表对齐（补入钝音符 `à ò`），
此前 `lotgàlo` 被切成 `lotg`+`lo` 造成的假阳性已清除。
