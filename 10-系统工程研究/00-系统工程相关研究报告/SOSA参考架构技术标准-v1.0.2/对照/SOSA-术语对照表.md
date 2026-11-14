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

> **注**：本件 `shall`／`should`／`may`／`must` 的用法与原书 §1.5.2 的定义一致。**英文侧实测**（16 册源件，按词界计数）：`shall` 210、`should` 54、`may` 121、`must` 12；**对照册中文侧**（合订本）：应（剔「不应／相应／对应」后）320、宜 57、必须 14。两边不是一一相等——英文一句 `shall` 里中文可能出两个「应」，表内 `may`／「可」又大量出现在非规范语境，故只作量级核对，不作逐词配平。

---

## 二、架构与描述

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| architecture | 架构 | 直译 | 本项目既定口径 |
| reference architecture | 参考架构 | 直译 | 本件标题即 `SOSA Reference Architecture`→SOSA 参考架构 |
| architecture description | 架构描述 | 直译 | 依 GB/T 45630-2025 与 24 号报告附录 A |
| requirement（名词） | **需求** | 直译 | **不译「要求」**（用户 2026-11-14 定）：凡英文为 requirement(s) 的，一律「需求」；`系统需求`／`系统管理需求`／`符合性需求`／`机械需求` 等均从之 |
| require / required / requires（动词、分词） | 要求／所要求的 | 直译 | 与上条的「需求」分开：`不要求`／`只要求`／`所要求的程度`／`要求上述各领域…` 保留「要求」 |
| architecture principle | 架构原则 | 直译 | 原书 §3.2 分面向业务的（Business-Oriented）与面向技术的（Technically-Oriented）两组——**不取「业务向／技术向」**，一律「面向…的」 |
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

**二十五个模块**（编号原样；另有六个分组行 `SOSA Sensor Management`／`Transmission/Reception`／`Process Signals/Targets`／`Analyze/Exploit`／`Convey`／`Support System Operation`，见上表）

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
4. **规范动词**：逐段核——含 `shall`／`should`／`must` 的英文段，其配对中文段须出现「应／宜／必须」。**惯用的 `It should be noted that…`／`Should any viewer…` 不算规范动词**，脚本比对前先抹掉；`may`／「可」不作强制核对（「可」在非规范语境里过密，硬核全是假阳性）。另设**段内句数比**提示：英文 ≥4 句而中文句数不到其一半的段，报 WARN 供人查删译。
5. **脚本**：`00-对照核对.py`（本目录），`python 00-对照核对.py` 退出码 0 为过。

---

## 十二、维护纪律

- 本表是**唯一权威**：正文与本表冲突，改正文。
- 新增译名先入本表再入正文；**自拟档必须在表内写明"非定译"**。
- 英文原书自身的不一致（`Ariel`／`Slots 2 uses`／`Contol Plane`／`AS39029/56` 缺 II 等，见 `../99-转换说明与已知差异.md`）照字面译，**不许顺手改对**；这类地方的中文照英文的字面走，不替原文纠错。

---

## 十三、随译回填的领域词（2026-11-14 译 03／04 时定）

译 03／04 两册时出现的词，术语表前十二节未收，按判据就地定下并回填于此。**档位照旧三档**。

### 13.1 物项与语境

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| SOSA host | SOSA 宿主 | 直译 | 承 `host platform`＝宿主平台 |
| Nominal Case / special case | 标称情形／特例 | 直译 | §3.4 图 4／图 5 两情形 |
| Physical Context Entities | 物理语境实体 | 直译 | §3.5 节题 |
| actor | 参与者 | 直译 | — |
| hardware enclosure | 硬件壳体 | 直译 | `enclosure`＝壳体；`chassis` 仍作"机箱" |
| packaged antenna array / packaged imaging array | 封装天线阵／封装成像阵 | 直译 | — |
| hardware assembly | 硬件装配体 | 自拟 | 避免与 `software component` 软件组件相撞 |
| box-level | 整机级 | 自拟 | §4.5 节题；首次括注 `box-level` |
| multi-INT | 多情报 | 存原词 | 正文存 `multi-INT` |
| over-capacity (system saturation) | 超容量（系统饱和） | 直译 | — |
| Field Replaceable Unit (FRU) | 现场可更换单元 | 直译 | 缩写原样 |
| 2 Level Maintenance (2LM) | 二级维修 | 直译 | 缩写原样 |
| form factor | 形状因数 | 直译 | — |
| power cycle | 电源循环 | 直译 | — |
| sanitize | 净化 | 直译 | 数据清除义 |
| lights out | "熄灯"状态 | 自拟 | 无人值守义；首次括注 `lights out` |

