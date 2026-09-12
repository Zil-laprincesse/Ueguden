# 更新日志 · Changelog

本文件记录维古登语项目的版本变更。
版本沿革按**语言**（词典版次 + 规范轮次）编排，仓库本身的整理过程另列一节。

---

## [未发布] — 下一轮

- [ ] 全量回改：把历代文档头部的「3963 词目」统一为 **4347**
- [ ] 统一词类写法：`名`/`名词`、`动`/`动词`、`形`/`形容词`、`副`/`副词`、`介`/`介词` 二选一
- [ ] 清理语料中的世界语残留（`tools/validate.py --corpus` 报 73 处）
- [ ] `dictionary.html` 的 `DICT_REV` 与词典版次（6）对齐

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
| 词汇 | `DICT_REV = 6`（对应「词典第六版」） | 词条增删 |
| 规范 | 「第 N 轮」勘误 | 音系、词法、句法、正字法任何改动 |

**只改拼写不改音位**记作「勘误」；**改动音位或格系统**需要新的一轮并同步全部语料。

## 发布方式

GitHub Release 的附件包含：

- `词典第六版.docx`（可打印/批注的原始版）
- `ueguden_dict.json` / `.csv`（机器可读快照）
- `dictionary.html`（离线单文件词典）
- `维古登语规范总纲.docx` 与全套规范 docx

正文给出该版本的：词条数、`DICT_REV`、适用规范清单、与上一版的差异摘要。
