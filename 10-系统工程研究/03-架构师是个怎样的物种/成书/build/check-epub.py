#!/usr/bin/env python3
"""check-epub.py — EPUB 出厂体检：XHTML/OPF 是否真的能被 XML 解析

为什么要有这一步（2026-10-19 的教训）：
  pandoc 用 `--include-in-header` 把 `table-inline.html` 原样塞进每个 xhtml 的 head。
  XHTML 按 **XML** 解析（不按 HTML），style 元素里出现裸尖括号会被当成标签——
  一句注释里写了 `<head>`，就让全书 26 个 xhtml 全崩。浏览器把 style 当原始文本、看不出毛病，
  只有 Apple Books 这类走严格 XML 的阅读器会整页报错：
  "Opening and ending tag mismatch: head line 12 and style"。
  该项此前一直"自检通过"，因为自检只数文件与表数，从不解析 XML。故立此脚本。

用法：python3 build/check-epub.py 架构师-电子版.epub [更多.epub ...]
退出码：0 全过；1 有不合规文件。
"""
import sys
import zipfile
import xml.etree.ElementTree as ET

# ★ 2026-10-20：Windows 控制台默认 GBK，脚本里的「✓」与中文路径会撞 UnicodeEncodeError，
# 于是"体检全过"被误报成"体检不过"（build.sh 第 8 步据此 return 1）。故先强制 UTF-8 输出。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001 — 老 Python／被重定向时不支持 reconfigure，忽略即可
        pass


def check(path):
    problems = []
    try:
        zf = zipfile.ZipFile(path)
    except Exception as e:  # noqa: BLE001
        return [f"{path}: 打不开 → {e}"], 0

    names = zf.namelist()
    if not names or names[0] != "mimetype":
        problems.append(f"{path}: mimetype 不是首件（EPUB 规范要求第一个且不压缩）")
    elif zf.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
        problems.append(f"{path}: mimetype 被压缩（应为 STORED）")

    targets = [n for n in names if n.endswith((".xhtml", ".html", ".opf", ".ncx"))]
    for n in targets:
        raw = zf.read(n)
        # 去掉 BOM 再解析
        try:
            ET.fromstring(raw.decode("utf-8-sig"))
        except ET.ParseError as e:
            problems.append(f"{path}:{n}: XML 解析失败 → {e}")
    return problems, len(targets)


def main(argv):
    if len(argv) < 2:
        print("用法：python3 build/check-epub.py <epub> [<epub> ...]")
        return 2
    bad = 0
    for path in argv[1:]:
        problems, n = check(path)
        if problems:
            bad += 1
            print(f"✗ {path}：{len(problems)} 处不合规（检查了 {n} 个 XML 件）")
            for p in problems[:10]:
                print("   ", p)
            if len(problems) > 10:
                print(f"    ……另 {len(problems) - 10} 处")
        else:
            print(f"✓ {path}：{n} 个 XML 件全部可解析")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
