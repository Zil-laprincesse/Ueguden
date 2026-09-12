# -*- coding: utf-8 -*-
"""assemble.py — 把既有 Markdown、工具脚本与原始 docx 归置进 ueguden/ 仓库

* docs/14-errata.md、docs/15-rewrite-spec-v2.md —— 既有 Markdown 加 front matter 后归档
* tools/ —— 词典网页、构词/音标脚本、小说数据
* archive/docx/ —— 全部源 docx（供 Release 附件与历史比对）
* archive/notes/ —— 重写稿与审校笔记

用法：python assemble.py <项目根目录> <ueguden目录>
"""
from __future__ import annotations

import os
import shutil
import sys
from datetime import date

ROOT = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Administrator\Desktop\UEGUDEN"
DEST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "ueguden")

MD_NOTES = [
    ("勘误记录 20260905.md", "docs/14-errata.md", "维古登语勘误记录（2026-09-05）",
     "第五轮勘误：拼写、音标、词形一致性回改记录"),
    ("重写规范 v2.md", "docs/15-rewrite-spec-v2.md", "维古登语小说重写规范 v2.0",
     "清除世界语残留、恢复 SOV 语序的重写规范"),
]

TOOLS = [
    ("Dictionary.html", "tools/dictionary.html"),
    ("build_novel_docx.js", "tools/build_novel_docx.js"),
    ("novel_ueguden_data.js", "tools/novel_ueguden_data.js"),
    ("_fix_r3.js", "tools/fix_novel_r3.js"),
    (os.path.join("_letter", "coin.js"), "tools/gen_ipa.js"),
]

NOTES = ["_rewrite_c1.txt", "_rewrite_c2.txt", "_zh_review.txt", "_share_og.txt"]


def with_front_matter(src: str, dst: str, title: str, note: str) -> None:
    with open(src, encoding="utf-8") as fh:
        body = fh.read()
    fm = ["---", f"title: {title}", f"source: {os.path.basename(src)}",
          f"converted: {date.today().isoformat()}", f"note: {note}", "---", ""]
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(fm) + "\n" + body.strip() + "\n")
    print("  md   ", dst)


def copy(src: str, dst: str) -> None:
    if not os.path.exists(src):
        print("  MISS", src)
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print("  copy ", dst)


def main() -> int:
    for src, dst, title, note in MD_NOTES:
        with_front_matter(os.path.join(ROOT, src), os.path.join(DEST, dst), title, note)
    for src, dst in TOOLS:
        copy(os.path.join(ROOT, src), os.path.join(DEST, dst))
    for name in NOTES:
        copy(os.path.join(ROOT, name),
             os.path.join(DEST, "archive", "notes", os.path.basename(name)))
    docx_dir = os.path.join(DEST, "archive", "docx")
    os.makedirs(docx_dir, exist_ok=True)
    n = 0
    for name in sorted(os.listdir(ROOT)):
        if name.lower().endswith(".docx") and os.path.isfile(os.path.join(ROOT, name)):
            copy(os.path.join(ROOT, name), os.path.join(docx_dir, name))
            n += 1
    print(f"\n归档 docx {n} 份 -> archive/docx/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
