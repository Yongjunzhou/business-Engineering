#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""核对-46v26对齐.py —— 「26 件随 46 号 v2.6 严格对齐」的机械体检（只读）。

用法（在本目录 00-系统工程相关研究报告/ 下）：
    python 90-治理登记/核对-46v26对齐.py
    python 90-治理登记/核对-46v26对齐.py --quiet

退出码：0＝无硬违规；1＝有硬违规。

判七件（逐件）：
  ① **已改**：文件相对 HEAD 有差异（没改过的件必是漏办）；
  ② **回执行**：新增了「随 46 号 v2.6」的修订条目（版本层留痕）；
  ③ **旧号残影**：指 46 号却仍写旧节号（§9.x／§11.3／§11.4／§12.x／§13.x），
     排除"修订记录／版本行／2026-10 及更早日期行"（那些是存史，允许）；
  ④ **K 号未动**：结论台账 `| Knn ` 行数与 HEAD 相同；
  ⑤ **案例数字未动**：M3-0417／30 s／≥72 h／±0.5 等计数与 HEAD 相同；
  ⑥ **表格列数**：每个连续表块的列数一致（转义竖线 `\\|` 不计）；
  ⑦ **目录锚点**：每个 `](#x)` 必须解析到存在的标题（GitHub 风格 slug）——
     防的是**错链**：断链事小，点进去落到别处事大。

