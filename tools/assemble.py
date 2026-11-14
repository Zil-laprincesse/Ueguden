# -*- coding: utf-8 -*-
"""assemble.py — 把既有 Markdown、工具脚本与原始 docx 归置进 ueguden/ 仓库

* docs/14-errata.md、docs/15-rewrite-spec-v2.md —— 既有 Markdown 加 front matter 后归档
* tools/ —— 词典网页、构词/音标脚本、小说数据
* archive/docx/ —— 全部源 docx（供 Release 附件与历史比对）
* archive/notes/ —— 重写稿与审校笔记

用法：python assemble.py [<项目根目录>] [<ueguden目录>]

2026-11-14 起：作者工作区按用途分了子目录（规范/ 词典/ 语料/ 工具/ 素材/ 归档/），
本脚本不再假定源文件都在根目录——按 SRC_DIRS 顺序递归查找，同名文件以先找到的为准；
旧布局（文件全在根目录）仍可用，因为根目录也在候选列表里。
"""
from __future__ import annotations

import os
import shutil
import sys
from datetime import date

ROOT = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Administrator\Desktop\UEGUDEN"
DEST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "ueguden")

# 源目录候选（按优先级；根目录放最后，兼容旧布局）
SRC_DIRS = ["规范", "词典", "语料", "素材", "工具", "归档/旧版词典", "归档", "."]

# 不进 archive/docx/ 的文件（已从仓库撤下的应用实例等）
EXCLUDE = {"告别信.docx"}

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
    ("coin.js", "tools/gen_ipa.js"),           # 原在 _letter/ 下
]

NOTES = ["_rewrite_c1.txt", "_rewrite_c2.txt", "_zh_review.txt", "_share_og.txt"]


def find(name: str, prefer: str | None = None) -> str | None:
    """在 SRC_DIRS 里找文件；prefer 给定时优先该子目录；最后再递归兜底。"""
    cands = []
    if prefer:
        cands.append(os.path.join(ROOT, prefer, name))
    for d in SRC_DIRS:
        cands.append(os.path.join(ROOT, d, name))
    cands.append(os.path.join(ROOT, name))
    seen = set()
    for c in cands:
        c = os.path.normpath(c)
        if c in seen:
            continue
        seen.add(c)
        if os.path.isfile(c):
            return c
    # 递归兜底（跳过仓库、备份与 Office 锁文件）
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d != "ueguden" and not d.startswith("_backup")]
        if name in filenames:
            return os.path.join(dirpath, name)
    return None


def with_front_matter(src: str, dst: str, title: str, note: str) -> None:
    with open(src, encoding="utf-8") as fh:
        body = fh.read()
    fm = ["---", f"title: {title}", f"source: {os.path.basename(src)}",
          f"converted: {date.today().isoformat()}", f"note: {note}", "---", ""]
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(fm) + "\n" + body.strip() + "\n")
    print("  md   ", os.path.relpath(dst, DEST))


def copy(src: str, dst: str) -> None:
    if not src or not os.path.exists(src):
        print("  MISS", src)
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print("  copy ", os.path.relpath(dst, DEST), " <- ", os.path.relpath(src, ROOT))


def iter_docx():
    """按 SRC_DIRS 顺序递归收集 docx；同名以先出现的为准。"""
    seen: set[str] = set()
    for d in SRC_DIRS:
        base = os.path.normpath(os.path.join(ROOT, d))
        if not os.path.isdir(base):
            continue
        for dirpath, _dirnames, filenames in os.walk(base):
            # 仓库自身与备份目录不参与
            if os.path.normpath(dirpath) == os.path.normpath(DEST):
                _dirnames[:] = []
                continue
            _dirnames[:] = [x for x in _dirnames if not x.startswith("_") and x != "ueguden"]
            for name in sorted(filenames):
                if name.startswith("~$"):          # Office 打开文档时产生的锁文件
                    continue
                if not name.lower().endswith(".docx") or name in seen or name in EXCLUDE:
                    continue
                seen.add(name)
                yield name, os.path.join(dirpath, name)


def main() -> int:
    for src_name, dst, title, note in MD_NOTES:
        p = find(src_name, prefer="归档")
        if p:
            with_front_matter(p, os.path.join(DEST, dst), title, note)
        else:
            print("  MISS", src_name)

    for src_name, dst in TOOLS:
        copy(find(src_name, prefer="工具"), os.path.join(DEST, dst))

    for name in NOTES:
        copy(find(name, prefer="归档"),
             os.path.join(DEST, "archive", "notes", name))

    docx_dir = os.path.join(DEST, "archive", "docx")
    os.makedirs(docx_dir, exist_ok=True)
    n = 0
    for name, path in iter_docx():
        copy(path, os.path.join(docx_dir, name))
        n += 1
    print(f"\n归档 docx {n} 份 -> archive/docx/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
