#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《架构师是个怎样的物种？》表达量尺（口径 v1，18 章散文层）

用途：**"读者是不是更容易理解"这件事的可复算那一半**——配额与形态的自查与清单产出。
     与 `00-标题-量尺.py` 分工：那把管题面，这把管正文。
     口径变更必须先改本文件并在 `00-风格参考.md` §6.6／`00-逐章修订手册.md` §2.10 留痕。

口径 v1（2026-10-17 立；配套 `00-风格参考.md` §6.5 啰嗦三条、§6.6 白话优先、§6.10 句子十条）
- **量什么**：只量**散文段**——按空行切段；**豁免**标题行、表格行、代码围栏内、引用块（`>`，含台词与概念卡）、
  清单行（`- `／`1. ` 等）、章前件（`**…**：` 型标签行）。判据：读者是"顺着读"还是"查着看"，只算顺着读的那部分。
- **读数单位**：汉字 `[\\u4e00-\\u9fff]`；编号、标点、拉丁字母与阿拉伯数字不计。
- **六类读数**（**只报不判**——判读仍按 §6.10 十条人工过）：
  ① **段 >150 汉字**（散文段红线，取自框架 §五 第 10 条与案例镜照 ≤150 同源）
  ② **句中位**（句以「。」断；判据 §6.9 呼吸）
  ③ **最长句**（诊断"读一遍要停一下"的第一大来源）
  ④ **破折号密度**（‰，每千散文汉字；红线 ≤10‰）
  ⑤ **白话命中**（§6.6 行话词表逐词计数；提示线 **每章 ≤10 次**）
  ⑥ **括号对／嵌套括号**（§6.6 判据 3"括号里不再套括号"；嵌套数应恒为 0）
  另报：**加粗对数与其千字密度**（§6.5 啰嗦、手册 §2.10 slim_bold 口径，只报不判）。

**★ 与旧读数的关系（口径差异须登记）**：`00-风格参考.md` §6.6 记的"2026-10-16 实测（全书 291 次／中位 11.5／
最高 ch06 51）"与 `claude-memory/pending-titles-and-expression.md` §二 记的"2026-10-17（ch06 33）"**是两次不同口径的读数**，
两把旧尺都不在库。本尺立后，**以本尺读数为唯一口径**；旧数作历史留痕，不追平、也不再引用。

用法：在本目录下 `python 00-表达-量尺.py`（只读，不改文件）；`--show 06` 看该章逐条明细。
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
HAN = re.compile(r'[\u4e00-\u9fff]')
# §6.6 行话词表（无定义、无户口的字面行话；户口术语如"枢纽／根概念／能力四级／归零项"不在此列）
PLAIN_WORDS = ['口径', '落点', '归位', '挂载', '作业', '颗粒度', '内蕴', '正交',
               '因子', '代理', '可审计', '操作版', '上沿', '收束']
LIMITS = {'段>150': 0, '破折号‰': 10.0, '白话': 10, '嵌套括号': 0}


def han(s):
    return len(HAN.findall(s))


def is_prose(line):
    t = line.strip()
    if not t:
        return False
    for pre in ('#', '|', '>', '```', '---', '- ', '* ', '+ ', '　'):
        if t.startswith(pre):
            return False
    if re.match(r'^\d+[.、)]\s', t):
        return False
    if re.match(r'^\*\*[^*]+：\*\*', t):   # 章前件标签行
        return False
    return True


def chapter_files():
    out = {}
    for name in sorted(os.listdir(BOOK)):
        m = re.match(r'^(\d\d)-第(\d+)章-(.+)\.md$', name)
        if m and '分析' not in name:
            out[int(m.group(2))] = os.path.join(BOOK, name)
    return out


