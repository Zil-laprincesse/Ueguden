# -*- coding: utf-8 -*-
"""docx2md.py — 维古登语项目文档转换器

把 .docx（规范、词典、语料）转换为可 diff、可检索、可渲染的 Markdown。

特性：
  * 保留 Word 标题层级（Heading 1-6 / 标题 1-6）
  * 无样式文档按中文规范编号（一、/ 1.1 / 第X部分）推断标题
  * 表格转 Markdown 管道表，自动处理合并单元格（横向合并留空、纵向合并补空）
  * 保留加粗；清理全角空格、软回车、零宽字符
  * 支持批量清单（manifest.json / 命令行 键值对）

用法：
    python docx2md.py manifest.json
    python docx2md.py --src a.docx --dst out/a.md

依赖：python-docx
"""
from __future__ import annotations

import json
import os
import re
import sys
import zipfile
from datetime import date

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

# ---------------------------------------------------------------- 文本清理

ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\ufeff"), None)
HEADING_STYLES = {
    "title": 1,
    "标题": 1,
    "heading 1": 1, "heading 2": 2, "heading 3": 3,
    "heading 4": 4, "heading 5": 5, "heading 6": 6,
    "标题 1": 1, "标题 2": 2, "标题 3": 3,
    "标题 4": 4, "标题 5": 5, "标题 6": 6,
    "subtitle": 2, "副标题": 2,
}
LIST_STYLES = ("list paragraph", "列表段落", "list bullet", "list number")

CN_NUM = "一二三四五六七八九十百零〇"


def clean(text: str) -> str:
    text = text.translate(ZERO_WIDTH)
    text = text.replace("\u3000", " ").replace("\xa0", " ")
    text = text.replace("\v", " ").replace("\r", " ").replace("\n", " ")
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def escape_cell(text: str) -> str:
    return clean(text).replace("\\", "\\\\").replace("|", "\\|") or " "


def slug_ok(text: str) -> bool:
    return 0 < len(text) <= 60 and not text.endswith(("。", "，", "；", "：", "、", ".", ","))


# ---------------------------------------------------------------- 标题启发式

RE_CN_SECTION = re.compile(rf"^[{CN_NUM}]+[、．.]\s*\S")
RE_PART = re.compile(rf"^第[{CN_NUM}\d]+(部分|篇|章|节)")
RE_NUM = re.compile(r"^(\d+(?:\.\d+){0,3})[\.、]?\s+?\S")
RE_PAREN = re.compile(rf"^[（(][{CN_NUM}\d]+[)）]\s*\S")


def guess_heading(text: str) -> int | None:
    """对没有 Word 样式的老文档，按编号模式推断标题级别。"""
    if re.fullmatch(r"[A-ZÆØÅÃ][A-Z]?", text):   # 词典的字母分节 A / B / C …
        return 2
    if not slug_ok(text):
        return None
    if len(text) > 40:
        return None
    if RE_PART.match(text):
        return 2
    if RE_CN_SECTION.match(text):
        return 2
    m = RE_NUM.match(text)
    if m:
        depth = m.group(1).count(".") + 1
        return min(2 + depth, 5)
    if RE_PAREN.match(text):
        return 3
    return None


# ---------------------------------------------------------------- 段落 / 表格

def runs_md(paragraph: Paragraph) -> str:
    out = []
    for run in paragraph.runs:
        t = run.text
        if not t:
            continue
        if run.bold and t.strip() and not t.strip().startswith("**"):
            out.append(f"**{t.strip()}**")
        else:
            out.append(t)
    text = "".join(out)
    return clean(text)


def para_to_md(paragraph: Paragraph, first: bool) -> str:
    text = runs_md(paragraph)
    if not text:
        return ""
    style = (paragraph.style.name or "").strip().lower()
    level = HEADING_STYLES.get(style) or HEADING_STYLES.get(style.replace("  ", " "))
    if level:
        text = text.replace("**", "")
        return f"{'#' * min(level, 6)} {text}"
    if first and slug_ok(text) and not text.endswith((":", "：")):
        text = text.replace("**", "")
        return f"# {text}"
    if any(style.startswith(s) for s in LIST_STYLES):
        return f"- {text}"
    guessed = guess_heading(text)
    if guessed:
        return f"{'#' * guessed} {text}"
    return text


