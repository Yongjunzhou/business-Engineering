#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""研究报告库「用途登记表」核对器

用途：让"哪份报告有人认领、落在谁家"这件事可复算，不靠记性。核对五件：
  ① 表内号是否在 00~50 区间、无重号（允许有意留空，留空号只打印提示）；
  ② 表与文件是否双向对得上（表里有号必有件，件里有号必在表）；
  ③ 状态与落点是否在用封闭词表、落点章号是否真有那一章；
  ④ 04 侧取料单与表是否一致（表说 04 用的号，取料单里必须有；反之亦然）；
  ⑤ 有随章取料单（claude-memory/pending-align-textbook-to-NN.md）的号，
     表内 03 列不得写「—」（那是已认领的证据）。

用法：`python 90-治理登记/核对-报告用途.py`（在本目录 `00-系统工程相关研究报告/` 下运行亦可）。
口径与词表见同目录 `08-报告用途登记.md`（用途的唯一权威），04 侧视图见
`../../04-可运行的运营体系开发方法/00-取料单.md`。

退出码：0＝全过；1＝有缺口。
"""
import os
import re
import glob
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))          # 10-系统工程研究/
RDIR = os.path.dirname(HERE)                            # 00-系统工程相关研究报告/
BOOK = os.path.join(REPO, '03-架构师是个怎样的物种')
PICK = os.path.join(REPO, '04-可运行的运营体系开发方法', '00-取料单.md')
MEM = os.path.join(REPO, 'claude-memory')
REG = os.path.join(HERE, '08-报告用途登记.md')

CH_NUM = 19          # 教材书章数（2026-10-27 起：新第18章入册，《架构师》后移为第19章，全书十九章）
UNIT_NUM = 20        # 培训教材单元数（单元号＝章号，20＝附录；2026-10-27 同步 19→20，待训侧重派生落地）
RANGE = (0, 50)      # 表内应覆盖的报告号区间（允许区间内留空，见 ① 提示）

S03 = ('已落', '备料', '背景', '—')
S04 = ('主料', '背景', '—', '待核')
SEOS = ('引用', '—')
SURE = ('已核', '待核')


def table_rows():
    """从登记件里取数据行：形如 | 21 | … | 的行；返回 [[cell,…], …]。"""
    rows = []
    for ln in open(REG, encoding='utf-8').read().split('\n'):
        if not ln.startswith('|'):
            continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cells) < 6:
            continue
        if re.fullmatch(r'\d{2}', cells[0]):
            rows.append(cells)
    return rows


def files_by_no():
    """报告库里带号的文件，按号归组：{号: [文件名, …]}。"""
    out = {}
    for f in glob.glob(os.path.join(RDIR, '[0-9][0-9]-*.md')):
        n = os.path.basename(f)[:2]
        out.setdefault(n, []).append(os.path.basename(f))
    return out


def chapters():
    """教材书现行的 18 章：(章号, 文件名)，不含派生件「从教材到问题分析」。"""
    out = {}
    for f in glob.glob(os.path.join(BOOK, '*.md')):
        b = os.path.basename(f)
        m = re.match(r'\d\d-第(\d+)章', b)
        if m and '从教材到问题分析' not in b:
            out[int(m.group(1))] = b
    return out


def pick_numbers():
    """04 侧取料单里出现的报告号。"""
    if not os.path.exists(PICK):
        return None
    txt = open(PICK, encoding='utf-8').read()
    return set(re.findall(r'(?<!\d)(\d{2})(?=\s*号)', txt))


def main():
    bad = []
    rows = table_rows()
    if not rows:
        bad.append('登记件里没有解析到任何数据行')
    nos = [r[0] for r in rows]
    lo, hi = RANGE

    # ① 号齐全、连续、无重号
    dup = sorted({n for n in nos if nos.count(n) > 1})
    if dup:
        bad.append('重号：%s' % '、'.join(dup))
    want = ['%02d' % i for i in range(lo, hi + 1)]
    missing = [n for n in want if n not in nos]
    extra = [n for n in nos if n not in want]
    if extra:
        bad.append('表内有区间外的号：%s' % '、'.join(extra))
    if missing:
        print('提示：号段内留空 %s（允许，但应是有意留空，见登记件 §五）'
              % '、'.join(missing))

    # ② 表与文件双向
    byno = files_by_no()
    for n in nos:
        if n not in byno:
            bad.append('%s 号：表内有、报告库里没有对应文件' % n)
    for n in sorted(byno):
        if n not in nos:
            bad.append('%s 号：报告库里有（%s）、表内没有' % (n, byno[n][0]))

    # ③ 词表与落点
    chs = chapters()
    for r in rows:
        n, col03, col04, col_eos = r[0], r[2], r[3], r[4]
        if not any(col03.startswith(s) for s in S03):
            bad.append('%s 号：03 列取值不合法（%s）' % (n, col03))
        if col04 not in S04 and not col04.startswith('主料'):
            bad.append('%s 号：04 列取值不合法（%s）' % (n, col04))
        if col_eos not in SEOS:
            bad.append('%s 号：EOS 列取值不合法（%s）' % (n, col_eos))
        if len(r) >= 7 and r[6] not in SURE:
            bad.append('%s 号：核列取值不合法（%s）' % (n, r[6]))
        if col03.startswith('已落'):
            for num in re.findall(r'ch(\d+)', col03):
                k = int(num)
                if not 1 <= k <= CH_NUM:
                    bad.append('%s 号：落点 ch%d 超出 %d 章' % (n, k, CH_NUM))
                elif k not in chs:
                    bad.append('%s 号：落点 ch%d 在教材书里找不到那一章' % (n, k))
            if '附录' in col03 and not glob.glob(
                    os.path.join(BOOK, '[0-9][0-9]-附录.md')):
                bad.append('%s 号：落点写「附录」，但教材书里找不到 NN-附录.md' % n)
        for num in re.findall(r'单元(\d+)', col03):
            k = int(num)
            if not 1 <= k <= UNIT_NUM:
                bad.append('%s 号：落点 单元%d 超出 %d 单元' % (n, k, UNIT_NUM))

    # ④ 04 取料单一致性
    pn = pick_numbers()
    if pn is None:
        bad.append('04 侧取料单不存在：%s' % os.path.relpath(PICK, REPO))
    else:
        use04 = {r[0] for r in rows if not r[3].startswith('—')}
        for n in sorted(use04 - pn):
            bad.append('04 号 %s：登记表说 04 要用，取料单里没有' % n)
        for n in sorted(pn - {r[0] for r in rows}):
            bad.append('04 号 %s：取料单里提到，登记表里没有这一行' % n)

    # ⑤ 随章取料单 ↔ 03 列
    for f in sorted(glob.glob(os.path.join(MEM, 'pending-align-textbook-to-*.md'))):
        m = re.search(r'to-(\d+)\.md$', os.path.basename(f))
        if not m:
            continue
        n = '%02d' % int(m.group(1))
        row = next((r for r in rows if r[0] == n), None)
        if row is None:
            bad.append('%s 号：有随章取料单（%s），登记表里没有这一行'
                       % (n, os.path.basename(f)))
        elif row[2].startswith('—'):
            bad.append('%s 号：有随章取料单（%s），但 03 列写「—」'
                       % (n, os.path.basename(f)))

    # 汇总
    print('登记件：%s' % os.path.relpath(REG, REPO))
    print('数据行：%d 行（区间 %02d~%02d）｜报告库带号文件：%d 号'
          % (len(rows), lo, hi, len(byno)))
    stat = {}
    for r in rows:
        for c, nm in ((r[2], '03'), (r[3], '04'), (r[4], 'EOS')):
            key = c.split()[0] if c.startswith('已落') else c
            stat[(nm, key)] = stat.get((nm, key), 0) + 1
    for nm in ('03', '04', 'EOS'):
        seg = '／'.join('%s %d' % (k, v) for (a, k), v in sorted(stat.items()) if a == nm)
        print('  %-4s %s' % (nm, seg or '—'))
    if bad:
        print('\n缺口 %d 条：' % len(bad))
        for b in bad:
            print('  - ' + b)
        return 1
    print('\n全过（号无重号且不越界、表↔件双向对上、词表与落点合法、04 取料单一致、随章取料单已认领）。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
