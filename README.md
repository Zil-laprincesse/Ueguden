---
title: 维古登语（Ueguden）
---

# Ueguden · 维古登语

> **维古登语（Ueguden）** 是一门为文学创作设计的黏着语人造语（artlang）。
> 本仓库是它的**规范、词典、语料与工具**的唯一权威集合。

![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)
![Dictionary](https://img.shields.io/badge/dictionary-4347%20entries-blue.svg)
![Docs](https://img.shields.io/badge/specs-16%20documents-green.svg)

---

## 这是什么

维古登语是一门**艺术语（artlang）**，为诗歌、小说、书信等文学创作而生。
核心语序为 **SOV**；语法意义通过后缀层层黏着表达，不做屈折变化。
它拥有一套独立的诗歌体（古 Ueguden）历史方言变体，用于史诗与抒情诗。

本仓库把散落在 Word 文档里的语言材料整理成**可读、可查、可协作、可版本化**的结构：
规范转为可 diff 的 Markdown，词典同时给出人工可读与机器可读的三种格式，
语料按体裁归档，工具链（词典网页、构词脚本、校验器）集中放在 `tools/`。

## 快速开始

| 我想…… | 去这里 |
| --- | --- |
| 查一个词 | **在线词典** <https://zil-laprincesse.github.io/Ueguden/tools/dictionary.html> ｜ 离线版 [`tools/dictionary.html`](tools/dictionary.html) |
| 从零学这门语言 | [`docs/12-tutorial.md`](docs/12-tutorial.md)（自学教程，含练习与答案） |
| 读完整规范 | [`docs/13-full-spec.md`](docs/13-full-spec.md)（规范总纲，109 张表） |
| 看怎么发音 | [`docs/01-phonology.md`](docs/01-phonology.md) · [`docs/02-orthography.md`](docs/02-orthography.md) |
| 学语法 | [`docs/04-morphology.md`](docs/04-morphology.md) → [`docs/06-syntax.md`](docs/06-syntax.md) → [`docs/08-advanced-grammar.md`](docs/08-advanced-grammar.md) |
| 读作品 | [`corpus/`](corpus/)（诗歌、书信、小说） |
| 提交修改 | [CONTRIBUTING.md](CONTRIBUTING.md) |

## 仓库结构

| 目录 | 内容 |
| --- | --- |
| `docs/` | 语法规范、教程、勘误、重写规范（16 份 Markdown） |
| `dictionary/` | 主词库：Markdown / CSV / JSON 三种格式；`archive/` 存历代版本 |
| `corpus/` | 语料库：诗歌 `poems/`、书信 `letters/`、小说 `novel/` |
| `tools/` | 在线词典、构词与音标脚本、校验器、转换器 |
| `archive/` | 原始 `.docx` 与历史笔记（供 Release 附件与比对） |

## 语言概览

| 项目 | 内容 |
| --- | --- |
| 类型 | 黏着语（agglutinative） |
| 语序 | **SOV**（主语—宾语—谓语），动词居句末 |
| 字母 | 26 个基本拉丁字母 + 8 个扩展字母（元音 `ã æ å ø ŭ`，辅音 `ç ĉ ĝ`） |
| 音系要点 | `c /k/` 与 `k /kʰ/` 送气对立；`r` 按位置三值（`/ʁ/`音节首、`/ɹ/`元音后、`/r/`辅音后）；尖音符标记长元音 |
| 名词 | **6 格**（主 / 宾 / 与 / 工具 / 方位 / 属）× 单复数，复数标记 `-té` |
| 动词 | 词缀链叠加：**体态 + 时态 + 语态 + 极性 + 人称 + 语气 + 情态** |
| 形容词 | 有格与数的变化，须与所修饰名词一致 |
| 体裁变体 | 常规体 ｜ **诗歌体（古 Ueguden）**：42 位变格（6 人称 × 7 格）+ 21 位变位（3 人称 × 7 格），含夺格 |
| 词汇量 | 4347 条（词典第六版） |

## 当前标准

学习和引用本项目时，请以以下版本为准：

- **词汇标准**：`dictionary/ueguden_dict.json`（词典第六版，**4347 条**，`DICT_REV = 6`）
- **语法标准**：[`docs/00-framework.md`](docs/00-framework.md)、[`docs/02-orthography.md`](docs/02-orthography.md)、[`docs/04-morphology.md`](docs/04-morphology.md)、[`docs/06-syntax.md`](docs/06-syntax.md)、[`docs/08-advanced-grammar.md`](docs/08-advanced-grammar.md)
- **诗歌体标准**：[`docs/09-poetic-register.md`](docs/09-poetic-register.md) + [`docs/10-poetic-tables.md`](docs/10-poetic-tables.md)
- **勘误状态**：已应用 [`docs/14-errata.md`](docs/14-errata.md)（2026-09-05 第五轮）
- **词典版本沿革**：初版 → 第二版 → 第三版 → 第四版（修订）→ 第五版（修订）→ **第六版**，旧版全部保留在 `dictionary/archive/`

> ⚠️ **已知不一致**：历代文档头部沿用的「3963 词目」为旧统计，词典第六版实际词条为 **4347** 条（无重复词条）。
> 本仓库统一采用 4347。相关旧描述将在下一轮勘误中同步。

## 参与贡献

欢迎提交新词、语料、勘误与工具改进。提交前请先读 [CONTRIBUTING.md](CONTRIBUTING.md)，
并运行 `python tools/validate.py` 自检。

## 许可证

| 内容 | 许可证 |
| --- | --- |
| 代码（`tools/*.py`、`*.js`） | [MIT](LICENSE-MIT) |
| 语法规范、教程、词典、语料 | [CC BY-SA 4.0](LICENSE) |
| 语言规范本身 | CC BY-SA 4.0 —— **允许并鼓励用它创作衍生作品** |

---

## English

**Ueguden** is a constructed language (*artlang*) designed for literary creation.
This repository is the canonical collection of its grammar, dictionary, corpus and tooling.

- **Type:** agglutinative · **Word order:** SOV
- **Alphabet:** 26 Latin letters + 8 extended (`ã æ å ø ŭ ç ĉ ĝ`)
- **Nouns:** 6 cases (nominative, accusative, dative, instrumental, locative, genitive) × singular/plural
- **Verbs:** affix chain — aspect + tense + voice + polarity + person + mood + modal
- **Registers:** standard, and a **poetic register (Old Ueguden)** with 42 declensions and 21 conjugations
- **Lexicon:** 4347 entries (`DICT_REV = 6`)

**Layout:** `docs/` specifications and tutorial · `dictionary/` lexicon (MD/CSV/JSON) ·
`corpus/` poems, letters, novel · `tools/` web dictionary, scripts, validator · `archive/` original `.docx`.

Start with [`docs/12-tutorial.md`](docs/12-tutorial.md) to learn the language, or
[`docs/13-full-spec.md`](docs/13-full-spec.md) for the complete specification.

**License:** code under MIT; documentation, dictionary and corpus under CC BY-SA 4.0.
