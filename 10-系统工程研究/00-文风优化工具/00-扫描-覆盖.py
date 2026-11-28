# -*- coding: utf-8 -*-
"""扫描覆盖：正文散文句数与扫描单行数对账。只报不判。

用法：
  python 00-扫描-覆盖.py <正文.md> --emit        # 按正文生成扫描单骨架
  python 00-扫描-覆盖.py <正文.md> <扫描单.md>    # 对账；不等即退出码 1

口径：
  正文只数散文句：标题、表格行、引文块、代码块不计；表格按格，不按句。
  句以 。！？!? 切；一行多句的，逐句计。
  扫描单认两种行：Markdown 表首格为数字的行，或行首为「1.」「1、」的行。
"""
import sys, re, io, argparse

CJK = re.compile(r'[一-鿿]')
SENT_END = re.compile(r'(?<=[。！？!?])')


def prose_sentences(path):
    out = []
    in_code = False
    for raw in io.open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        s = line.strip()
        if not s:
            continue
        if s.startswith('#') or s.startswith('|') or s.startswith('>') or s.startswith('---'):
            continue
        s = re.sub(r'^\s*(?:[-*+]|\d+[.、])\s+', '', s)
        for part in SENT_END.split(s):
            part = part.strip()
            if part and CJK.search(part):
                out.append(part)
    return out


def ledger_rows(path):
    rows = []
    for raw in io.open(path, encoding='utf-8'):
        s = raw.strip()
        m = re.match(r'^\|\s*(\d+)\s*\|', s)
        if m:
            rows.append(m.group(1))
            continue
        m = re.match(r'^\s*(\d+)[.、]\s+', s)
        if m:
            rows.append(m.group(1))
    return rows


def main(argv):
    ap = argparse.ArgumentParser(description='正文散文句数与扫描单行数对账')
    ap.add_argument('body')
    ap.add_argument('ledger', nargs='?')
    ap.add_argument('--emit', action='store_true', help='按正文生成扫描单骨架')
    a = ap.parse_args(argv)

    sents = prose_sentences(a.body)

    if a.emit:
        print('| 句序 | 原句 | 类别 | 处置 | 理由 |')
        print('|---|---|---|---|---|')
        for i, s in enumerate(sents, 1):
            print('| %d | %s |  |  |  |' % (i, s))
        print('正文散文句 %d 句' % len(sents), file=sys.stderr)
        return 0

    if not a.ledger:
        print('需要扫描单路径；只生成骨架用 --emit', file=sys.stderr)
        return 2

    rows = ledger_rows(a.ledger)
    diff = len(sents) - len(rows)
    print('正文散文句 %d｜扫描单行 %d｜差 %d' % (len(sents), len(rows), diff))
    if diff != 0:
        print('缺口：扫描单行数与正文散文句数不等，扫描未做。', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
