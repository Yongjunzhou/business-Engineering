# SOSA 参考架构技术标准 · 术语对照表（中英）

> **本件性质**：`Technical Standard for SOSA™ Reference Architecture, Edition 1.0, Version 2`（The Open Group Snapshot）中英文对照版的**术语定译件**。对照版全部 16 册的中文用词以此表为准；本表未收的词，按 §十一 的判据临时定，并回填本表。

> **三档标注**：**直译**＝中文有稳定对应，正文直接用中文；**存原词**＝中文无稳定对应，正文用英文原词并在首次出现处括注一次中文，其后一律用原词；**自拟**＝有中文说法但无定译，译名系本文件所定，**非定译**，日后不得当权威译法引用。

> **规范动词**：`shall`→应、`shall not`→不应、`should`→宜、`should not`→不宜、`may`→可（许可）、`must`→必须。此六条不分档，一律照用。

---

## 一、规范关键字与条目标目

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| Rule | 规则 | 直译 | 原文条目标目形如 `Rule 5.2.18-1`，**标目连同编号一律原样不译**；正文说"规则"时用中文 |
| Recommendation | 推荐 | 直译 | 条目标目 `Recommendation …` 原样不译；与 `Suggestion` 分译，不合成"建议" |
| Suggestion | 建议 | 直译 | — |
| Permission | 许可 | 直译 | — |
| Observation | 观察 | 直译 | 原文定义为"不提具体建议、只点明后果与理由"的条目；不译"注意事项" |
| Conformance Methodology | 符合性方法 | 直译 | 原文多作 `Conformance Methodology: (TBD)`，`(TBD)` 原样保留 |
| descriptive in nature | 描述性 | 直译 | §1.5.3 用语：未挂关键字者按描述性理解 |

