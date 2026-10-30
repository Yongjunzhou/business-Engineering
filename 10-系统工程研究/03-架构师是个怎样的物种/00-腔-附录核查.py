#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《架构师是个怎样的物种？》附录段体查（第四病·批四立，口径 v1.2 备用工具）

**为什么要有这个脚本**：腔量尺（`00-腔-量尺.py` 口径 v1.1）的"剔章末附录"是
`if '附录' in heading: continue`，而 `00-冗余-量尺.py` 的 `paragraphs()` 返回的
`heading` 是**最近一个二／三级标题**——附录小节名叫「A 本章概念总图」「B 本章的能力级」
「C 自查」「D 练习」，**不含"附录"二字**，故附录下的散文段其实没被剔掉。
本脚本按**块**（`## 附录` 起）重新切一遍，量化这个漏口，供口径 v1.2 修量尺时对照。

用法（本目录下）：
    python 00-腔-附录核查.py            # 各章漏口清单＋全书法
    python 00-腔-附录核查.py --ch 18    # 单章：列出被误收进池的附录段

口径要点：切段规则与 `00-冗余-量尺.py` 的 `paragraphs()` **逐字同法**（空行切段、散文行
豁免、``` 代码块跳过、参考文献／版本变更记录整块不计），只是额外记下"当前块标题"，
并在开工时自校验段数与段文本与 `paragraphs()` 完全一致——否则口径漂移。
"""
import os
import re
import sys
import io
import importlib.util
import contextlib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(BOOK, '00-冗余-量尺.py')

_spec = importlib.util.spec_from_file_location('redund_ruler', BASE)
R = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):      # 屏蔽被 import 模块的自跑输出
    _spec.loader.exec_module(R)


def parse(path):
    """与 R.paragraphs() 同法切段，多记 block（最近一个二级标题）。"""
    out, buf = [], []
    block, sub, in_code = '', '', False
    with open(path, encoding='utf-8') as f:
        head_txt = f.read()
    inline = ('**误解现场。**' in head_txt) or ('**误解现场**。' in head_txt)

    def flush():
        if not buf:
            return
        p = ' '.join(buf)
        m = R.LEAD.match(p)
        label = m.group(1) if m else ''
        k = R.kind(label) if (inline and label and R.kind(label) != 'argue') else R.kind(sub or block)
        out.append(dict(text=p, kind=k, block=block, sub=sub))
        del buf[:]

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.strip().startswith('```'):
                in_code = not in_code
                flush()
                continue
            if in_code:
                continue
            if re.match(r'^## ', line):
                flush()
                block = re.sub(r'^#+\s*', '', line).strip()
                sub = ''
                continue
            if re.match(r'^### ', line):
                flush()
                sub = re.sub(r'^#+\s*', '', line).strip()
                continue
            if not line.strip():
                flush()
                continue
            if R.is_prose(line):
                if any(s in (sub or block) for s in R.SKIP):
                    continue
                buf.append(line.strip())
            else:
                flush()
    flush()
    for i, d in enumerate(out, 1):
        d['no'] = i
    return out


def verify(path, mine):
    ref = [t for t, _, _ in R.paragraphs(path)]
    assert len(ref) == len(mine), f'段数不符 {len(ref)} vs {len(mine)}'
    for a, b in zip(ref, mine):
        assert a == b['text'], f'段文本不符：{a[:24]} | {b["text"][:24]}'


def han(t):
    return R.han(t)


def main():
    args = sys.argv[1:]
    if args[:1] == ['--ch']:
        want = args[1]
        for lbl, path in R.items():
            if lbl != want.zfill(2):
                continue
            ps = parse(path)
            verify(path, ps)
            app = [p for p in ps if '附录' in p['block']]
            print(f'ch{lbl} 全池 {len(ps)} 段｜附录块内 {len(app)} 段（应为 0；v1 口径把它们留在了池里）')
            for p in app:
                print(f'  段{p["no"]}［{p["sub"] or p["block"]}］{han(p["text"])} 汉字 破折 {p["text"].count("——")}')
                print('   ', p['text'][:60])
        return

    tot = dict(par=0, app=0, han=0, dash=0)
    print('章   全池段  附录段  附录汉字  附录内破折')
    for lbl, path in sorted(R.items()):
        ps = parse(path)
        verify(path, ps)
        app = [p for p in ps if '附录' in p['block']]
        h = sum(han(p['text']) for p in app)
        d = sum(p['text'].count('——') for p in app)
        tot['par'] += len(ps)
        tot['app'] += len(app)
        tot['han'] += h
        tot['dash'] += d
        if app:
            print(f'{lbl:<5}{len(ps):>6}{len(app):>8}{h:>10}{d:>12}')
    print(f'合计 全池段 {tot["par"]}｜附录段 {tot["app"]}（{100.0 * tot["app"] / tot["par"]:.1f}%）'
          f'｜附录散文汉字 {tot["han"]}｜附录内破折 {tot["dash"]}')
    print('★ 这三笔就是口径 v1.1 的漏口；v1.2 改成"按块判"后，段池、破折‰、三连‰ 都会小幅回落。')


if __name__ == '__main__':
    main()