硬违规＝③（正文部分）／④／⑤／⑥／⑦；①② 作提示（缺 ② 而 ① 有差异，说明漏了版本留痕）。
"""
import os
import re
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.dirname(HERE)

FILES = [
    '06-架构概念研究报告-从术语到实践.md',
    '12-工程师与架构师能力研究报告-从工程师到CTO.md',
    '22-架构、概念、属性研究报告—术语权威定义与对照分析.md',
    '24-架构与设计边界研究报告-从定义辨析到架构视角与架构视图.md',
    '28-治理概念研究报告-从ISO 37000定义到域治理实例.md',
    '29-架构治理研究报告-从标准依据到责任主体.md',
    '30-架构描述核心概念研究报告-从四个定义到判据与治理接驳.md',
    '32-架构视角与关切判据研究报告-从视角集到关切裁决.md',
    '34-架构与设计过程模型研究报告-从术语定义到双线过程.md',
    '35-架构定义与视图设计研究报告-从意义目的到产品数据与四案例.md',
    '36-架构描述与架构视图价值研究报告-从清单与描述的分野到视角自建与四案例.md',
    '37-架构视图口径研究报告-从三词定位到七类视图与三张清单并附HUD·EOS·冷链·合同审批四套示例.md',
    '38-架构权衡与架构决策研究报告-从标准定义与过程落点到决策记录装置.md',
    '39-架构师职责与产品数据研究报告-从架构工作定义到过程级责任矩阵.md',
    '40-架构治理研究报告-从名词与动作到四案对证.md',
    '42-架构研究报告-从定义句与目的到三张清单治理与视图.md',
    '43-企业信息系统合规开发过程研究报告-从四层单向链到配置载体治理.md',
    '44-平视显示器架构描述与系统组成说明研究报告-从目的目标清单到三视图与一份册子.md',
    '45-EOS平台架构描述与系统组成说明研究报告-从目的关切到三视图与一份册子.md',
    '48-架构定义研究报告-从问题与机会到架构描述.md',
    # 第二批（扫描批发现后补办）
    '07-架构概念研究报告-从概念设计到架构.md',
    '08-治理概念研究报告-从词源到翻译史.md',
    '11-工程师六项能力研究报告-从工程定义到能力培养.md',
    '13-工程角色谱系研究报告-从模块工程师到系统架构师.md',
    '16-构思定义设计关系及架构活动研究报告.md',
    '18-四角色与型号总师系统研究报告.md',
]

CASE_TOKENS = ['M3-0417', '30 s', '≥72 h', '±0.5']

# 2026-11-14 37 号重构轮：用户裁「冷链断链口径按 48 号 §14.1 末分两量」——断链门槛改 ≥N 分钟、
# 告警时延改「≤三十秒」，故该件正文的 "30 s" 由 9 处降为 0，属**已授权的口径变更**，不是漂移。
# 记在：37 号 v2.0 修订记录、`claude-memory/pending-37冷链断链口径.md`。
CASE_EXPECT_DELTA = {
    # 30 s：冷链口径分两量（见上）；±0.5：《摘要》由十七条并为九条后，原第 15 条对案例的重述并入
    # 要点，正文四套示例（现 §11.2~§11.5）的案例数字一处未动（`pending-37冷链断链口径.md` 同记）。
    '37': {'30 s': 0, '±0.5': 8},
}
OLD_PTR = re.compile(r'46\s*号[（(]?新?[）)]?[^。\n]{0,20}?§\s*(9\.\d|11\.[34]|12\.\d|13\.\d)')

# 2026-11-13 修（36 号对齐轮）：v2.6 的 §9.x 是**现行号**（§9.1~§9.6），旧启发式把它一律当旧号，
# 凡引「46 号 §9.5」即误判。按 19 号规程「按现行目录判，不用附录 E 左列」：先从 46 号现行标题
# 取出全部节号集合，命中该集合者不算旧号残影。
CUR_46 = None


def cur46_nums():
    t = read(os.path.join(LIB, '46-架构内容与架构描述研究报告-二者的目的、存在理由与关系.md'))
    return set(re.findall(r'(?m)^#{2,4} (\d+(?:\.\d+)*)', t))
HIST = ('修订记录', '修订行', '版本行', '历史', '旧号', '判留', '存史')
HIST_DATE = re.compile(r'20(2[0-5])-(0[1-9]|1[0-2])')
HIST_ROW = re.compile(r'^\|\s*\*{0,2}v[\d.]')
HIST_PARA = re.compile(r'^\*{0,2}v\d')


def is_history(ln):
    """存史行：修订记录表行／修订记录段落／版本链行／含旧日期行。"""
    if HIST_ROW.match(ln) or HIST_PARA.match(ln):
        return True
    if '文档版本' in ln or '版本 v' in ln:
        return True
    if '→ v' in ln or '→v' in ln or '→ **v' in ln:
        return True
    if any(h in ln for h in HIST):
        return True
    # 本轮新增的修订条目（自陈改动与判留）
    if '46 号 v2.6' in ln and ('改动' in ln or '判留' in ln or '对齐' in ln):
        return True
    m = HIST_DATE.search(ln)
    if m and '2026-11-11' not in ln:
        return True
    return False


def read(p):
    with open(p, 'rb') as f:
        return f.read().decode('utf-8-sig')


def head_text(name):
    try:
        out = subprocess.run(
            ['git', 'show', 'HEAD:./' + name],
            cwd=LIB, capture_output=True, check=True)
        return out.stdout.decode('utf-8-sig')
    except Exception:
        return None


def body_only(t):
    """去掉存史行（修订记录／版本链），只留正文——比对案例数字与旧号都按正文算。"""
    return '\n'.join(ln for ln in t.split('\n') if not is_history(ln))


def count_k(t):
    return len(re.findall(r'(?m)^\|\s*K\d\d\s', t))


def case_counts(t):
    b = body_only(t)
    return {k: b.count(k) for k in CASE_TOKENS}


def table_problems(lines):
    bad = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('|'):
            start = i
            cols = []
            while i < len(lines) and lines[i].startswith('|'):
                s = lines[i].replace('\\|', '\u0000')
                cols.append(s.strip().strip('|').count('|') + 1)
                i += 1
            if len(set(cols)) > 1:
                bad.append('lines %d-%d cols=%s' % (start + 1, i, cols))
        else:
            i += 1
    return bad


def _slug(s):
    s = s.lower()
    s = re.sub(r'[^\w\u4e00-\u9fff\- ]', '', s)
    return s.replace(' ', '-')


def anchor_problems(text):
    """目录↔标题逐条相等：每个 ](#x) 必须解析到一个存在的标题（GitHub 风格 slug）。

    标题层级取 h1~h4——报告库里有把附录与修订记录写成 `# 附录 A…` 的体例。
    """
    heads = {_slug(m.group(1).strip())
             for m in re.finditer(r'(?m)^#{1,4} (.+)$', text)}
    broken = [l for l in re.findall(r'\]\(#([^)]+)\)', text) if l not in heads]
    return broken


def main():
    quiet = '--quiet' in sys.argv
    rows, hard = [], []
    for name in FILES:
        p = os.path.join(LIB, name)
        if not os.path.exists(p):
            hard.append('%s：文件不存在' % name[:2])
            continue
        cur = read(p)
        old = head_text(name)
        changed = (old is None) or (cur != old)
        has_note = ('46 号 v2.6' in cur) or ('46 号（v2.6）' in cur)

        # ③ 旧号残影（排除存史行；命中的节号若在 46 号现行标题集合内，则不算旧号）
        global CUR_46
        if CUR_46 is None:
            CUR_46 = cur46_nums()
        ptr = []
        skipped = 0
        for ln_no, ln in enumerate(cur.split('\n'), 1):
            if not OLD_PTR.search(ln):
                continue
            if OLD_PTR.search(ln).group(1) in CUR_46:
                continue
            if is_history(ln):
                skipped += 1
                continue
            ptr.append((ln_no, OLD_PTR.search(ln).group(0)))

        k_now = count_k(cur)
        k_old = count_k(old) if old else k_now
        k_bad = (k_now != k_old)

        c_now = case_counts(cur)
        c_old = case_counts(old) if old else c_now
        expect = CASE_EXPECT_DELTA.get(name[:2], {})
        case_bad = [k for k in CASE_TOKENS
                    if c_now[k] != expect.get(k, c_old[k])]

        tbad = table_problems(cur.split('\n'))
        abad = anchor_problems(cur)

        if ptr:
            hard.append('%s：旧号残影 %d 处 %s' % (name[:2], len(ptr), ptr[:3]))
        if k_bad:
            hard.append('%s：K 行数变 %d→%d' % (name[:2], k_old, k_now))
        if case_bad:
            hard.append('%s：案例数字计数变 %s' % (name[:2],
                       ', '.join('%s %d→%d' % (k, c_old[k], c_now[k]) for k in case_bad)))
        if tbad:
            hard.append('%s：表列数不一致 %s' % (name[:2], tbad[:2]))
        if abad:
            hard.append('%s：目录锚点断 %d 条（首个：%s）' % (name[:2], len(abad), abad[0]))

        rows.append((name[:2], 'changed' if changed else 'UNCHANGED',
                     'note' if has_note else 'NO-NOTE', len(ptr), k_now,
                     'ok' if not tbad else 'BAD', len(abad)))

    if not quiet:
        print('== 逐件读数（26 件）==')
        print('  %-4s %-10s %-8s %-6s %-4s %-4s %s' % ('号', '相对HEAD', '版本行', '旧号', 'K', '表', '锚点'))
        for r in rows:
            print('  %-4s %-10s %-8s %-6d %-4d %-4s %d' % r)
        print('\n== 硬违规 ==')
        for h in hard:
            print('  - ' + h)
    ok = not hard
    print('\n件 %d｜硬违规 %d｜%s' % (len(rows), len(hard),
                                     'PASS' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
