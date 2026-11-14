# SOSA 参考架构技术标准 · 中英文对照版（施工中）

> **本目录是什么**：英文侧 [`../`](../README.md)（16 册＋合订＋`assets/` 50 图）的**中英文对照版**。英文为源文（一字不改），中文译文紧随其下。体例见 [`00-对照体例说明.md`](00-对照体例说明.md)，用词见 [`SOSA-术语对照表.md`](SOSA-术语对照表.md)。

---

## 一、已出件（可复核）

| 件 | 文件 | 作用 |
|---|---|---|
| 体例卡 | [`00-对照体例说明.md`](00-对照体例说明.md) | 对照八条、术语三档、禁令、机械关、已知代价 |
| 术语表 | [`SOSA-术语对照表.md`](SOSA-术语对照表.md) | 十二节、约 240 条；自拟译名一律标「非定译」 |
| 样章 | [`01-introduction.md`](01-introduction.md) | 全册对照，五关全过（段 45/45、页锚 7、图 2） |
| 表样 | [`00-表格分层样张.md`](00-表格分层样张.md) | 表 7（混排）／表 8（纯代码）／表 47（词典）／表 5（特办）四档 |
| 核对脚本 | [`00-对照核对.py`](00-对照核对.py) | 五关：段对齐、禁译串、术语、规范动词、表列数 |

**已译 9／16 册**（`01`、`02`、`06`、`08`、`09`、`10`、`11`、`12`、`13`），`python 00-对照核对.py` 退出码 **0**。

---

## 二、分册进度

| 文件 | 章 | 英文侧字符 | 状态 |
|---|---|---|---|
| `00-front-matter.md` | 前置：封面·目录·图表清单·序 | 34,134 | 待译（目录与图表清单按版面构件不译，见 §四） |
| `01-introduction.md` | 1 Introduction | 14,979 | **已出（样章）** |
| `02-definitions.md` | 2 Definitions | 315 | **已出** |
| `03-reference-architecture-description.md` | 3 Reference Architecture Description | 91,332 | 待译（切 4 批） |
| `04-architecture-definition.md` | 4 Architecture Definition | 34,684 | 待译（切 2 批） |
| `05-sosa-technical-standard.md` | 5 SOSA Technical Standard | 184,517 | 待译（切 8 批；含表 5 特办） |
| `06-appendix-a-stdv1.md` | Appendix A | 203 | **已出** |
| `07-appendix-b-av2-dictionary.md` | Appendix B：AV-2 集成词典 | 12,859 | 待译 |
| `08-appendix-c-use-case-details.md` | Appendix C | 1,309 | **已出** |
| `09-appendix-d-div2-and-data-dictionary.md` | Appendix D | 2,177 | **已出** |
| `10-appendix-e-div3.md` | Appendix E | 907 | **已出** |
| `11-appendix-f-connector-details.md` | Appendix F | 219 | **已出** |
| `12-appendix-g-slot-profiles.md` | Appendix G | 171 | **已出** |
| `13-appendix-h-module-details.md` | Appendix H | 193 | **已出** |
| `14-appendix-i-backplane-examples.md` | Appendix I | 8,561 | 待译 |
| `15-acronyms-and-abbreviations.md` | 缩略语与缩写 | 4,520 | 待译（107 条，缩写列不译） |
| 合订 | `SOSA参考架构技术标准-中英文对照-全文.md` | — | 待全册译完后拼 |

---

## 三、机械关

```bash
python 00-对照核对.py                    # 核全部已译分册
python 00-对照核对.py 01-introduction.md   # 核一册
```

退出码 0 为过。五关口径见 [`SOSA-术语对照表.md` §十一](SOSA-术语对照表.md)。**本轮样章一跑就抓出两类真伤**（都属"内容会静默消失"）：① 我把 3 处英文段按句拆开了（机械关报"英文段数变了"）；② 表 8 分隔行少一个 `---`，GFM 按分隔行定列数，最后一列 Comms 会连同五个 `✓` 静默消失。两类现都入关。

---

## 四、前置册的处理（已定，待用户认可）

`00-front-matter.md` 里有封面、版权页、印刷式目录、图表清单与序言。按 42010 对照版的家法：**目录与图表清单属版面构件，不译、照录**（译了也会与本目录的 Markdown 目录打架），**序言（Preface）照译**，册首加一条 `译注` 说明哪些块未译。封面版权页保留原样，只在其后加中文标题一行。

---

## 五、图不重画

图仍指 [`../assets/`](../assets/)，50 张原图不复制、不重画；框内文字本来就未转录，以原图为准。
