# 更新日志 · Changelog

本文件记录维古登语项目的版本变更。
版本沿革按**语言**（词典版次 + 规范轮次）编排，仓库本身的整理过程另列一节。

---

## [未发布] — 下一轮

- [ ] 清理语料中的世界语残留（`tools/validate.py --corpus` 报 73 处，集中在小说篇）
- [ ] 语料层的前置介词改写：规范与教程已统一为后置词（`sovæt en`），小说与书信正文尚未逐句过
- [ ] `tools/validate.py --corpus` 报 1378 个未收录词形（多为专名音译与待收新词），逐个判定是否入典

---

## [语言 · 第六轮] 2026-09-19 — 增补词目 + 规范层清尾

> 备份：改动前的 `.docx` 与生成物均在 git 历史中（本轮起以版本库为唯一回退手段）

**词典（DICT_REV 6 → 7，词典第七版）**

- 新增 3 条词目，**4347 → 4350** 条：
  | # | 词形 | 音标 | 词类 | 释义 |
  | ---: | --- | --- | --- | --- |
  | 47 | ajíwiquce | /a.d͡ʒiː.wi.ˈku.ke/ | 名词 | 相濡以沫的青梅竹马 |
  | 618 | didni | /ˈdid.ni/ | 名词 | 扭曲；《星空夜》 |
  | 1498 | jinpesilua | /d͡ʒin.pe.ˈsi.lu.a/ | 形容词 | 口误的，说错了的 |
- 两条新词按音系微调拼写（原稿 `ajíwyquce` / `jinpsilua`）：
  `wy` = /wj/ 不在允许首辅音丛表内 → 写作 `wí`；`ps` 属借词专用组合 → 插 `e` 断开（同 `pkela→pekela`、`pneuma→peneuma` 的旧例）
- **词类写法统一为全称**：`名`→`名词`、`动`→`动词`、`形`→`形容词`、`副`→`副词`、`介`→`介词`，
  以及 `代`/`连`/`数`/`前` 与全部复合标注（`名/形`→`名词/形容词` 等），共改 **3609 行**；
  `validate.py` 的 `POS_MIXED` 提示随之清零（检查保留为回归防线）
- 新词按词形局部字母序插入（非追加），插入点之后全表重新编号 1–4350
- 源文档另存为 `archive/docx/词典第七版.docx`；第六版保留为历史快照，并生成
  `dictionary/archive/dict-v6.md`（manifest 已登记）
- 源文档头部「以《词典第六版》为准 · 共 3963 词目」→「以《词典第七版》为准 · 共 4350 词目」
- `tools/build_dict.py` 的 `DICT_REV` 6 → 7，默认源文档改为《词典第七版》
- `tools/dictionary.html` 内嵌词库同步 4350 条与全称词类，`DICT_REV`（缓存重建号）24 → 26

**规范层修复（docx 源文档就地改 + 重新生成 md）**

- 清除残留世界语 `kaj` 3 处：`08-advanced-grammar`「Fíexen kaj kantar!」→「Fíexen **æ** kantar!」、
  `12-tutorial`「Salút, kaj græses!」→「Salút, **æ** græses!」、总纲随源文档同步
- 废止表述「c 只出现在非音节首」清尾：《框架》《自学教程》的字母表/条件变体表 → 「c /k/（任何位置）」，
  与第四轮裁决、《核心音素》《高级语法》一致（教程表内 `ç` 与 `c` 两行按新规则重写）
- 后置词体例清尾：《高级语法》2.5 / 3.4 与《自学教程》两处 `en tabloæt` → `tabloæt en`
- 《高级语法》2.5 例句主语 `Makanan`（非词典词）→ `liman`（食物）
- 词表引用统一：《词法规范》《句法规范》《高级语法》《自学教程》共 4 处「第五版词典」→「第七版」

**仓库声明同步**

- `README.md`（徽章 / 词汇量 / 词汇标准 / 版本沿革 / 勘误状态 / English）、`index.html`、
  `CITATION.cff`、`CONTRIBUTING.md`、`tools/README.md`、`.github/workflows/validate.yml` 全部改为 4350 / 第七版
- README 中「3963 词目」的已知不一致条目改为「统计口径已统一」（源文档头部已改写）
- `tools/README.md` 补充说明：`dict_rev`（词典版次）与 `DICT_REV`（缓存重建号）是两套编号

**终验**

- `python tools/validate.py --corpus`：错误 **0** ｜ 提示 **2**（语料世界语残留 73 处 · 未收录词形 1378 个）——
  词类两套写法的提示已随本轮统一清零
- CI 一致性复算：由源文档重新生成的词典与提交的 `ueguden_dict.json` 词形、词类序列完全一致
- 文档一致性：`docx2md` 与 `build_master` 重新生成的 md 与源文档逐行一致（仅 `converted` 日期变化）
- 在线词典：`node --check` 校验内嵌脚本通过

---

## [仓库整理] 2026-09-12

把散落在 Word 文档中的语言材料整理为可协作、可版本化的仓库。
同日稍后完成首次上线与结构修复，见下一节。

**新增**

- `README.md` 中英双语门面；`CONTRIBUTING.md` / `CHANGELOG.md` / `CITATION.cff` / `CODE_OF_CONDUCT.md`
- `LICENSE`（CC BY-SA 4.0，文档/词典/语料）+ `LICENSE-MIT`（代码）
- `.gitignore`、`.github/workflows/validate.yml`（CI 自检）

**文档**