### 13.2 交互与数据

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| transport | 传输 | 直译 | — |
| interconnect | 互连 | 直译 | — |
| SOSA Wideband (Low Latency) Interconnect | 宽带（低延迟）互连 | 存原词 | 体系名，首次括注后存原词 |
| SOSA Message Interconnect | 消息互连 | 直译 | — |
| topic | 主题 | 直译 | 发布／订阅语境 |
| middleware | 中间件 | 直译 | — |
| many-to-many | 多对多 | 直译 | — |
| point-to-point / point-to-multi-point | 点到点／点到多点 | 直译 | — |
| blunt end | 钝端 | 直译 | — |
| publisher / subscriber | 发布方／订阅方 | 直译 | 与 `Publish-Subscribe` 发布-订阅 同源 |
| requestor / responder | 请求方／响应方 | 直译 | — |
| writer / reader | 写入方／读取方 | 直译 | — |
| controller / subordinate | 控制方／下属方 | 直译 | 系统管理主从关系 |
| receiver（端点角色义） | 接收方 | 直译 | **与 §三 的"接收机"分义**：硬件语境作接收机，交互角色语境作接收方 |
| deterministic | 确定性 | 直译 | — |
| structured data | 结构化数据 | 直译 | — |
| Needline | 需求线 | 存原词 | DoDAF 术语，首次括注后存原词 |
| interaction group | 交互组 | 直译 | — |
| Service endpoint / client endpoint | 服务端点／客户端点 | 直译 | — |
| unique identity | 唯一标识 | 直译 | — |
| configuration description | 配置描述 | 直译 | — |
| out-of-band | 带外 | 直译 | — |
| network-based | 基于网络的 | 直译 | — |

### 13.3 管理与判据

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| prescriptive | 规定性 | 直译 | 与 `descriptive` 描述性 相对 |
| Management Domain / Payload Domain | 管理域／载荷域 | 直译 | — |
| Management Information Base (MIB) | 管理信息库 | 直译 | 缩写原样 |
| Intelligent Platform Management Bus | 智能平台管理总线 | 直译 | 缩写 `IPMB` 原样 |
| Access Control Services | 访问控制服务 | 直译 | — |
| Authorization Provider / Health Provider | 授权提供者／健康提供者 | 直译 | — |
| Reliability, Availability, and Serviceability (RAS) | 可靠性、可用性与可服务性 | 直译 | 缩写原样 |
| Service-Oriented Architecture | 面向服务的架构 | 直译 | 缩写 `SOA` 原样 |
| Motion Imagery Standards Board | 运动图像标准委员会 | 直译 | 缩写 `MISB` 原样 |
| **safety** | **安全** | 直译 | 与 `safety-critical` 安全关键、`safety ground` 安全地 同源 |
| **security** | **信息安全** | 直译 | 与 `safety` 分开，防两词都译"安全"；`system safety and security requirements`＝系统安全与信息安全要求 |

> **待裁一处**：`safety` 亦可取「功能安全」（与 GB/T 体系对接时更准），`security` 亦可取「安全防护」。现取「安全／信息安全」是照本册自身语境的直读。

### 13.4 新定术语的记法

以上各条凡标「自拟」者，仍照 §二 的规矩：**非定译**，日后不得当权威译法引用。前十二节的表未动，新增只落在本节——回填时按主题归到本节，不散写进前面各节，便于日后整体复核。