def table_to_md(table: Table) -> list[str]:
    rows = []
    for row in table.rows:
        cells, seen = [], set()
        for cell in row.cells:
            key = id(cell._tc)
            if key in seen:          # 横向合并 → 留空
                cells.append(" ")
            else:
                seen.add(key)
                cells.append(escape_cell(cell.text))
        rows.append(cells)
    width = max(len(r) for r in rows) if rows else 0
    if not width:
        return []
    out = []
    header = rows[0] if rows else [""] * width
    if len(set(header)) == 1 and len(rows) > 1:
        header = [f"列{i + 1}" for i in range(width)]
    header = header + [" "] * (width - len(header))
    out.append("| " + " | ".join(header) + " |")
    out.append("|" + "|".join([" --- "] * width) + "|")
    for r in rows[1:]:
        r = r + [" "] * (width - len(r))
        out.append("| " + " | ".join(r) + " |")
    return out


def iter_blocks(doc: Document):
    body = doc.element.body
    for child in body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            yield Paragraph(child, doc)
        elif tag == "tbl":
            yield Table(child, doc)


# ---------------------------------------------------------------- 主转换

def convert(src: str, dst: str, title: str | None = None, note: str | None = None) -> dict:
    doc = Document(src)
    lines: list[str] = []
    tables = 0

    for index, block in enumerate(iter_blocks(doc)):
        if isinstance(block, Paragraph):
            # 只有「文档的第一个块」才当作标题；表格在前时不误判正文为 H1
            md = para_to_md(block, index == 0)
            if md:
                lines.append(md)
                lines.append("")
        else:
            md = table_to_md(block)
            if md:
                tables += 1
                lines.extend(md)
                lines.append("")

    # 压缩多余空行
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    doc_title = title or os.path.splitext(os.path.basename(src))[0]
    fm = ["---", f"title: {doc_title}",
          f"source: {os.path.basename(src)}",
          f"converted: {date.today().isoformat()}"]
    if note:
        fm.append(f"note: {note}")
    fm.append("---")
    body = "\n".join(fm) + "\n\n" + text
    heading = f"# {doc_title}"
    if text.startswith("# "):
        body = "\n".join(fm) + "\n\n" + text
    else:
        body = "\n".join(fm) + "\n\n" + heading + "\n\n" + text

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)

    media = extract_media(src, dst)
    return {"src": src, "dst": dst, "bytes": len(body.encode("utf-8")),
            "tables": tables, "media": media}


def extract_media(src: str, dst: str) -> int:
    """把 docx 内嵌图片抽到 <md同级>/assets/<md名>/ 下并计数。"""
    try:
        zf = zipfile.ZipFile(src)
    except Exception:
        return 0
    names = [n for n in zf.namelist() if n.startswith("word/media/")]
    if not names:
        return 0
    base = os.path.join(os.path.dirname(dst), "assets",
                        os.path.splitext(os.path.basename(dst))[0])
    os.makedirs(base, exist_ok=True)
    for n in names:
        with open(os.path.join(base, os.path.basename(n)), "wb") as fh:
            fh.write(zf.read(n))
    return len(names)


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    if argv[0] == "--src":
        src = argv[argv.index("--src") + 1]
        dst = argv[argv.index("--dst") + 1]
        title = argv[argv.index("--title") + 1] if "--title" in argv else None
        print(json.dumps(convert(src, dst, title), ensure_ascii=False))
        return 0

    base = ""
    if "--base" in argv:
        i = argv.index("--base")
        base = argv[i + 1].rstrip("/\\")
        del argv[i:i + 2]
    with open(argv[0], encoding="utf-8") as fh:
        manifest = json.load(fh)

    report = []
    for item in manifest:
        dst = os.path.join(base, item["dst"]) if base else item["dst"]
        try:
            report.append(convert(item["src"], dst,
                                  item.get("title"), item.get("note")))
            print(f"  OK  {os.path.basename(item['src'])} -> {dst} "
                  f"({report[-1]['bytes']} B, {report[-1]['tables']} tables)")
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {item['src']}: {exc}")
            report.append({"src": item["src"], "error": str(exc)})

    ok = sum(1 for r in report if "error" not in r)
    print(f"\n完成：{ok}/{len(report)}")
    return 0 if ok == len(report) else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
