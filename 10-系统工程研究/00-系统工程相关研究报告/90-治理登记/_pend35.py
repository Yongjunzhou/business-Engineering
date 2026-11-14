# -*- coding: utf-8 -*-
"""挂账清算（2026-11-13）：① 35 号两处清单计数（11→十项，撤销"48 号错"的判）② 35/48 界一界二按 §5.9 正文/NOTE 分层 ③ 年版口径追注 ④ 三把尺口径裁定。

    python 90-治理登记/_pend35.py [--apply]
"""
import os, re, sys

LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P35 = os.path.join(LIB, '35-架构定义与视图设计研究报告-从意义目的到产品数据与四案例.md')
P48 = os.path.join(LIB, '48-架构定义研究报告-从问题与机会到架构描述.md')
P02 = os.path.join(LIB, '90-治理登记', '02-标准条款号核对表.md')

E = []   # (文件, 旧, 新, 说明)
def A(f, o, n, t): E.append((f, o, n, t))

# ── ① 35 号：两处清单计数改回十项（附录 B 那行我自己写错了）────────────
A(P35,
  '| **§3.4 NOTE 1 那张（不可与上行混）** | **42010 §3.4 NOTE 1（资料性）** | *仍是 11 项，但计数口径不同*（§5.2.9 的"对应关系与对应方法"另加、不计入那 11 类；§3.4 NOTE 1 的 correspondences 与 correspondence methods 计入这 11 项）：stakeholder／concern／aspect／stakeholder perspective／**ADLs（架构描述语言）／ADFs（架构描述框架）**／correspondence（method）／view／view component／viewpoint／model kind——**不含** legend（图例）·architecture decision（架构决策）·architecture rationale（架构理由） |',
  '| **§3.4 NOTE 1 那张（不可与上行混）** | **42010 §3.4 NOTE 1（资料性）** | *十项*：stakeholder（相关方）／concern（关切）／aspect（方面）／stakeholder perspective（相关方视角）／view（视图）／view component（视图组件）／viewpoint（视角）／model kind（模型种类）／correspondence（对应关系）／correspondence method（对应方法）。**前四样是"在 AD、ADL、ADF 中被标识"的——ADL／ADF 是所在、不是元素本身**（正本 *stakeholders …, identified in an AD, ADLs, ADFs and correspondences…*）。**不含** legend（图例）·architecture decision（架构决策）·architecture rationale（架构理由）三样；§5.2.9 那张含这三样、并把"对应关系与对应方法"作外加（十一类＋外加）。**两处不可混，计数也不同（十 对 十一）** |',
  '①附录 B 十项')

A(P35,
  '> **★ 两处清单不可混（勘误 2026-10-12）**：**42010:2022 §3.4 NOTE 1** 列举的 AD 元素为 **11 类**',
  '> **★ 两处清单不可混（勘误 2026-10-12）**〔**追注 2026-11-13**：本条里"**11 类**"的计数**应作十项**——§3.4 NOTE 1 中 ADL／ADF 是"被标识的所在"而非元素本身（正本 *identified in an AD, ADLs, ADFs…*），数下来是 十（4＋2＋4）；准确表述见附录 B 两行。下文原字属存史，不改〕**42010:2022 §3.4 NOTE 1** 列举的 AD 元素为 **11 类**',
  '①§8.4 勘误块加追注')

# ── ② 35 号界一/界二：按 15288 §5.9 正文 vs NOTE 分层 ────────────────
A(P35,
  '- **界一（描述 vs 实体）**：**AD 元素是"描述本身的零件"**（§3.4 NOTE 1），**不等于系统元素**；',
  '- **界一（描述层 ↔ 模型层）**：**描述元素是"描述本身的零件"**（42010 §3.4 NOTE 1），**不等于模型层的位**——一张视图里的一个框，是某个位的**一次露面**，不是这个位（1:N）；',
  '②35 界一')
A(P35,
  '- **界二（② 层 vs ④ 层）**：**"两种不同的概念"**（15288 §5.9 末段）。',
  '- **界二（架构侧 ↔ 实现侧）**：15288 §5.9 **正文**说的是把 *architectural entities*（复数，即 ② 层那批单位）**分配、划分、对齐到** *system elements*——这一句撑的是"② 与 ④ 之间还隔着 ③"；同段的 **NOTE** 另说一事：*an architecture entity*（**单数，被架构的那个事物**）与系统元素"代表两种不同的概念"，**不要拿这句撑 ②↔④**（本报告附录 B 已单列此辨）。',
  '②35 界二')
A(P35,
  '**两条（三条）补充边界**', '**三条补充边界**', '②35 措辞（若在）') if False else None

# ── ③ 48 号界二：正文与 NOTE 分层 ───────────────────────────────
A(P48,
  '- **界二（架构侧 ↔ 实现侧）**：15288 §5.9 正文（规范）——*an architecture entity … and a system element … represent **two different notions***（中译：架构实体与系统元素**代表两种不同的概念**）。**位在②，系统元素在④，中间还隔着③。**',
  '- **界二（架构侧 ↔ 实现侧）**：15288 §5.9 **正文**（规范）——*…the allocation, partitioning and alignment of **architectural entities** (e.g. strategic goals, capabilities and effects, operational activities, resource functions) **to system elements** that comprise the system*（中译：把架构侧实体分配、划分并对齐到构成系统的系统元素）；同段 **NOTE** 另说：*an architecture entity … and a system element … represent **two different notions***（中译：架构实体与系统元素**代表两种不同的概念**）——**该 NOTE 的主语是"被架构的那个事物"（单数），不是 ② 层的位**。**位在②，系统元素在④，中间还隔着③。**',
  '③48 界二')

# ── ④ 02 号：年版口径追注 ─────────────────────────────────────
A(P02,
  '> **约定**：本表是**台账**，不是授权载体；',
  '> **版次口径（2026-11-13 追注，挂账清算）**：库内文件名 `ISO_IEC_IEEE 42010 2023*` 里的 **2023 是文件／译本年份，不是标准版次**——正本通篇页眉与题名均作 **42010:2022**（中英对照版首行：*ISO/IEC/IEEE 42010:2022《软件、系统与企业 — 架构描述》*）。故各报告引「42010:2022」为**正确版次**，**无须改号**；本条结清此前"文件名 2023 vs 正文 2022"的挂账。\n> **约定**：本表是**台账**，不是授权载体；',
  '④02 版次追注')

def main():
    apply = '--apply' in sys.argv
    files = {}
    for f, o, n, t in E:
        if f is None:
            continue
        if f not in files:
            files[f] = open(f, encoding='utf-8').read()
        c = files[f].count(o)
        if c != 1:
            print('MISS %-22s 命中 %d' % (t, c))
        else:
            files[f] = files[f].replace(o, n, 1)
            print('OK   ' + t)
    if not apply:
        print('（预演，未写）'); return 0
    for f, txt in files.items():
        open(f, 'w', encoding='utf-8', newline='\n').write(txt)
    print('已写入 %d 个文件' % len(files))
    return 0

sys.exit(main())