- 24 份 `.docx` + 2 份既有 Markdown 全部转为 Markdown，落位 `docs/`（16 份）与 `corpus/`（5 份）
- 每份文件带 YAML front matter，记录源文档与转换日期
- 原 Word 文档完整保留于 `archive/docx/`，供 Release 附件与逐字比对

**词典**

- `dictionary/ueguden_dict.md` / `.csv` / `.json` 三格式同源生成
- **第六版确定 4347 条词目**（含音标、词类、释义、词源四字段齐全，无重复词条）
- 初版至第五版（修订）全部转为 Markdown 存档于 `dictionary/archive/`

**工具**

- `tools/docx2md.py` 通用 docx→Markdown 转换器（标题层级 / 表格 / 合并单元格 / 加粗）
- `tools/build_dict.py` 词典三格式生成器
- `tools/validate.py` 仓库自检（结构、重复词、音标、词形、表格、README 声明一致性）
- `tools/assemble.py` 归置脚本；`tools/manifest.json` 转换清单

**修正**

- `勘误记录 20260905.md` 第十二节表格中的裸 `|` 已转义（修复 Markdown 表格错行）
- `12-tutorial.md` 数词表表头补齐至 17 列（修复转换期列数跳变）

---

## [首次上线与结构修复] 2026-09-12

仓库 `Zil-laprincesse/Ueguden` 建立。首次上传时各子目录被**逐个压平上传**，
并各自生成同名分支（`archive`、`corpus`、`dictionary`、`docs`、`docx`、`github`、
`letters`、`notes`、`novel`、`poems`、`tools`、`workflows` 等 13 条），
`main` 只剩一堆散文件，所有嵌套路径（如 `docs/12-tutorial.md`）返回 404。

**修复**

- 完整目录树一次性推送到 `main`：85 个文件，`docs/` `dictionary/` `corpus/` `tools/` `archive/` `.github/` 各归其位
- 删除 13 条临时分支。删除前逐条比对 blob 哈希，确认内容均已含于 `main`；
  仅两份**只存在于分支**的文件抽出保留至 `archive/github-init/`，无内容丢失
- 许可证关系留痕：建仓时选择的 CC0 1.0 原件存入 `archive/github-init/LICENSE-CC0-1.0.txt`；
  仓库维持双许可（文档/词典/语料 CC BY-SA 4.0，代码 MIT），CC0 不再作为仓库许可证生效
- `fix(ci)`：`tools/validate.py` 原先在「仅有提示」时返回退出码 `2`，
  被 GitHub Actions 判为失败（工作流 `validate` 显示 failing）。
  现改为只有**错误**才返回非零，严格模式改用 `--strict`
- 修复后：`validate` 工作流 passing；`docs/12-tutorial.md`、`dictionary/archive/dict-v4-revised.md`
  等此前 404 的链接全部 200

**教训（写进 CONTRIBUTING 之外的备忘）**

用 GitHub 网页端上传**整个仓库**时，不要一个文件夹一个文件夹地拖——
浏览器上传会拍平目录，并且默认往新分支提交。
正确做法是本地 `git clone` → 放入目录 → `git add/commit/push`，
或者把文件夹**自身**（而不是它的内容）拖进去并确认提交到 `main`。

---

## [语言 · 第五轮] 2026-09-05 — 全量勘误

见 [`docs/14-errata.md`](docs/14-errata.md)。要点：

- 清除旧拼写：`khav → hav/havi`、`skribar → kribar`、`stranga → tranga`、`fenestr → fenester`、`ŝuo → shuo`
- `ʌ` 字母废弃，统一写作 `ŭ`（音值仍为 `/ʌ/`）
- 音标内的钝音符 `à / ò` 全部改为标准 IPA 重音符 `ˈ`
- 扩展辅音 `ç ĉ ĝ` 纳入正式字母表
- 词典：`ueguden_dict.docx`（后改名 `dict_ueguden.docx`）同步修正
- `Dictionary.html`：合并早期双份副本、补回 `</html>`、`DICT_REV` 15 → 18

## [语言 · 第四轮] 2026-08-30 — 小说重写

- 确立《小说重写规范 v2.0》：SOV 语序、无冠词、格后缀、形容词变格、动词词缀链
- 《阈界·永夜之狂澜》第二卷第一、二章重写

## [语言 · 第三轮] 2026-08-29 — 词典与诗歌体

- 词典第五版（修订）：拼写与音标系统更新，补充词源
- 诗歌体（古 Ueguden）42 位变格表 + 21 位变位表确定

## [语言 · 第二轮] 2026-08

- 词典第四版（修订）：基于第一版词汇、第二版拼写与音标系统
- 句法规范、词法规范、体态表成型

## [语言 · 初版] 2026-07

- 词典初版、第二版、第三版
- 框架、核心音素与字母系统、正字法规范、音节结构与重音规则

---

## 版本号约定

本项目**不使用** SemVer 作为语言版本号，改用两条独立轴：

| 轴 | 记法 | 递增条件 |
| --- | --- | --- |
| 词汇 | `DICT_REV = 7`（对应「词典第七版」） | 词条增删 |
| 规范 | 「第 N 轮」勘误 | 音系、词法、句法、正字法任何改动 |

**只改拼写不改音位**记作「勘误」；**改动音位或格系统**需要新的一轮并同步全部语料。

## 发布方式

GitHub Release 的附件包含：

- `词典第七版.docx`（可打印/批注的原始版）
- `ueguden_dict.json` / `.csv`（机器可读快照）
- `dictionary.html`（离线单文件词典）
- `维古登语规范总纲.docx` 与全套规范 docx

正文给出该版本的：词条数、`DICT_REV`、适用规范清单、与上一版的差异摘要。
