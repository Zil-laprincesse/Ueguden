# -*- coding: utf-8 -*-
"""validate.py — 维古登语仓库自检

默认检查（无参数）：

  1. 词典 JSON 结构完整（字段齐全、序号连续）
  2. 重复词形
  3. 音标只含合法 IPA 字符（禁止 à / ò 等钝音符混入音标）
  4. 词形只含《正字法规范》字母表中的字符
  5. 词类写法一致性（名 vs 名词）——提示级
  6. Markdown 表格列数是否一致（转换质量）
  7. README 声明的词条数与 DICT_REV 是否与实际一致

可选：

  --corpus   额外扫描 corpus/ 中的词形，列出未被词典收录的词（提示级）
  --strict   把提示也当作失败（本地严格自检用；CI 默认不加）

退出码：0 = 无错误（含仅有提示）；1 = 有错误；加 --strict 时，只有提示也返回 1。
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# 《正字法规范》：26 基本字母 + 扩展字母 + 尖音符长元音
# 另允许：专名首字母大写、词缀连字符、钝音符 à/ò（标注重音）、分音符号 ä ë ï ö ü
WORD_CHARS = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "æøåãŭáéíóúǽàòäëïöüçĉĝ-"
)
# 音标（IPA）允许出现的字符
IPA_CHARS = set(
    "abcdefghijklmnopqrstuvwxyz"          # 拉丁基字（音标中的 /a/ /e/ 等）
    "æøåʌɐɜəɔʁɹŋɲʃʒ"                      # 元音与辅音音素
    "ˈˌ.ʰʲː͡\u0303\u0329\u031f"            # 重音、音节界、送气、长音、塞擦、鼻化、成音节
    "ɡ"                                    # U+0261，与 g 不同字
)
POS_CANON = {"名": "名词", "动": "动词", "形": "形容词", "副": "副词", "介": "介词"}

errors: list[str] = []
warns: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warns.append(msg)


def check_dict() -> dict:
    path = os.path.join(ROOT, "dictionary", "ueguden_dict.json")
    if not os.path.exists(path):
        err(f"缺少 {path}，请先运行 tools/build_dict.py")
        return {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    entries = data["entries"]

    if data.get("count") != len(entries):
        err(f"count 字段({data.get('count')}) 与实际条目数({len(entries)}) 不一致")

    nums = [e["n"] for e in entries]
    if nums != list(range(1, len(entries) + 1)):
        err("序号不连续或未从 1 开始")

    seen: Counter[str] = Counter(e["word"] for e in entries)
    dup = [w for w, c in seen.items() if c > 1]
    if dup:
        err(f"重复词形 {len(dup)} 个：{'、'.join(dup[:10])}")

    for e in entries:
        tag = f"#{e['n']} {e['word']}"
        for field in ("word", "ipa", "pos", "gloss", "etym"):
            if not str(e.get(field, "")).strip():
                err(f"{tag} 字段 {field} 为空")
        ipa = e["ipa"]
        bad = sorted({c for c in ipa if c not in IPA_CHARS and c not in "/"})
        if bad:
            err(f"{tag} 音标含非法字符 {bad}：{ipa}")
        if "à" in ipa or "ò" in ipa:
            err(f"{tag} 音标中出现钝音符（应写 ˈ）：{ipa}")
        badw = sorted({c for c in e["word"] if c not in WORD_CHARS})
        if badw:
            err(f"{tag} 词形含字母表外字符 {badw}")

    mixed = [(p, POS_CANON[p]) for p in POS_CANON
             if any(e["pos"] == p for e in entries) and any(e["pos"] == POS_CANON[p] for e in entries)]
    if mixed:
        warn("词类写法两套并存：" + "、".join(f"{a}/{b}" for a, b in mixed))
    return data


def check_tables() -> None:
    for sub in ("docs", "dictionary", "corpus"):
        base = os.path.join(ROOT, sub)
        for dirpath, _dirnames, filenames in os.walk(base):
            for name in filenames:
                if not name.endswith(".md"):
                    continue
                full = os.path.join(dirpath, name)
                with open(full, encoding="utf-8") as fh:
                    lines = fh.read().splitlines()
                width, start = None, 0
                for i, line in enumerate(lines, 1):
                    s = line.strip()
                    if s.startswith("|") and s.endswith("|"):
                        cells = len(re.findall(r"(?<!\\)\|", s)) - 1
                        if cells < 2:
                            width, start = None, 0
                            continue
                        if width is None:
                            width, start = cells, i
                        elif cells != width:
                            err(f"{sub}/{name}:{i} 表格列数跳变（第 {start} 行 {width} 列 → {cells} 列）")
                            width, start = cells, i
                    else:
                        width, start = None, 0


def check_readme_claims(data: dict) -> None:
    if not data:
        return
    path = os.path.join(ROOT, "README.md")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    n = data["count"]
    if f"dictionary-{n}%20entries" not in text.replace("+", "%20"):
        warn(f"README 徽章中的词条数与实际（{n}）可能不一致")
    if str(n) not in text:
        err(f"README 未声明当前词条数 {n}")
    rev = str(data.get("dict_rev"))
    if f"DICT_REV = {rev}" not in text:
        err(f"README 未声明当前词典版本 DICT_REV = {rev}")


# 语料扫描用的常见词缀（名词格、形容词格、体态、时态、语态、极性、人称、语气、情态、派生、数词）
AFFIXES = sorted(
    """gàlo gòle ona anto bela itá ment ize mis tut pha shŭ nai dai lai vai sai
    çe ge te rw de mŭ ma mé on un øt ŭt æt åt ló nó om oma der das gel gal os omo
    dem dap tís tæph kŭ ta se re an er es ion il lok li if en i ti rad sén tús ión
    té t m f c s""".split(),
    key=len, reverse=True,
)

# 世界语残留（《小说重写规范 v2.0》要求清除的形式）
ESPERANTO = {
    "la", "kaj", "ĉu", "pri", "povas", "devus", "estas", "estis", "kiel", "kiam",
    "kion", "kio", "kiu", "por", "kun", "sed", "nur", "tre", "pli", "plej", "oni",
    "mi", "vi", "li", "ŝi", "ĝi", "ili", "ni", "jes", "ne", "ĉar", "ke", "se",
    "ankaŭ", "jam", "nun", "tiam", "ĉi", "ĉio", "ĉiu", "unu", "du", "tri",
}


def strip_affixes(token: str, known: set[str]) -> bool:
    """词缀可叠加：最多剥 4 层，任一中间结果命中词典即视为已收录。"""
    stack = [token]
    for _ in range(4):
        nxt = []
        for tok in stack:
            if len(tok) <= 2:
                continue
            for aff in AFFIXES:
                if tok.endswith(aff) and len(tok) > len(aff) + 1:
                    base = tok[: -len(aff)]
                    if base in known:
                        return True
                    nxt.append(base)
        if not nxt:
            break
        stack = nxt
    return False


def check_corpus(data: dict) -> None:
    if not data:
        return
    known = {e["word"].lower() for e in data["entries"]}
    base = os.path.join(ROOT, "corpus")
    unknown: Counter[str] = Counter()
    esperanto: Counter[str] = Counter()
    for dirpath, _d, filenames in os.walk(base):
        for name in filenames:
            if not name.endswith(".md") or name == "README.md":
                continue
            with open(os.path.join(dirpath, name), encoding="utf-8") as fh:
                body = fh.read()
            body = re.sub(r"^---.*?^---", "", body, flags=re.S | re.M)   # front matter
            for tok in re.findall(r"[a-zæøåãŭáéíóúǽçĉĝˈ]{2,}", body.lower()):
                tok = tok.strip("ˈ")
                if tok in known or strip_affixes(tok, known):
                    continue
                if tok in ESPERANTO:
                    esperanto[tok] += 1
                elif len(tok) >= 3:
                    unknown[tok] += 1
    if esperanto:
        warn("语料中检出世界语残留 " + str(sum(esperanto.values())) + " 处（"
             + "、".join(f"{w}×{c}" for w, c in esperanto.most_common(12))
             + "）—— 按 docs/15-rewrite-spec-v2.md 应全部清除")
    if unknown:
        warn(f"语料中 {len(unknown)} 个词形在剥离常见词缀后仍未匹配词典"
             "（多为专名音译与尚未收录的新造词，仅供发现新词参考）："
             + "、".join(w for w, _ in unknown.most_common(20)))


def main(argv: list[str]) -> int:
    print("维古登语仓库自检")
    print("-" * 52)
    data = check_dict()
    check_tables()
    check_readme_claims(data)
    if "--corpus" in argv:
        check_corpus(data)

    for w in warns:
        print("  提示 ", w)
    for e in errors:
        print("  错误 ", e)
    print("-" * 52)
    if data:
        print(f"词典：{data['count']} 条 ｜ DICT_REV = {data.get('dict_rev')}")
    print(f"错误 {len(errors)} ｜ 提示 {len(warns)}")
    if errors:
        return 1
    if warns and "--strict" in argv:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
