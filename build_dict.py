# -*- coding: utf-8 -*-
"""build_dict.py — 由《词典第六版》生成词典的三种可协作格式

输入：词典第六版.docx（表格式词表，每行「序号 | 词形 /音标/ 词类　释义。　词源。」）
输出：
    dictionary/ueguden_dict.md    人读版（Markdown 表）
    dictionary/ueguden_dict.csv   表格版（UTF-8 BOM，Excel 可直接打开）
    dictionary/ueguden_dict.json  机器版（工具链 / 在线词典的数据源）

用法：python build_dict.py [源docx] [输出目录]
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from datetime import date

from docx import Document

ENTRY = re.compile(r"^(\S+)\s+(/[^/]+/)\s+(\S+)\s*(.*)$")
FW = "\u3000"
DICT_REV = 6


def parse(path: str) -> list[dict]:
    table = Document(path).tables[0]
    entries = []
    for row in table.rows:
        cells = [c.text.strip() for c in row.cells]
        if len(cells) < 2:
            continue
        num, body = cells[0].replace(FW, " ").strip(), cells[1]
        if not num.isdigit():
            continue
        body = body.replace(FW, " ").strip()
        m = ENTRY.match(body)
        if not m:
            entries.append({"n": int(num), "word": body, "ipa": "", "pos": "",
                            "gloss": "", "etym": "", "raw": body})
            continue
        word, ipa, pos, rest = m.groups()
        rest = row.cells[1].text.strip()
        parts = [p.strip() for p in rest.split(FW) if p.strip()]
        gloss = parts[1] if len(parts) > 1 else ""
        etym = " ".join(parts[2:]) if len(parts) > 2 else ""
        entries.append({"n": int(num), "word": word, "ipa": ipa, "pos": pos,
                        "gloss": gloss, "etym": etym, "raw": rest})
    return entries


def write_md(entries: list[dict], path: str, src: str) -> None:
    out = [
        "---",
        "title: 维古登语词典（第六版）",
        f"source: {os.path.basename(src)}",
        f"converted: {date.today().isoformat()}",
        f"dict_rev: {DICT_REV}",
        f"entries: {len(entries)}",
        "note: 当前词汇标准",
        "---",
        "",
        "# Ueguden 词典 · 第六版",
        "",
        f"> 当前词汇标准 ｜ 共 **{len(entries)}** 条词目 ｜ `DICT_REV = {DICT_REV}` ｜ "
        "词形按《正字法规范》，音标按 IPA，词条格式：`词形 /音标/ 词类 释义。词源`",
        "",
        "> 本表由 `tools/build_dict.py` 自 `词典第六版.docx` 自动生成，请勿手工改动；"
        "修订请改源文档后重新生成，或提交 Issue。",
        "",
        "| # | 词形 | 音标 | 词类 | 释义 | 词源 |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for e in entries:
        row = [str(e["n"]), e["word"], e["ipa"], e["pos"], e["gloss"], e["etym"]]
        row = [c.replace("|", "\\|") or "—" for c in row]
        out.append("| " + " | ".join(row) + " |")
    out.append("")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out))


def write_csv(entries: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "word", "ipa", "pos", "gloss", "etym"])
        for e in entries:
            w.writerow([e["n"], e["word"], e["ipa"], e["pos"], e["gloss"], e["etym"]])


def write_json(entries: list[dict], path: str, src: str) -> None:
    payload = {
        "language": "Ueguden",
        "name_zh": "维古登语",
        "dict_rev": DICT_REV,
        "source": os.path.basename(src),
        "generated": date.today().isoformat(),
        "count": len(entries),
        "entries": [{"n": e["n"], "word": e["word"], "ipa": e["ipa"],
                     "pos": e["pos"], "gloss": e["gloss"], "etym": e["etym"]}
                    for e in entries],
    }
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)


def main(argv: list[str]) -> int:
    src = argv[0] if argv else "词典第六版.docx"
    out = argv[1] if len(argv) > 1 else "ueguden/dictionary"
    os.makedirs(out, exist_ok=True)
    entries = parse(src)
    write_md(entries, os.path.join(out, "ueguden_dict.md"), src)
    write_csv(entries, os.path.join(out, "ueguden_dict.csv"))
    write_json(entries, os.path.join(out, "ueguden_dict.json"), src)
    bad = [e for e in entries if not e["ipa"]]
    print(f"解析 {len(entries)} 条（无音标 {len(bad)} 条）-> {out}")
    for e in bad[:10]:
        print("  ??", e["raw"][:80])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
