# 文档总览 · docs/

本目录收录维古登语的全部规范、教程与勘误，共 **16 份 Markdown**。
所有文件由 `tools/docx2md.py` 自 `archive/docx/` 中的原始 Word 文档自动转换，
每份文件的 YAML front matter 里记录了它来自哪一份源文档。

> **转换原则**：只做结构化（标题层级、表格、加粗），不改动任何语言内容。
> 若正文与原始 docx 不一致，以 `archive/docx/` 中的原始文档为准，并请提 Issue。

---

## 阅读顺序

### 入门路线（第一次接触维古登语）

| 顺序 | 文档 | 内容 |
| ---: | --- | --- |
| 1 | [00-framework.md](00-framework.md) | 语言框架：字母表、音变规则、辅音群简化、整体设计 |
| 2 | [01-phonology.md](01-phonology.md) | 核心音素与字母系统 |
| 3 | [03-syllable-stress.md](03-syllable-stress.md) | 音节结构与重音规则 |
| 4 | [12-tutorial.md](12-tutorial.md) | **自学教程**（语音→词法→动词→派生→句法→语用→诗歌体，含练习与答案） |

### 规范路线（按顺序通读即得完整语法）

| 顺序 | 文档 | 内容 |
| ---: | --- | --- |
| 1 | [00-framework.md](00-framework.md) | 总论与框架 |
| 2 | [01-phonology.md](01-phonology.md) | 音系 |
| 3 | [02-orthography.md](02-orthography.md) | 正字法（字母—音位对应、长元音、书写约定） |
| 4 | [03-syllable-stress.md](03-syllable-stress.md) | 音节结构与重音 |
| 5 | [04-morphology.md](04-morphology.md) | 词法（词类、名词 6 格、动词词缀链、派生） |
| 6 | [05-aspect.md](05-aspect.md) | 体态（简单体与复合体、动作助词） |
| 7 | [06-syntax.md](06-syntax.md) | 句法（SOV 语序、句型、否定、疑问） |
| 8 | [07-clauses.md](07-clauses.md) | 从句问题 |
| 9 | [08-advanced-grammar.md](08-advanced-grammar.md) | 高级语法（连接音变、情态、复杂结构） |
| 10 | [11-translation-scheme.md](11-translation-scheme.md) | 中文转译方案 |

### 诗歌体路线

| 文档 | 内容 |
| --- | --- |
| [09-poetic-register.md](09-poetic-register.md) | 诗歌体规范：适用范围、拟古屈折、音系调整、节律重音、夺格 |
| [10-poetic-tables.md](10-poetic-tables.md) | 42 位变格表 / 21 位变位表 / 形容词副词变格表 |

### 工程与维护

| 文档 | 内容 |
| --- | --- |
| [13-full-spec.md](13-full-spec.md) | **规范总纲**：把上述规范合成一份完整手册（含 109 张表） |
| [14-errata.md](14-errata.md) | 勘误记录（最近一轮：2026-09-05，第五轮全量回改） |
| [15-rewrite-spec-v2.md](15-rewrite-spec-v2.md) | 小说重写规范 v2.0：清除世界语残留、恢复严格 SOV |

---

## 文件清单

| 文件 | 源文档 | 规模 |
| --- | --- | :---: |
| `00-framework.md` | 框架.docx | 20 表 |
| `01-phonology.md` | 核心音素与字母系统.docx | 12 表 |
| `02-orthography.md` | 正字法规范.docx | — |
| `03-syllable-stress.md` | 音节结构与重音规则.docx | 3 表 |
| `04-morphology.md` | 词法规范.docx | 27 表 |
| `05-aspect.md` | 体态表.docx | 3 表 |
| `06-syntax.md` | 句法规范.docx | 4 表 |
| `07-clauses.md` | 从句问题.docx | 2 表 |
| `08-advanced-grammar.md` | 维古登语高级语法.docx | 11 表 |
| `09-poetic-register.md` | 诗歌体.docx | — |
| `10-poetic-tables.md` | 诗歌体（古Ueguden）变格变位表.docx | 3 表 |
| `11-translation-scheme.md` | 中文转译方案.docx | 24 表 |
| `12-tutorial.md` | 维古登语自学教程.docx | 37 表 |
| `13-full-spec.md` | 维古登语规范总纲.docx | 109 表 |
| `14-errata.md` | 勘误记录 20260905.md | — |
| `15-rewrite-spec-v2.md` | 重写规范 v2.md | — |

## 文档间的优先级

出现冲突时，按以下顺序裁定：

1. [`02-orthography.md`](02-orthography.md)、[`04-morphology.md`](04-morphology.md)、[`06-syntax.md`](06-syntax.md) —— 分项规范
2. [`13-full-spec.md`](13-full-spec.md) —— 规范总纲（合成版）
3. [`00-framework.md`](00-framework.md) —— 框架（设计说明）
4. [`12-tutorial.md`](12-tutorial.md) —— 教程（教学表述，可能简化）
5. 其余文档

诗歌体（`09`/`10`）与常规体互不覆盖，**禁止混用**；混用时以常规体为准。

## 重新生成本目录

```bash
python tools/docx2md.py tools/manifest.json --base .
```

清单在 `tools/manifest.json`，增删文档改清单即可。