### 13.5 架构原则三要素与一般用语（译 §3.1／§3.2 时定）

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| Statement / Rationale / Implications | 陈述／理由／影响 | 直译 | 原书每条架构原则的三段式；仿 TOGAF 中译口径 |
| patterns | 模式 | 直译 | 设计模式义；首次括注 `patterns` |
| software shim | 软件垫层 | 自拟 | 夹在两方之间的适配层；不译"垫片" |
| lock out | 锁定排除 | 直译 | 把某做法排除在外 |
| IP (Intellectual Property) | 知识产权 | 直译 | 与 `data rights` 数据权利 分开 |
| UAS | 无人机系统 | 直译 | 缩写原样；与 `UAV` 无人机 并列时各译各的 |
| Section N.N / Appendix X | 第 N.N 节／附录 X | 直译 | 交叉引用一律这样写，编号原样 |

### 13.6 安全与信号处理（译 §3.7／§3.9 时定）

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| security enclave | 安全飞地 | 直译 | `enclave`＝飞地 |
| ICD (Interface Control Document) | 接口控制文件 | 直译 | 缩写原样 |
| Anti-Tamper (AT) | 反篡改 | 直译 | 缩写原样 |
| TIG (Technical Implementation Guide) | 技术实施指南 | 直译 | — |
| RMF (Risk Management Framework) | 风险管理框架 | 直译 | 缩写原样 |
| Cyber Survivability Endorsement Implementation Guide | 《网络生存性背书实施指南》 | 直译 | 文件名译出，原串不动 |
| O-TTPS | 开放可信技术提供方™ 标准 | 直译 | 标准名，缩写原样 |
| human language processing | 人类语言处理 | 直译 | 不译"自然语言处理"，防与 NLP 混同 |
| image chip | 图像切片 | 自拟 | 目标图像的小块；首次括注原词 |
| constant false alarm rate | 恒虚警率 | 直译 | — |
| STAP (Space-Time Adaptive Processing) | 空时自适应处理 | 直译 | 缩写原样 |
| root of security | 安全根 | 直译 | — |
| zeroize | 清零 | 直译 | 敏感数据清零义 |
| degraded | 劣化 | 直译 | `degraded network element`＝劣化网络元素 |
| intrusion detection | 入侵检测 | 直译 | — |
| security breach | 安全破入 | 自拟 | 与 `breach` 破入 同源；不用"泄露"（`leakage` 另有其词） |
| data-at-rest / data-in-transit | 静态数据／传输中数据 | 直译 | — |
| artifact | 制品 | 直译 | DoDAF 语境；与 §七 的"制品号"同源 |

### 13.7 AV-2 词典用词（译表 47 时定；66 条已逐条译入该表，此处摘易混与高复用者）

| 英文 | 中文 | 档 | 说明 |
|---|---|---|---|
| Cohesion / Coupling | 内聚／耦合 | 直译 | 软件度量义 |
| Reuse | 复用 | 直译 | 不译"重用" |
| Open Source | 开源 | 直译 | 与 `open standard` 开放标准 分开 |
| Real-time / Reconfigure / Portable / Scalable | 实时／重配置／可移植／可扩展 | 直译 | — |
| Subsystem / System | 子系统／系统 | 直译 | `system-of-systems`＝系统之系统（首次括注原词） |
| Standardized Interfaces | 标准化接口 | 直译 | AV-2 定义条目 |
| Open Architecture / Open Interface / Open Systems Architecture | 开放架构／开放接口／开放系统架构 | 直译 | — |
| Published Architecture (or Standard) | 已发布架构（或标准） | 直译 | 括注原样 |
| Security Risk | 信息安全风险 | 直译 | 承 §13.3 的 `security`＝信息安全 |
| SOSA enterprise | SOSA 企业 | 直译 | AV-2 的 `the SOSA enterprise` 指整个 SOSA 事业体；`SOSA Consortium` 仍作 SOSA 联盟 |
| **Secure** | **安全防护** | **自拟** | AV-2 的属性条目。**取"安全防护"是为了三分不撞车**：`safety` 安全、`security` 信息安全、`secure`（属性）安全防护。若改"安全的"，会与 safety 混同 |
