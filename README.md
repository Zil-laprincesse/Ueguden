# 词典 · dictionary/

维古登语主词库。**当前词汇标准是第六版**，共 **4347** 条词目（`DICT_REV = 6`）。

## 文件

| 文件 | 格式 | 用途 |
| --- | --- | --- |
| [`ueguden_dict.md`](ueguden_dict.md) | Markdown 表 | 人读版，GitHub 上可直接浏览与检索 |
| [`ueguden_dict.csv`](ueguden_dict.csv) | CSV（UTF-8 BOM） | 表格版，Excel / Numbers 双击即开 |
| [`ueguden_dict.json`](ueguden_dict.json) | JSON | 机器版，工具链与在线词典的数据源 |
| `archive/` | 同上（Markdown） | 历代词典存档，用于比对与回溯 |

三种格式全部由脚本自同一份源文档生成，内容一致：

```bash
python tools/build_dict.py "archive/docx/词典第六版.docx" dictionary
```

> ⚠️ **不要手工编辑 `ueguden_dict.*`**：它是一次性生成的产物。
> 改词请提 Issue 或改源文档后重新生成，否则下一次生成会覆盖你的改动。

## 词条格式

源文档中每个词条为一行：

```
词形 /音标/ 词类　释义。　词源。
```

拆分后映射到三个格式的六个字段：

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| `n` | 序号（1 – 4347） | `2002` |
| `word` | 词形（按《正字法规范》） | `loĝejo` |
| `ipa` | 音标（IPA，含重音符 `ˈ`） | `/loˈd͡ʒe.jo/` |
| `pos` | 词类 | `名` |
| `gloss` | 中文释义 | `住处，住所。` |
| `etym` | 词源 | `loĝi（居住）+ -ejo（场所）。` |

## 词类分布

| 词类 | 数量 | 词类 | 数量 |
| --- | ---: | --- | ---: |
| 名 / 名词 | 2407 + 300 | 动 / 动词 | 559 + 206 |
| 形 / 形容词 | 414 + 101 | 副 / 副词 | 201 + 25 |
| 连词 | 20 | 代词 | 17 |
| 数词 | 14 | 后缀 | 10 |
| 介词 / 介 | 9 + 7 | 助词 | 8 |
| 前缀 | 7 | 叹词 | 5 |
| 分词 | 5 | 名/形 | 3 |

> 词类缩写有两套写法（`名` 与 `名词`、`动` 与 `动词`），属历史遗留。
> `tools/validate.py` 会把它报为 `POS_MIXED` 提示，与拼写/音标错误分开统计。

## 版本沿革

| 版本 | 文件 | 说明 |
| --- | --- | --- |
| 第六版 | `ueguden_dict.*` | **当前标准**，4347 条，全表化结构 |
| 第五版（修订） | [`archive/dict-v5-revised.md`](archive/dict-v5-revised.md) | 段落式词表，含字母分节 |
| 第四版（修订） | [`archive/dict-v4-revised.md`](archive/dict-v4-revised.md) | 第二版拼写 + 音标系统，补词源 |
| 第三版 | [`archive/dict-v3.md`](archive/dict-v3.md) | — |
| 第二版 | [`archive/dict-v2.md`](archive/dict-v2.md) | 确立第二代拼写与音标 |
| 初版 | [`archive/dict-v1.md`](archive/dict-v1.md) | 最早词表 |

旧版中的拼写（如 `khav`、`skribar`、`stranga`、`fenestr`、`ŝuo`、`aço`）属于**已废弃形式**，
第五轮勘误（见 [`docs/14-errata.md`](../docs/14-errata.md)）已给出对应关系。**请勿用于新文本。**

## 统计口径说明

历代文档头部写有「共 3963 词目」，那是第五版时期的统计。
第六版实际为 **4347** 条，且经校验无重复词条、无缺音标、无缺释义、无缺词源。
本仓库一律采用 **4347**。