def analyse(path):
    paras, para = [], []
    in_code = False
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.strip().startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            if not line.strip():
                if para:
                    paras.append(' '.join(para))
                    para = []
                continue
            if is_prose(line):
                para.append(line.strip())
            else:
                if para:
                    paras.append(' '.join(para))
                    para = []
    if para:
        paras.append(' '.join(para))

    text = '\n'.join(paras)
    total = han(text)
    long_paras = [p for p in paras if han(p) > 150]
    sentences = [s for s in re.split(r'。', text) if han(s) >= 2]
    lens = sorted(han(s) for s in sentences)
    median = lens[len(lens) // 2] if lens else 0
    longest = lens[-1] if lens else 0
    dash = text.count('——')
    words = {w: text.count(w) for w in PLAIN_WORDS if text.count(w)}
    pairs = text.count('（')
    nested = 0
    for m in re.finditer(r'（[^（）]*（', text):
        nested += 1
    bold = len(re.findall(r'\*\*[^*]+\*\*', text))
    return {
        'total': total, 'paras': len(paras), 'long': long_paras,
        'median': median, 'longest': longest,
        'dash_pm': (dash * 1000.0 / total) if total else 0.0,
        'words': words, 'plain': sum(words.values()),
        'pairs': pairs, 'nested': nested,
        'bold': bold, 'bold_pm': (bold * 1000.0 / total) if total else 0.0,
    }


def main():
    files = chapter_files()
    show = None
    if '--show' in sys.argv:
        i = sys.argv.index('--show')
        if i + 1 < len(sys.argv):
            show = int(sys.argv[i + 1])

    print('=' * 108)
    print('表达量尺（口径 v1，18 章散文层）—— 只报不判；骨架仍须按 §6.10 十条人工过')
    print('=' * 108)
    hdr = '章  散文汉字  段数  段>150  中位句长  最长句  破折号‰  白话  括号对  嵌套  加粗‰'
    print(hdr)
    rows = {}
    for ch in sorted(files):
        r = analyse(files[ch])
        rows[ch] = r
        print('%02d  %8d  %4d  %6d  %8d  %6d  %8.2f  %4d  %6d  %4d  %6.2f' % (
            ch, r['total'], r['paras'], len(r['long']), r['median'], r['longest'],
            r['dash_pm'], r['plain'], r['pairs'], r['nested'], r['bold_pm']))

    tot = sum(r['total'] for r in rows.values())
    print('-' * 108)
    print('合计 %d 汉字｜中位句长 %d｜最长句 %d｜段>150 共 %d 段｜白话共 %d 次｜嵌套括号共 %d 处｜加粗共 %d 对' % (
        tot,
        sorted(r['median'] for r in rows.values())[len(rows) // 2],
        max(r['longest'] for r in rows.values()),
        sum(len(r['long']) for r in rows.values()),
        sum(r['plain'] for r in rows.values()),
        sum(r['nested'] for r in rows.values()),
        sum(r['bold'] for r in rows.values())))

    print('\n【红线／提示线超线汇总】')
    over = {k: [] for k in LIMITS}
    for ch in sorted(rows):
        r = rows[ch]
        if len(r['long']) > LIMITS['段>150']:
            over['段>150'].append('ch%02d %d 段' % (ch, len(r['long'])))
        if r['dash_pm'] > LIMITS['破折号‰']:
            over['破折号‰'].append('ch%02d %.2f‰' % (ch, r['dash_pm']))
        if r['plain'] > LIMITS['白话']:
            over['白话'].append('ch%02d %d 次' % (ch, r['plain']))
        if r['nested'] > LIMITS['嵌套括号']:
            over['嵌套括号'].append('ch%02d %d 处' % (ch, r['nested']))
    for k in ('段>150', '破折号‰', '白话', '嵌套括号'):
        print('  %-7s 红线 %-5s → 超线 %d 章：%s' % (
            k, LIMITS[k], len(over[k]), '｜'.join(over[k]) if over[k] else '无'))

    if show and show in rows:
        r = rows[show]
        print('\n【ch%02d 明细】散文 %d 汉字／%d 段；白话命中 %s' % (
            show, r['total'], r['paras'],
            '、'.join('%s×%d' % (w, n) for w, n in r['words'].items()) or '无'))
        print('  段 >150：%d 段（最长 %d 汉字段）' % (
            len(r['long']), max((han(p) for p in r['long']), default=0)))
        for p in sorted(r['long'], key=han, reverse=True)[:10]:
            print('   · %3d 字｜%s…' % (han(p), p[:46]))


if __name__ == '__main__':
    main()
