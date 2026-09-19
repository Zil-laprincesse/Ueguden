# 学习材料 · study/

维古登语的**默写**（看汉语，写词形）材料。两份产物、同一份词典数据：

| 产物 | 用途 | 位置 |
| --- | --- | --- |
| **默写器**（单文件网页） | 日常刷题：随机抽题、即时判分、错词本 | [`../tools/dictation.html`](../tools/dictation.html) |
| **默写卷**（可打印 docx） | 手写默写：卷面 + 卷末答案册 | [`维古登语默写卷（第七版）.docx`](维古登语默写卷（第七版）.docx) |

> 数据源一律是 [`../dictionary/ueguden_dict.json`](../dictionary/ueguden_dict.json)（当前 **词典第七版 · 4350 条**）。
> 改词之后重新生成一次，两份材料就都跟上。

---

## 一、默写器（网页）

双击 `tools/dictation.html` 即可，无需联网、无需安装；也可以走线上地址
<https://zil-laprincesse.github.io/Ueguden/tools/dictation.html>。

- **范围**：首字母（`A`–`Z` 与「词缀与符号」）· 词类（名词 / 动词 / 形容词 …）
- **题量**：10 / 20 / 30 / 50 / 100 / 全部 ｜ **顺序**：随机 或 顺序
- **提示三档**：不给提示 ｜ 给音标 ｜ 给首字母与词长
- **作答**：输入后回车提交；答对显示 `✓`，答错显示正解与音标；再回车进下一题
- **符号键盘**：`í á é ó ú ǽ æ ø å ŭ ã ç ĉ ĝ à ò` 一键插入（省得切输入法）
- **判分**：完全一致才算对；只有变音符号写错会提示「字母对了，符号不对」（仍记错）
- **错词本**：答错与「看答案」会自动记入，答对后自动移出；存在本机浏览器里，不上传任何数据
- **重做错词 / 打印本卷**：结算页可以把本轮错词再练一遍，或直接打印成一张空白卷

## 二、默写卷（可打印）

- 卷面按首字母分 **27 节**（A – Z + 词缀与符号），每节一张表：`# ｜ 汉语释义 ｜ 词类 ｜ 默写`
- 答案册在卷末，序号与卷面一一对应，逐行核对
- 当前规模：**4350 题 + 4350 条答案，约 210 页**（A4，四号以下小字）
- 只用词典第七版数据；`--hint` 可在卷面加「音标」或「首字母与词长」提示列

## 三、重新生成

```bash
# 两份都出（默认）
python tools/build_dictation.py --all

# 只出网页 / 只出 docx
python tools/build_dictation.py --html
python tools/build_dictation.py --docx

# 出小卷：随机 200 题，固定种子（可复现），卷面带音标提示，不要答案册
python tools/build_dictation.py --docx --limit 200 --seed 7 --hint ipa --no-answers

# 只出某几个字母 / 某个词类
python tools/build_dictation.py --docx --letters A B C
python tools/build_dictation.py --docx --pos 动词
```

| 选项 | 说明 |
| --- | --- |
| `--html` / `--docx` / `--all` | 出哪一份（不带参数等价于 `--all`） |
| `--limit N` | 随机抽 N 条（配 `--seed` 可复现） |
| `--seed N` | 随机种子 |
| `--letters A B C` | 只出这些首字母分节 |
| `--pos 名词 --pos 动词` | 只出这些词类 |
| `--hint none\|ipa\|first` | 卷面提示列（默认 `none`） |
| `--no-answers` | 不出答案册 |

> 建议：整本 210 页适合按字母打印；平常用「随机 100–200 题的小卷」更顺手。
> 网页版的 `DICT_REV` 缓存号与词典版次（`dict_rev`）是两套编号，改动词库后网页会自动重建本地缓存。

## 四、许可

与仓库其余部分一致：内容 CC BY-SA 4.0，脚本 MIT。