> **注**：本件 `shall`／`should`／`may` 的用法与原书 §1.5.2 的定义一致；`shall` 187 处、`should` 53 处、`may` 121 处、`must` 12 处（英文侧读数），中文侧计数按 [§十一](#十一机械关口径) 第 4 项核。

---

## 二、架构与描述

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| architecture | 架构 | 直译 | 本项目既定口径 |
| reference architecture | 参考架构 | 直译 | 本件标题即 `SOSA Reference Architecture`→SOSA 参考架构 |
| architecture description | 架构描述 | 直译 | 依 GB/T 45630-2025 与 24 号报告附录 A |
| architecture principle | 架构原则 | 直译 | 原书 §3.2 分业务向（Business-Oriented）与技术向（Technically-Oriented）两组 |
| architecture view | 架构视图 | 直译 | 本件少用；原书用 DoDAF 制品号指称，见 §七 |
| viewpoint / viewpoint model | 视角／视角模型 | 直译 | 依 42010:2022 与 GB/T 45630-2025 |
| quality attribute | 质量属性 | 直译 | 表 1 十条，见 §六 |
| capability | 能力 | 直译 | — |
| function | 功能 | 直译 | 术语位一律"功能"；纯数学语境不入术语位 |
| behavior | 行为 | 直译 | — |
| interface | 接口 | 直译 | — |
| interaction | 交互 | 直译 | 与 interface 分开：接口是界，交互是往来 |
| entity | 实体 | 直译 | — |
| architectural entity | 架构实体 | 直译 | AV-2 对 `SOSA module` 的定义用语 |
| instantiate / instantiation | 实例化／实例 | 直译 | — |
| abstraction | 抽象 | 直译 | — |
| facet | 侧面 | 自拟 | 图 1 `The Facets that Comprise a SOSA Module`；原书无定义条目 |
| trade-off | 权衡 | 直译 | — |

---

## 三、物项与硬件

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| module | 模块 | 直译 | `SOSA module`→SOSA 模块；分册 §三 与 §四 的模块名一律照 §四 |
| hardware element | 硬件元素 | 直译 | AV-2 定义条目；不译"硬件单元" |
| software component | 软件组件 | 直译 | 与 `hardware element` 并列 |
| software application | 软件应用 | 直译 | — |
| firmware | 固件 | 直译 | — |
| SOSA sensor | SOSA 传感器 | 直译 | 本标准的主题物项 |
| sensor system | 传感器系统 | 直译 | — |
| sensor type | 传感器类型 | 直译 | 五类：Communications、EO/IR、EW、Radar、SIGINT，见 §八 |
| sensor modality | 传感器模态 | 自拟 | 原书与 `sensor type` 近似而不等同；不译"体制" |
| host platform | 宿主平台 | 直译 | — |
| platform | 平台 | 直译 | AV-2 提示该词三义（装置／载具／计算基础设施），正文按语境留"平台" |
| pod | 吊舱 | 直译 | AV-2 未单列；`SOSA sensor pod`→SOSA 传感器吊舱 |
| turret / turreted sensor | 转塔／转塔式传感器 | 直译 | 表 6 `Turreted Sensor Classes`→转塔式传感器类别 |
| imaging turret | 成像转塔 | 直译 | — |
| gimbal | 万向架 | 直译 | — |
| aperture | 孔径 | 直译 | 天线／成像口径义；模块名见 §四 |
| transducer | 换能器 | 直译 | — |
| conditioner | 调理器 | 直译 | MORA 信号链部件 |
| exciter | 激励器 | 直译 | 与 receiver 对应 |
| receiver | 接收机 | 直译 | — |
| laser | 激光器 | 直译 | — |
| camera | 相机 | 直译 | — |
| plug-in card | 插卡 | 直译 | 不译"插入式卡"；`SOSA plug-in card`→SOSA 插卡 |
| slot profile | 槽位配置档 | 自拟 | VITA 65.1 术语，中文无定译；正文首次括注后一律存原词 `slot profile` |
| module profile | 模块配置档 | 自拟 | 同上，正文存原词 `module profile` |
| backplane | 背板 | 直译 | — |
| backplane connector | 背板连接器 | 直译 | — |
| chassis | 机箱 | 直译 | — |
| chassis manager module (CMM) | 机箱管理模块 | 直译 | 缩写原样 |
| chassis management controller (ChMC) | 机箱管理控制器 | 直译 | 缩写原样 |
| payload | 载荷 | 直译 | `C4ISR payload`→C4ISR 载荷 |
| switch / switch card | 交换机／交换卡 | 直译 | 数据平面上的交换功能，不译"开关" |
| single board computer (SBC) | 单板计算机 | 直译 | 缩写原样 |
| power supply module (PSM) | 电源模块 | 直译 | 缩写原样 |
| mezzanine module | 夹层模块 | 直译 | `XMC` 属夹层卡，缩写原样 |
| rear transition module | 后置转接模块 | 直译 | — |
| connector | 连接器 | 直译 | — |
| contact | 接触件 | 直译 | 不译"触点"：表 8 注中 `Contacts … shall be populated by a dummy plug` |
| pin / pin allocation | 引脚／引脚分配 | 直译 | 表题 `Pin Allocation`→引脚分配 |
| insert pattern / insert | 插针排布 | 自拟 | 如 `21-11 insert`→21-11 插针排布；数字串原样 |
| keying | 键位 | 直译 | 如 `N-Keying`→N 键位 |
| receptacle / plug | 插座／插头 | 直译 | — |
| shell size | 壳体号 | 直译 | — |
| lane | 通道 | 直译 | VITA 语境（链路数）；型号码内原样不译 |
| plane | 平面 | 直译 | `control plane`→控制平面、`data plane`→数据平面、`expansion plane`→扩展平面、`utility plane`→辅助平面 |
| radial clock | 径向时钟 | 直译 | — |
| reference clock | 参考时钟 | 直译 | — |
| conduction cooled | 传导散热式 | 直译 | `Conduction Cooled SOSA Plug-In Cards`→传导散热式 SOSA 插卡 |
| convection | 对流 | 直译 | — |
| cooling method | 散热方式 | 直译 | 表 19 |
| ground | 地 | 直译 | `chassis ground`→机壳地、`safety ground`→安全地、`DC RTN`→直流回线（**表内原样**） |
| fiber optic | 光纤 | 直译 | — |
| 3U / 6U | 3U／6U | 存原词 | 板卡高度规格，不译，不加空格 |

---

## 四、模块名（原书表 2，SvcV-1）

**六个分组**

| 英文 | 中文 | 档 |
|---|---|---|
| SOSA Sensor Management | 传感器管理 | 直译 |
| Transmission/Reception | 发射／接收 | 直译 |
| Process Signals/Targets | 信号／目标处理 | 直译 |
| Analyze/Exploit | 分析／情报利用 | 自拟 |
| Convey | 传递 | 直译 |
| Support System Operation | 支持系统运行 | 直译 |

**三十个模块**（编号原样）

| 英文 | 中文 | 档 |
|---|---|---|
| 1.1 System Manager | 系统管理器 | 直译 |
| 1.2 Task Manager | 任务管理器 | 直译 |
| 2.1 Receive Aperture/Transducer/Camera | 接收孔径／换能器／相机 | 直译 |
| 2.2 Transmit Aperture/Transducer/Laser | 发射孔径／换能器／激光器 | 直译 |
| 2.3 Conditioner-Receiver-Exciter | 调理器-接收机-激励器 | 直译 |
| 3.1 Signal/Object Detector and Extractor | 信号／目标检测与提取器 | 直译 |
| 3.2 Signal/Object Characterizer | 信号／目标特征化器 | 直译 |
| 3.3 Image Pre-processor | 图像预处理器 | 直译 |
| 3.4 Tracker | 跟踪器 | 直译 |
| 4.1 External Data Ingestor | 外部数据摄取器 | 直译 |
| 4.2 Encoded Data Extractor | 编码数据提取器 | 直译 |
| 4.3 Situation Assessor | 态势评估器 | 直译 |
| 4.4 Impact Assessor and Responder | 影响评估与响应器 | 直译 |
| 4.6 Storage/Retrieval Manager | 存储／检索管理器 | 直译 |
| 5.1 Reporting Services | 报告服务 | 直译 |
| 6.1 Security Services | 安全服务 | 直译 |
| 6.2 Encryptor/Decryptor | 加解密器 | 自拟 |
| 6.3 Guard/Cross-Domain Service | 护卫／跨域服务 | 自拟 |
| 6.4 Network Subsystem | 网络子系统 | 直译 |
| 6.5 Calibration Service | 校准服务 | 直译 |
| 6.6 Nav Data Service | 导航数据服务 | 直译 |
| 6.7 Time & Frequency Service | 时间与频率服务 | 直译 |
| 6.8 Compressor/Decompressor | 压缩／解压器 | 直译 |
| 6.9 Host Platform Interface | 宿主平台接口 | 直译 |
| 6.10 Power | 电源 | 直译 |

> **原书两处自身不一致，一律照录并照译**：编号自 4.4 跳到 4.6（无 4.5）；3.1 的条目名在同一份文件里既作 `Signal/Object Detector and Extractor` 也作 `Signal/Target Detector and Extractor`，两处各照本处字面译（前者"信号／目标检测与提取器"，后者"信号／目标检测与提取器"）。

---

## 五、交互、系统管理与运行

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| system management | 系统管理 | 直译 | — |
| task | 任务 | 直译 | AV-2：自传感器系统**外部**发来的请求 |
| assignment | 分派 | 直译 | AV-2：自传感器系统**内部**发出的请求；与 task 分开 |
| tasking | 任务指派 | 自拟 | 宿主平台向传感器下达的任务流，与单条 `task` 分开 |
| notification | 通知 | 直译 | — |
| publication / subscribe | 发布／订阅 | 直译 | `Publish-Subscribe`→发布-订阅 |
| request / response | 请求／响应 | 直译 | — |
| endpoint | 端点 | 直译 | 表 42 `Interaction Endpoints`→交互端点 |
| heartbeat | 心跳 | 直译 | — |
| discovery | 发现 | 直译 | — |
| configuration | 配置 | 直译 | 与 `mode`／`state` 分开 |
| mode | 模式 | 直译 | AV-2：离散且已知预期行为的工作方式 |
| state | 状态 | 直译 | AV-2：运行生存周期中的顶层状况之一 |
| status | 状况 | 直译 | AV-2：性能或健康的描述；与 `state` 分译，防混 |
| health | 健康 | 直译 | `health management`→健康管理、`health report`→健康报告 |
| fault | 故障 | 直译 | — |
| warning | 告警 | 直译 | — |
| logging | 日志记录 | 直译 | — |
| reset | 复位 | 直译 | — |
| BIT (Built-In Test) | 机内自检 | 直译 | 缩写原样 |
| calibration | 校准 | 直译 | — |
| cueing | 引导 | 直译 | `cross-sensor cueing`→跨传感器引导 |
| track / track report | 航迹／航迹报告 | 直译 | — |
| detection | 检测 | 直译 | AV-2 定义条目；不译"探测"（`detector` 仍译"检测器"，保持同源） |
| target | 目标 | 直译 | — |
| clutter | 杂波 | 直译 | — |
| interference | 干扰 | 直译 | — |
| waveform | 波形 | 直译 | — |
| channelization | 信道化 | 自拟 | — |
| data cube | 数据立方 | 直译 | — |
| metadata | 元数据 | 直译 | — |
| data products | 数据产品 | 直译 | AV-2 定义条目 |
| information products | 信息产品 | 直译 | AV-2 定义条目 |
| streaming data | 流数据 | 直译 | — |
| Quality of Service (QoS) | 服务质量 | 直译 | 缩写原样 |
| interoperability level | 互操作等级 | 直译 | 原书 §5.4.3.2 |
| virtual machine | 虚拟机 | 直译 | — |

---

## 六、质量属性（原书表 1，按优先级降序）

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| Interoperability | 互操作性 | 直译 | — |
| Securability | 可安全性 | 自拟 | **本文件自拟，非定译**；指系统设计上大体不可被攻破、不可被未授权访问的程度。不译"安全性"（那是 `security`），也不译"安保性" |
| Modularity | 模块化 | 直译 | 属性义；`modular design`→模块化设计 |
| Compatibility | 兼容性 | 直译 | — |
| Portability | 可移植性 | 直译 | — |
| Plug-and-playability | 即插即用性 | 直译 | 不译"插拔性" |
| Upgradeability | 可升级性 | 直译 | — |
| Scalability: Sensor Multiplicity | 可扩展性：传感器数量 | 直译 | 冒号原样 |
| Scalability: Platform Size | 可扩展性：平台规模 | 直译 | — |
| Resiliency | 韧性 | 直译 | — |

---

## 七、DoDAF 制品号（原样保留）

| 英文 | 中文括注（仅首次） | 处理 |
|---|---|---|
| CV-1 / CV-2 | 能力视图-1／-2 | 号原样；首次括注后只写号 |
| SV-1 / SV-2 / SV-3 | 系统视图-1／-2／-3 | 同上 |
| SvcV-1 / SvcV-2 / SvcV-3b / SvcV-4 | 服务视图-1／-2／-3b／-4 | 同上 |
| OV-1 / OV-2 / OV-5b | 运行视图-1／-2／-5b | 同上 |
| DIV-1 / DIV-2 / DIV-3 | 数据信息视图-1（概念数据模型）／-2（逻辑数据模型）／-3（物理数据模型） | 同上；模型名前一律存原词 + 中文括注 |

> **判据**：制品号是寻址用的，译了就与 DoDAF 文献对不上；中文括注只在各册首次出现处给一次。分册标题里的号（如 `3.1 CV-1/CV-2 Objectives`）按"英文 中文"同行并置，号不动。

---

## 八、外部体系、标准名与缩写（不译）

下列一律保留英文原名，不括注、不音译：`SOSA`、`MOSA`、`OSA`、`OOSA`、`C4ISR`、`DoD`、`VITA`、`ANSI/VITA 65.1`、`VPX`、`MORA`、`VICTORY`、`FACE`、`OMS`、`HOST`、`UCI`、`DoDAF`、`FACE`、`REI`、`RTE`、`DDS`、`MIL-STD-*`、`MIL-DTL-*`、`MIL-PRF-*`、`AS6129/69`、`ISO/IEC/IEEE 42010`、`SLT*`、`MOD*`、`MT9*`、`J1`~`J10`、`DC-1`~`DC-4`、`PWR_EN`、`MASTER_ARM`、`TX1+`、`RX1-`、`DA+`、`RS422`、`1000BaseT`、`28V DC@15A`、`1 PPS`、`10MHz`。

> **理由**：这些串是**寻址键**——引脚号、信号名、型号码、标准号。译一个，正文引用、与引脚图、与外部文献三处就对不上。分册 `15-acronyms-and-abbreviations.md` 的 107 条缩写照原样收，只把 "Expansion" 列作中英并置。

**英文类别名（正文可用中文，括注一次）**

| 英文 | 中文 | 说明 |
|---|---|---|
| Communications | 通信 | 五类传感器之一 |
| EO/IR | 光电／红外 | Electro-Optical/Infrared |
| EW | 电子战 | Electronic Warfare |
| Radar | 雷达 | — |
| SIGINT | 信号情报 | Signals Intelligence |
| SAR | 合成孔径雷达 | Synthetic Aperture Radar |
| AMTI | 空中动目标指示 | Air Moving Target Indicator |
| GMTI | 地面动目标指示 | Ground Moving Target Indicator |
| SAA | 感知与避让 | Sense and Avoid |
| SWaP | 尺寸、重量与功耗 | Size, Weight, and Power |
| PED | 处理、利用与分发 | Processing Exploitation and Dissemination |

---

## 九、判据与程序用语

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| conformance | 符合性 | 直译 | 依 42010／42020 既有口径 |
| compliance | 符合程度 | 直译 | **与 conformance 分开**：AV-2 明言 `conformance is the limiting case of 100% compliance`（符合性是符合程度达 100% 的极限情形），故 compliance 取"程度"义 |
| conformant / non-conformant | 符合的／不符合的 | 直译 | — |
| verification | 验证 | 直译 | — |
| certification | 认证 | 直译 | — |
| registration | 登记 | 直译 | — |
| registry | 登记簿 | 直译 | `SOSA Registry`→SOSA 登记簿 |
| conformance certificate | 符合性证书 | 直译 | — |
| Conformance Program | 符合性计划 | 自拟 | 原文为项目集义，不译"程序" |
| Product Standard | 产品标准 | 直译 | — |
| Conformance Guide | 符合性指南 | 直译 | — |
| Distribution Statement | 分发声明 | 直译 | 原书 `Distribution Statement A`→分发声明 A |
| Snapshot | 快照版 | 自拟 | 原书 `This is a Snapshot, not an approved standard`；译"快照版"以与正式版相区分 |
| open standard | 开放标准 | 直译 | — |
| open interface / closed interface | 开放接口／封闭接口 | 直译 | AV-2 定义条目 |
| Open Business Model | 开放业务模式 | 直译 | — |
| governance | 治理 | 直译 | — |
| stakeholder | 利益相关方 | 直译 | 依 42010 口径 |

---

## 十、尚待裁的四项（译名已定，档位待用户裁）

以下四项按 §十一 判据取了"直译"，与原 2026-11-14 商定的示例清单（把 `aperture`／`transducer`／`pod`／`conditioner-receiver-exciter` 列为"存原词"）不同——差别不在判据，在四个词其实**有稳定中文**。若用户仍要存原词，改本表两处并在正文替换即可。

| 词 | 本表取 | 商定清单取 | 取舍理由 |
|---|---|---|---|
| aperture | 孔径 | 存原词 | 雷达／光电的专业词，天线孔径、接收孔径都通行，模块名「接收孔径／换能器／相机」读得通 |
| transducer | 换能器 | 存原词 | 同上；与 conditioner、exciter 同属 MORA 信号链，四个词都能直译，混着存原词反而割裂 |
| pod | 吊舱 | 存原词 | 光电吊舱、传感器吊舱是国内通行说法 |
| conditioner-receiver-exciter | 调理器-接收机-激励器 | 存原词 | 同上；保留连字符原样 |

---

## 十一、机械关口径

1. **段数对齐**：英文段与中文段一一配对，逐册核数，比值须为 1:1。
2. **禁译串**：`SLT*`／`MOD*`／`J\d+`／`MIL-STD-*`／`MIL-PRF-*`／`MIL-DTL-*`／`AS\d+`／电压电流值／信号名／Excel 文件名／链接／图表编号／页锚，译前译后的**多重集完全一致**。
3. **术语一致性**：本表每一行的中文译法全册唯一；同词异译一律报出。
4. **规范动词计数**：`shall`／`should`／`may`／`must` 与"应／宜／可／必须"的计数比，与英文侧逐册核。
5. **脚本**：`00-对照核对.py`（本目录），`python 00-对照核对.py` 退出码 0 为过。

---

## 十二、维护纪律

- 本表是**唯一权威**：正文与本表冲突，改正文。
- 新增译名先入本表再入正文；**自拟档必须在表内写明"非定译"**。
- 英文原书自身的不一致（`Ariel`／`Slots 2 uses`／`Contol Plane`／`AS39029/56` 缺 II 等，见 `../99-转换说明与已知差异.md`）照字面译，**不许顺手改对**；这类地方的中文照英文的字面走，不替原文纠错。
