# 前置：封面·目录·图表清单·序 ｜ Front Matter: Cover, Contents, Lists of Tables and Figures, Preface

> 原书 p.i–xx ｜ PDF p.1–20

> **译注**：原书把 Figure 46 印了两次（p.146、p.179），转换时把后者及之后顺移为 47~50；故**图清单里的 Figure 46 起与正文图题差一号**（见 `../99-转换说明与已知差异.md`）。

The Open Group Snapshot

The Open Group 快照版

Technical Standard for SOSA™ Reference Architecture,

《SOSA™ 参考架构技术标准》

Edition 1.0, Version 2

第 1.0 版，第 2 次修订

- You have a choice: you can either create your own future, or you can become the victim of a future that someone else creates for you. By seizing the transformation opportunities, you are seizing the opportunity to create your own future.

- 你有一个选择：要么自己创造未来，要么成为别人所造未来的受害者。抓住转型的机会，你就抓住了创造自己未来的机会。

Vice Admiral (ret.) Arthur K. Cebrowski

阿瑟·K·塞布罗夫斯基（Arthur K. Cebrowski），退役中将

NOTICE

声明

Snapshots are draft documents, which provide a mechanism for The Open Group to disseminate information on its current direction and thinking to an interested audience, in advance of formal publication, with a view to soliciting feedback and comment. A Snapshot represents the interim results of a technical activity. Although at the time of publication The Open Group intends to progress the activity towards publication of a Preliminary Standard or Open Group Standard, The Open Group is a consensus organization, and makes no commitment regarding publication. Similarly, a Snapshot does not represent any commitment by any member of The Open Group to make any specific products available. This Snapshot is intended to make public the direction, thinking and path the SOSA Consortium is taking in the development of the SOSA Reference Architecture. We invite your feedback and guidance. To provide feedback on this Snapshot, please send comments by email to ogsosa-admin@opengroup.us no later than December 31, 2019. This Snapshot document is valid through December 31, 2019 only. For information on joining The Open Group SOSA™ Consortium, please send email to ogsosa-admin@opengroup.us or visit our website at www.opengroup.org/sosa.

快照版是草案文件，为 The Open Group 提供一种机制：在正式出版之前，先向有兴趣的读者传播其当前的方向与思考，以求征集反馈与意见。快照版代表一项技术活动的阶段性成果：尽管在出版之时 The Open Group 有意推动该活动走向发布初步标准或 The Open Group 标准，但 The Open Group 是一个以共识为基础的组织，对是否出版不作任何承诺；同样，快照版不代表 The Open Group 任何成员承诺提供任何具体产品。本快照版意在公开 SOSA 联盟开发 SOSA 参考架构所取的方向、思路与路径。我们欢迎您的意见与指导。如对本快照版提出意见，请于 2019 年 12 月 31 日前发邮件至 ogsosa-admin@opengroup.us。本快照版文件仅在 2019 年 12 月 31 日之前有效。有关加入 The Open Group SOSA™ 联盟的信息，请发邮件至 ogsosa-admin@opengroup.us，或访问网站 www.opengroup.org/sosa。

Case: 88ABW-2019-0039; Cleared: 2019-01-07

案号：88ABW-2019-0039；已审查放行：2019-01-07

<!-- 原书 p.i ｜ PDF p.1 -->

Copyright © 2019, The Open Group LLC for the benefit of the SOSA Consortium Members. All rights reserved. The Open Group hereby authorizes you to use this document for any purpose, PROVIDED THAT any copy of this document, or any part thereof, which you make shall retain all copyright and other proprietary notices contained herein. This document may contain other proprietary notices and copyright information. Nothing contained herein shall be construed as conferring by implication, estoppel, or otherwise any license or right under any patent or trademark of The Open Group or any third party. Except as expressly provided above, nothing contained herein shall be construed as conferring any license or right under any copyright of The Open Group. Note that any product, process, or technology in this document may be the subject of other intellectual property rights reserved by The Open Group, and may not be licensed hereunder. This document is provided "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT. Some jurisdictions do not allow the exclusion of implied warranties, so the above exclusion may not apply to you. Any publication of The Open Group may include technical inaccuracies or typographical errors. Changes may be periodically made to these publications; these changes will be incorporated in new editions of these publications. The Open Group may make improvements and/or changes in the products and/or the programs described in these publications at any time without notice. Should any viewer of this document respond with information including feedback data, such as questions, comments, suggestions, or the like regarding the content of this document, such information shall be deemed to be non-confidential and The Open Group shall have no obligation of any kind with respect to such information and shall be free to reproduce, use, disclose, and distribute the information to others without limitation. Further, The Open Group shall be free to use any ideas, concepts, know-how, or techniques contained in such information for any purpose whatsoever including but not limited to developing, manufacturing, and marketing products incorporating such information. If you did not obtain this copy through The Open Group, it may not be the latest version. For your convenience, the latest version of this publication may be downloaded at www.opengroup.org/library.

版权所有 © 2019，The Open Group LLC，为 SOSA 联盟成员之利益持有。保留一切权利。The Open Group 特此授权您为任何目的使用本文件，**但以**您制作的任何副本或其任何部分**应**保留本文所载一切著作权与其他所有权声明**为条件**。本文件可能载有其他所有权声明与著作权信息。本文任何内容均**不应**解释为以默示、禁止反言或其他方式授予 The Open Group 或任何第三方任何专利或商标项下的许可或权利；除上文明确许可者外，本文任何内容也**不应**解释为授予 The Open Group 任何著作权项下的许可或权利。请注意：本文件所述任何产品、工艺或技术，可能是 The Open Group 保留的其他知识产权的标的，且不得依本文件获得许可。本文件按**"现状"（"AS IS"）提供，不附带任何明示或默示的保证**，包括但不限于对适销性、特定用途适用性或不侵权的默示保证。某些司法辖区不允许排除默示保证，故上述排除可能不适用于您。The Open Group 的任何出版物均可能含有技术性不准确或排印错误。这些出版物可能被定期修改，修改将并入其新版。The Open Group 可随时改进和／或变更这些出版物所述的产品和／或程序，恕不另行通知。若本文件的任何阅读者回以信息（含反馈数据，如对本文件内容的提问、意见、建议等），该等信息**应**视为非保密；The Open Group 对此类信息不负任何义务，并**应**可自由复制、使用、披露与分发之，不受限制。此外，The Open Group **应**可自由使用此类信息中所含的任何想法、概念、诀窍或技术，用于任何目的，包括但不限于开发、制造与营销采用此类信息的产品。若您并非通过 The Open Group 获得本副本，则它可能不是最新版本；为方便起见，本出版物的最新版本可在 www.opengroup.org/library 下载。

The Open Group Snapshot Technical Standard for SOSA™ Reference Architecture, Edition 1.0, Version 2 Document Number: S180

《The Open Group 快照版技术标准：SOSA™ 参考架构，第 1.0 版，第 2 次修订》，文件编号：S180。

Authored by The Open Group SOSA™ Consortium. Published by The Open Group, January 2019. Comments relating to the material contained in this document may be submitted to: The Open Group, 800 District Avenue, Suite 150, Burlington, MA 01803, United States or by electronic mail to: ogsosa-admin@opengroup.us

由 The Open Group SOSA™ 联盟撰写，The Open Group 于 2019 年 1 月出版。有关本文件所载内容的意见，可寄至：The Open Group, 800 District Avenue, Suite 150, Burlington, MA 01803, United States，或发电子邮件至：ogsosa-admin@opengroup.us。

<!-- 原书 p.ii ｜ PDF p.2 -->

## Contents ｜ 目录

<!-- 未译 印刷式目录、图清单与表清单（版面构件） -->

1 Introduction 1

1.1 Objective 1

1.2 Overview 2

1.2.1 SOSA Architecture Fundamentals 2

1.2.2 Business Alignment 4

1.3 Conformance 4

1.4 Normative References 5

1.5 Terminology 5

1.5.1 SOSA Architecture 5

1.5.2 System Requirements 5

1.5.3 Hardware Specification Keywords 6

1.6 Future Directions 7

2 Definitions 8 3 Reference Architecture Description 9

3.1 CV-1/CV-2 Objectives 9

3.1.1 SOSA Capability View – 1 (CV-1) 9

3.2 SOSA Architecture Principles 10

3.2.1 Business-Oriented Architecture Principles 11

3.2.2 Technically-Oriented Architecture Principles 12

3.3 SOSA Quality Attributes 17

3.4 SV-1 (System Interface Description/Context) 19

3.5 SOSA Physical Context Entities 21

3.5.1 SOSA Sensor 21

3.5.2 SOSA Hardware Element 21

3.5.3 SOSA Host Platform 22

3.5.4 SOSA Sensor Pod 22

3.6 Function to Module Aggregation Criteria 22

3.7 Security Concepts and Approach 23

3.7.1 SOSA Hardware Security Framework 23

3.8 Hardware Concepts and Approach 24

3.9 SvcV-1: Services Context Description 24

3.10 SOSA Inter-Module Interactions 29

3.10.1 SOSA Sensor Interconnections 30

3.10.2 SOSA Module Interaction Types 30

3.11 System Management Concepts and Approach 35

3.11.1 System Management Concepts 36

3.11.2 Network-Based System Management 37

3.11.3 SOSA Hardware Management Overview 39

4 Architecture Definition 43

4.1 Service Views 43

4.1.1 SvcV-4: Services Functionality Description 43

4.1.2 SvcV-2: Services Resource Flow Description 66

<!-- 原书 p.iii ｜ PDF p.3 -->

4.1.3 SvcV-3b: Services-Services Matrix 66

4.2 Data Architecture 66

4.2.1 DIV-1: Conceptual Data Model 67

4.2.2 DIV-2: Logical Data Model 69

4.2.3 DIV-3: Physical Data Model 70

4.3 Service Architecture 70

4.3.1 SvcV-6: Services Resources Flow Matrix 70

4.4 System Architecture 70

4.4.1 SV-2: Systems Resource Flow Description 70

4.4.2 SV-3: Systems-Systems Matrix 70

4.5 Box-Level Hardware 70

5 SOSA Technical Standard 72

5.1 Host Vehicle/SOSA Sensor Interface 72

5.1.1 Sensor Physical Packages 72

5.1.2 Mechanical Interfaces 72

5.2 SOSA Sensor Physical Interfaces 73

5.2.1 Electrical Connector Characteristics 73

5.2.2 J1-DC Power Connector 73

5.2.3 J2-Signals Connector 75

5.2.4 J3-Video (Copper) Connector 84

5.2.5 J4-Fiber Optics Connector 86

5.2.6 J5-GPS Antenna Connector 88

5.2.7 J6-DC Auxiliary Power Connector 88

5.2.8 J7-High Speed Connector 90

5.2.9 J8-High Density RF Connector 90

5.2.10 J9-Low Loss RF Connector 92

5.2.11 Auxiliary RF Connectors 93

5.2.12 J10-AC Power Connector 94

5.2.13 Hardware Platform 3U and 6U Slot Profile

Specifications 95 5.2.14 Hardware Platform SOSA Plug-In Card Profiles 101

5.2.15 Common 6U and 3U Plug-In Card Profile

Specifications 102

5.2.16 SOSA 3U Plug-IN Card Profile Specifications 102

5.2.17 6U Plug-In Card Profile Specifications 114

5.2.18 SOSA 6U Legacy Switch Plug-In Card Profile 119

5.2.19 SOSA 6U External I/O Plug-In Card Profile 120

5.2.20 Power Supply Module 122

5.2.21 Mezzanine Modules 123

5.2.22 Maintenance Console Port Requirements 124

5.3 SOSA System Management Requirements 126

5.3.1 SOSA Hardware Element System Management

Requirements 126

5.3.2 SOSA Module System Management Requirements 128

5.4 SOSA Software Operating Environment 128

5.4.1 Description 128

5.4.2 Scope 129

5.4.3 Recommendations 131

5.4.4 Safety 132

5.5 SOSA Module Interactions 133

<!-- 原书 p.iv ｜ PDF p.4 -->

5.6 Sensor Management 133

5.6.1 System Manager Module 134

5.6.2 Task Manager Module 140

5.7 RF Signal Layer Modules 144

5.7.1 Modular Open RF Architecture 145

5.7.2 Application of MORA to SOSA Signal Layer Modules 146

5.7.3 RF Receiver Aperture/Transducer Module 146

5.7.4 RF Transmit Aperture/Transducer Module 147

5.7.5 RF Conditioner-Receiver-Exciter Module 148

5.7.6 RF Signal Layer Module Interactions 149

5.7.7 RF Signal Layer Module Rules 155

5.8 EO/IR Signal Layer Modules 159

5.8.1 EO/IR Receiver Camera Module Standard 159

5.8.2 EO/IR Transmit Laser Module Standard 159

5.8.3 EO/IR Conditioner-Receiver-Exciter Module Standard 159

5.9 RF Digital Processing Modules 159

5.9.1 Tracker 159

5.10 Infrastructure Modules 162

5.10.2 External Data Ingestor 163

5.10.3 Host Platform Interface 163

5.11 OSA Architecture Development/Evolution Plan 172

A StdV-1 (Applicable Standards) 173 B AV-2 Integrated Dictionary 174 C Use-Case Details 179

C.1 OV-1 (High Level Operational Concept) 179

C.2 OV-2 (Operational Resource Flow) 179

C.3 OV-5b (Operational Activity Model) 179

D DIV-2 and Data Dictionary 180

D.1 SOSA Sensor RF Control (Distribution A) 180

D.2 MORA Signal Layer 180

D.3 AMTI SAA Multi-Sensor Fusion Tracker 180

D.4 Common System Management Data Elements 180

E DIV-3 (Physical Data Model) 182

E.1 SOSA Sensor RF Control (Distribution A) 182

E.2 RF Signal Layer 182

F Host Vehicle/Sensor Connector Details 183 G Slot Profiles 184 H Module-by-Module Details 185 I SOSA Backplane Examples 186

I.1 3U Medium-Sized Backplane Example 186

I.2 3U Large-Sized Backplane Example 187

I.3 3U/6U Hybrid Backplane Example 188

<!-- 原书 p.v ｜ PDF p.5 -->

Table of Figures

Figure 1: The Facets that Comprise a SOSA Module 3

Figure 2: The Architecture Development Method Adopted for the SOSA Technical Standard 3

Figure 3: SOSA CV-1 10

Figure 4: SV-1 for Nominal Case 20

Figure 5: SV-1 for Sensor Pod Special Case 21

Figure 6: SvcV-1: Top-Level SOSA Services Context Description 25

Figure 7: SOSA Sensor Interconnections 30

Figure 8: SOSA Network-Based System Management Architecture 38

Figure 9: SOSA Hardware System Management Logical Block Diagram 40

Figure 10: Example SOSA System Management Backplane/Chassis Implementation 41

Figure 11: Example SOSA System Management Plug-In Card Implementation 42

Figure 12: DIV-1 for Mission Entities 68

Figure 13: DIV-1 for Management Entities 69

Figure 14: SOSA Hardware Building Blocks 71

Figure 15: J1 Power Connector Pin Arrangement 74

Figure 16: J2 Signal Connector Pin Arrangement 75

Figure 17. Input Time Rollover Pulse (1 PPS) Signal Characteristics 83

Figure 18: J3 Video Connector Pin Arrangement 85

Figure 19: J4 Fiber Optic Connector Pin Arrangement 87

Figure 20. J6 Auxiliary Power Connector Pin Arrangement 89

Figure 21: J8 RF Connector Pin Arrangement 91

Figure 22: J9 RF Connector Pin Arrangement 92

Figure 23: J10 AC Power Connector Pin Arrangement 94

Figure 24: ANSI/VITA 65.0 3U I/O Intensive SBC Slot Profile

SLT3-PAY-1F1F2U1TU1T1U1T-14.2.16 103

Figure 25: ANSI/VITA 65.0 Payload Slot Profile for SLT3-PAY-2F2U-14.2.3 105

Figure 26: ANSI/VITA 65.0 Payload Slot Profile

SLT3-PAY-1F1U1S1S1U1U2F1H-14.6.11-n 106

Figure 27: ANSI/VITA 65.0 Payload Slot Profile

SLT3-PAY-1F1U1S1S1U1U4F1J-14.6.13-n 107

Figure 28: ANSI/VITA 65.0 Control/Expansion Plane Switch Slot Profile

SLT3-SWH-6F8U-14.4.15 108

Figure 29: ANSI/VITA 65.0 Control/Data Plane Switch Slot Profile

SLT3-SWH-6F1U7U-14.4.14 109

Figure 30: ANSI/VITA 65.0 Control/Data Plane Switch Slot Profile

SLT3-SWH-4F1U7U1J-14.8.7-n 110

Figure 31: ANSI/VITA 65.0 3U RF Switch Slot Profile

SLT3-SWH-1F1S1S1U1U1K-14.8.8-n 111

Figure 32: ANSI/VITA 65.0 Radial Clock Slot Profile

SLT3x-TIM-2S1U22S1U2U1H-14.9.2-n 112

Figure 33: ANSI/VITA 65.0 3U External I/O Slot Profile

SLT3-PAY-2U2U-14.2.17 113

Figure 34: ANSI/VITA 65.0 6U Payload Slot Profile

SLT6-PAY-4F2Q1H4U1T1S1S1TU2U2T1H-10.6.4-n 115

<!-- 原书 p.vi ｜ PDF p.6 -->

Figure 35: ANSI/VITA 65.0 6U Payload Slot Profile

SLT6-PAY-4F1Q1H4U1T1S1S1TU2U2T1H-10.6.3-n 116

Figure 36: ANSI/VITA 65.0 6U Control/Data Switch Slot Profile

SLT6-SWH-14F16U1U15U1J-10.8.1-n 118

Figure 37: ANSI/VITA65.0 Switch Slot Profile for SLT6-SWH-16U20F-10.4.2 120

Figure 38: ANSI/VITA 65.0 6U External I/O Slot Profile SLT6-PAY-4U2U-10.2.8 121

Figure 39: FACE Software Operating Environment and Subset Proposed for the

SOSA REI (red dashed line) 131

Figure 40: Sensor Management Architecture View 134

Figure 41: System Manager Interactions 135

Figure 42. RF Signal Layer Module Interactions 146

Figure 43: RF Receiver Aperture/Transducer Interactions 147

Figure 44: RF Transmit Aperture/Transducer Interactions 148

Figure 45: RF Conditioner Receiver/Exciter Interactions 148

Figure 46: Host Platform Interface Module Interactions 164

Figure 46: High-Level SOSA Use-Case 179

Figure 47: 3U Medium-Sized Backplane Example 187

Figure 48: 3U Large-Sized Backplane Example 188

Figure 49: 3U/6U Hybrid Backplane Example 190

<!-- 原书 p.vii ｜ PDF p.7 -->

Table of Tables

Table 1: SOSA Quality Attributes (in order of decreasing precedence) 18

Table 2: SvcV-1: Module Descriptions 25

Table 3: Interaction Types 31

Table 4: Interaction Roles, Endpoints, and Symbols 32

Table 5: SOSA SvcV-4 43

Table 6: Turreted Sensor Classes 72

Table 7: Sensor Connectors 73

Table 8: J1 DC Power Connector Pin Allocation 74

Table 9: J2 Signals Connector Pin Allocation 76

Table 10: J3 Video Connector Pin Allocation 85

Table 11: J4 Fiber Optic Connector Pin Allocation 87

Table 12: J5 GPS Connector Pin Allocation 88

Table 13. J6 Auxiliary DC Power Connector 89

Table 14: J7 Pin Allocations 90

Table 15: J8 RF Pin Allocations 91

Table 16: J9 RF Pin Allocation 93

Table 17: Auxiliary RF Connections 93

Table 18: J10 AC Power Pin Allocations 94

Table 19. Hardware Module Cooling Methods 101

Table 20: Referenced ANSI/VITA 65.1 Module Profiles for

SLT3-PAY-1F1F2U1TU1T1U1T-14.2.16 104

Table 21: ANSI/VITA 65.1Slot Profiles for SLT3-PAY-1F1U1S1S1U1U2F1H-14.6.11-n 106

Table 22: ANSI/VITA 65.1 Module Profiles for SLT3-PAY-1F1U1S1S1U1U2F1H-14.6.11-n

Table 23: ANSI/VITA 65.1Slot Profiles for SLT3-PAY-1F1U1S1S1U1U4F1J-14.6.13-n 107

Table 24: ANSI/VITA 65.1 Module Profiles for SLT3-PAY-1F1U1S1S1U1U4F1J-14.6.13-n 107

Table 25: ANSI/VITA 65.1 Module Profiles for SLT3-SWH-6F8U-14.4.15 108

Table 26: ANSI/VITA 65.1 Module Profiles for SLT3-SWH-6F1U7U-14.4.14 109

Table 27: ANSI/VITA 65.1 Module Profiles for SLT3-SWH-4F1U7U1J-14.8.7-n 110

Table 28: ANSI/VITA 65.1 Module Profiles for SLT3-SWH-1F1S1S1U1U1K-14.8.8-n 111

Table 29: VITA 65.1 Slot Profiles for SLT3x-TIM-2S1U22S1U2U1H-14.9.2-n 112

Table 30: VITA 65.1 Module Profiles for SLT3x-TIM-2S1U22S1U2U1H-14.9.2-n 112

Table 31: ANSI/VITA 65.1 Module Profiles for SLT3-PAY-2U2U-14.2.17 113

Table 32: ANSI/VITA 65.1 Slot Profiles for

SLT6-PAY-4F2Q1H4U1T1S1S1TU2U2T1H-10.6.4-n 115

Table 33: ANSI/VITA 65.1 Module Profiles for SLT6-PAY-4F2Q1H4U1T1S1S1TU2U2T1H-10.6.4-n

Table 34: ANSI/VITA 65.1 Module Profiles for SLT6-PAY-4F1Q1H4U1T1S1S1TU2U2T1H-10.6.3-n

Table 35: ANSI/VITA 65.1 Slot Profiles for SLT6-SWH-14F16U1U15U1J-10.8.1-n 118

Table 36: ANSI/VITA 65.1 Module Profiles for SLT6-SWH-14F16U1U15U1J-10.8.1-n 118

Table 37: ANSI/VITA 65.1 Module Profiles for SLT6-PAY-4U2U-10.2.8 122

Table 38: Maintenance Console Port Signal Levels 126

Table 39: Common System Management Interactions 135

<!-- 原书 p.viii ｜ PDF p.8 -->

Table 40: Task Management Interactions Table 140

Table 41: RF Signal Layer Module Interactions Table 149

Table 42. RF Signal Layer Module Interaction Endpoints 156

Table 43: Tracker Module Interactions 160

Table 44: Additional Tracker Interactions 161

Table 45: AMTI SAA Mission Configuration Data 162

Table 46: Host Platform Interface Interactions 164

Table 47: AV-2 Integrated Dictionary (Master Glossary of SOSA Terminology) 174

<!-- /未译 印刷式目录、图清单与表清单 -->

<!-- 装置 中文目录（译者所加，按正文章题生成） -->

## 中文目录

- 前置：封面·目录·图表清单·序　…　i–xx
- 目录　…　ii
- 前言　…　ix
- 执行摘要　…　ix
- 背景　…　ix
- 做法　…　ix
- 本文件　…　xi
- 商标　…　xii
- 致谢　…　xiii
- 引用文件　…　xv
- 1 引言　…　1–7
- 1.1 目标　…　1
- 1.2 概述　…　1
- 1.2.1 架构基础　…　1
- 1.2.2 业务对齐　…　3
- 1.3 符合性　…　3
- 1.4 规范性引用文件　…　4
- 1.5 术语　…　4
- 1.5.1 架构　…　4
- 1.5.2 系统需求　…　4
- 1.5.3 硬件规格关键字　…　5
- 1.6 未来方向　…　6
- 2 定义　…　8–8
- 3 参考架构描述　…　9–42
- 3.1 目标　…　9
- 3.1.1 能力视图 – 1（CV-1）　…　9
- 3.2 架构原则　…　9
- 3.2.1 面向业务的架构原则　…　10
- 3.2.2 面向技术的架构原则　…　11
- 3.3 质量属性　…　16
- 3.4 系统接口描述／上下文　…　18
- 3.5 物理语境实体　…　20
- 3.5.1 传感器　…　20
- 3.5.2 硬件元素　…　20
- 3.5.3 宿主平台　…　21
- 3.6 功能聚合为模块的判据　…　21
- 3.7 安全概念与做法　…　22
- 3.7.1 硬件安全框架　…　22
- 3.8 硬件概念与做法　…　23
- 3.9 服务上下文描述　…　23
- 3.10 模块间交互　…　28
- 3.10.1 传感器互连　…　29
- 3.10.2 模块交互类型　…　29
- 3.11 系统管理概念与方法　…　34
- 3.11.1 系统管理概念　…　35
- 3.11.2 基于网络的系统管理　…　36
- 3.11.3 硬件管理概述　…　38
- 4 架构定义　…　43–71
- 4.1 服务视图
- 4.1.1 SvcV-4：服务功能描述
- 4.1.2 SvcV-2：服务资源流描述　…　65
- 4.1.3 SvcV-3b：服务-服务矩阵　…　65
- 4.2 数据架构　…　65
- 4.2.1 DIV-1：概念数据模型　…　66
- 4.2.2 DIV-2：逻辑数据模型　…　68
- 4.2.3 DIV-3：物理数据模型　…　69
- 4.3 服务架构　…　69
- 4.4 系统架构　…　69
- 4.4.1 SV-2：系统资源流描述　…　69
- 4.4.2 SV-3：系统-系统矩阵　…　69
- 4.5 整机级硬件　…　69
- 5 SOSA 技术标准　…　72–172
- 5.1 宿主载具／传感器接口　…　72
- 5.1.1 传感器物理封装　…　72
- 5.1.1.1 吊舱　…　72
- 5.1.2 机械接口　…　72
- 5.2 SOSA 传感器物理接口　…　72
- 5.2.1 电气连接器特性　…　72
- 5.2.2 J1 直流电源连接器　…　72
- 5.2.3.2 以太网数据总线（铜缆）　…　80
- 5.2.3.6 安全状况　…　82
- 5.2.3.8 时间同步——1 PPS　…　82
- 5.2.6 天线连接器　…　87
- 5.2.7 直流辅助电源连接器　…　87
- 5.2.7.2 安全地　…　89
- 5.2.8 J7 高速连接器　…　89
- 5.2.8.1 说明　…　89
- 5.2.9 J8 高密度射频连接器　…　89
- 5.2.12.1 交流电源说明　…　94
- 5.2.13 硬件平台 3U 与 6U 槽位配置档规格　…　94
- 5.2.13.4 传导散热式 SOSA 插卡　…　100
- 5.2.14 硬件平台 SOSA 插卡配置档　…　101
- 5.2.15 6U 与 3U 通用插卡配置档规格　…　101
- 5.2.16 SOSA 3U 插卡配置档规格　…　101
- 5.2.16.1 3U I/O 密集型 SBC 插卡配置档　…　101
- 5.2.16.2 3U 旧式载荷配置档　…　103
- 5.2.16.4 3U 数据／控制平面交换机配置档　…　106
- 5.2.16.5 3U 控制／数据平面交换机配置档　…　107
- 5.2.16.6 3U SOSA 射频交换机插卡配置档　…　109
- 5.2.16.7 SOSA 3U 径向时钟插卡配置档　…　110
- 5.2.16.8 3U 外部 I/O 插卡配置档　…　111
- 5.2.17 6U 插卡配置档规格　…　113
- 5.2.17.2 SOSA 6U 控制／数据交换机插卡配置档　…　116
- 5.2.18 遗留交换插卡配置档　…　118
- 5.2.19 外部 I/O 插卡配置档　…　119
- 5.2.20 电源模块　…　121
- 5.2.21 夹层模块　…　123
- 5.2.22 维护控制台端口需求　…　124
- 5.2.22.2 集成方应用开发与调试　…　124
- 5.2.22.3 已部署系统　…　124
- 5.3 SOSA 系统管理需求　…　125
- 5.3.2 SOSA 模块系统管理需求　…　127
- 5.4 SOSA 软件运行环境　…　127
- 5.4.1 描述　…　127
- 5.4.2 范围　…　128
- 5.4.3 推荐　…　130
- 5.4.3.1 依据　…　130
- 5.4.3.2 互操作等级　…　131
- 5.4.4.3 虚拟机　…　131
- 5.5 SOSA 模块交互　…　132
- 5.6 传感器管理　…　132
- 5.6.1 系统管理器模块　…　133
- 5.6.1.1 模块定义　…　133
- 5.6.2 任务管理器模块　…　139
- 5.6.2.1 模块定义　…　139
- 5.7 射频信号层模块　…　143
- 5.7.1 模块化开放式射频架构　…　144
- 5.7.2 对 SOSA 信号层模块的应用　…　145
- 5.7.3 射频接收孔径／换能器模块　…　145
- 5.7.4 射频发射孔径／换能器模块　…　146
- 5.7.6 射频信号层模块交互　…　148
- 5.7.7 信号层模块规则　…　154
- 5.8 信号层模块　…　158
- 5.8.1 接收相机模块标准　…　158
- 5.8.2 发射激光器模块标准　…　158
- 5.8.3 调理器-接收机-激励器模块标准　…　158
- 5.9 数字处理模块　…　158
- 5.9.1 跟踪器　…　158
- 5.9.1.1 定义　…　158
- 5.9.1.3 跟踪器面向 AMTI SAA 的交互　…　159
- 5.10 基础设施模块　…　161
- 5.10.1.1 定义　…　161
- 5.10.1.2 交互　…　161
- 5.10.2 外部数据摄取器　…　162
- 5.10.2.1 定义　…　162
- 5.10.3 宿主平台接口　…　162
- 5.10.3.1 定义　…　162
- 5.11 架构开发／演进计划　…　171
- 附录 A：StdV-1（适用标准）　…　173–173
- A StdV-1（适用标准）　…　173
- 附录 B：AV-2 集成词典　…　174–178
- 附录 C：用例详细规定　…　179–179
- C 用例详细规定　…　179
- C.1 OV-1（高层运行概念）　…　179
- C.2 OV-2（运行资源流）　…　179
- C.3 OV-5b（运行活动模型）　…　179
- 附录 D：DIV-2 与数据字典　…　180–181
- D DIV-2 与数据字典　…　180
- D.1 SOSA 传感器射频控制（分发 A）　…　180
- D.2 MORA 信号层　…　180
- D.3 AMTI SAA 多传感器融合跟踪器　…　180
- D.4 通用系统管理数据元素　…　180
- 附录 E：DIV-3（物理数据模型）　…　182–182
- E DIV-3（物理数据模型）　…　182
- E.1 SOSA 传感器射频控制（分发 A）　…　182
- E.2 射频信号层　…　182
- 附录 F：宿主载具／传感器连接器详细规定　…　183–183
- F 宿主载具／传感器连接器详细规定　…　183
- 附录 G：槽位配置档　…　184–184
- G 槽位配置档　…　184
- 附录 H：各模块逐一详细规定　…　185–185
- H 各模块逐一详细规定　…　185
- 附录 I：SOSA 背板示例　…　186–190
- I SOSA 背板示例　…　186
- I.1 3U 中型背板示例　…　186
- I.2 3U 大型背板示例　…　186
- I.3 3U/6U 混合背板示例　…　187
- 缩略语与缩写　…　191–194

**图清单**

- 图 1 构成 SOSA 模块的各个侧面　…　2
- 图 2 SOSA 技术标准所采用的架构开发方法　…　2
- 图 3 SOSA CV-I　…　9
- 图 4 标称情形的 SV-1　…　19
- 图 5 传感器吊舱特例的 SV-1　…　20
- 图 6 SvcV-1 顶层 SOSA 服务上下文描述　…　24
- 图 7 SOSA 传感器互连　…　29
- 图 8 SOSA 基于网络的系统管理架构　…　37
- 图 9 SOSA 硬件系统管理逻辑框图　…　39
- 图 10 SOSA 系统管理背板／机箱实现示例　…　40
- 图 11 SOSA 系统管理插卡实现示例　…　41
- 图 12 任务实体的 DIV-1　…　67
- 图 13 管理实体的 DIV-1　…　68
- 图 14 SOSA 硬件构建块　…　70
- 图 15 J1 电源连接器引脚排列　…　73
- 图 16 J2 信号连接器引脚排列　…　74
- 图 17 输入时间翻转脉冲（1 PPS）信号特性　…　82
- 图 18 J3 视频连接器插针排布　…　84
- 图 19 J4 光纤连接器插针排布　…　86
- 图 20 J6 辅助电源连接器插针排布　…　88
- 图 21 J8 射频连接器引脚排布　…　90
- 图 22 J9 射频连接器引脚排布　…　91
- 图 23 J10 交流电源连接器引脚排布　…　93
- 图 24 ANSI/VITA 65.0 3U I/O 密集型 SBC 槽位配置档 SLT3-PAY-1F1F2U1TU1T1U1T-　…　103
- 图 25 SLT3-PAY-2F2U-14.2.3 的 ANSI/VITA 65.0 载荷槽位配置档　…　104
- 图 26 ANSI/VITA 65.0 载荷槽位配置档 SLT3-PAY-1F1U1S1S1U1U2F1H-14.6.11-n　…　105
- 图 27 ANSI/VITA 65.0 载荷槽位配置档 SLT3-PAY-1F1U1S1S1U1U4F1J-14.6.13-n　…　106
- 图 28 ANSI/VITA 65.0 控制／扩展平面交换机槽位配置档 SLT3-SWH-6F8U-14.4.15　…　107
- 图 29 ANSI/VITA 65.0 控制／数据平面交换机槽位配置档 SLT3-SWH-6F1U7U-14.4.14　…　108
- 图 30 ANSI/VITA 65.0 控制／数据平面交换机槽位配置档 SLT3-SWH-4F1U7U1J-14.8.7-n　…　109
- 图 31 ANSI/VITA 65.0 3U 射频交换机槽位配置档 SLT3-SWH-1F1S1S1U1U1K-14.8.8-n　…　110
- 图 32 ANSI/VITA 65.0 径向时钟槽位配置档 SLT3x-TIM-2S1U22S1U2U1H-14.9.2-n　…　111
- 图 33 ANSI/VITA 65.0 3U 外部 I/O 槽位配置档 SLT3-PAY-2U2U-14.2.17　…　112
- 图 34 ANSI/VITA 65.0 6U 载荷槽位配置档 SLT6-PAY-4F2Q1H4U1T1S1S1TU2U2T1H-　…　114
- 图 35 ANSI/VITA 65.0 6U 载荷槽位配置档 SLT6-PAY-4F1Q1H4U1T1S1S1TU2U2T1H-　…　115
- 图 36 ANSI/VITA 65.0 6U 控制／数据交换机槽位配置档 SLT6-SWH-14F16U1U15U1J-　…　118
- 图 37 SLT6-SWH-16U20F-10.4.2 的 ANSI/VITA65.0 交换槽位配置档　…　119
- 图 38 ANSI/VITA 65.0 6U 外部 I/O 槽位配置档 SLT6-PAY-4U2U-10.2.8　…　121
- 图 39 FACE 软件运行环境及拟用于 SOSA REI 的子集（红色　…　130
- 图 40 传感器管理架构视图　…　133
- 图 41 系统管理器交互　…　134
- 图 42 射频信号层模块交互　…　145
- 图 43 射频接收孔径／换能器交互　…　146
- 图 44 射频发射孔径／换能器交互　…　147
- 图 45 射频调理器接收机／激励器交互　…　147
- 图 46 宿主平台接口模块交互　…　163
- 图 47 SOSA 高层用例　…　179
- 图 48 3U 中型背板示例　…　186
- 图 49 3U 大型背板示例　…　187
- 图 50 3U/6U 混合背板示例　…　189

**表清单**

- 表 1 SOSA 质量属性（按优先级降序）　…　17
- 表 2 SvcV-1 模块描述　…　24
- 表 3 交互类型　…　30
- 表 4 交互角色、端点与符号　…　31
- 表 5 SOSA SvcV-4
- 表 6 转塔式传感器类别　…　72
- 表 7 传感器连接器　…　72
- 表 8 J1 直流电源连接器引脚分配　…　73
- 表 9 J2 信号连接器引脚分配　…　75
- 表 10 J3 视频连接器引脚分配　…　84
- 表 11 J4 光纤连接器引脚分配　…　86
- 表 12 J5 GPS 连接器引脚分配　…　87
- 表 13 符合性方法：(TBD)　…　87
- 表 14 J7 引脚分配　…　89
- 表 15 J8 射频引脚分配　…　90
- 表 16 J9 射频引脚分配　…　92
- 表 17 辅助射频连接　…　92
- 表 18 J10 交流电源引脚分配　…　93
- 表 19 硬件模块散热方式　…　100
- 表 20 SLT3-PAY-1F1F2U1T1U1T1U1T-14.2.16 所引用的 ANSI/VITA 65.1 模块配置档　…　103
- 表 21 SLT3-PAY-1F1U1S1S1U1U2F1H-14.6.11-n 的 ANSI/VITA 65.1 槽位配置档　…　105
- 表 22 SLT3-PAY-1F1U1S1S1U1U2F1H-14.6.11-n 的 ANSI/VITA 65.1 模块配置档　…　106
- 表 23 SLT3-PAY-1F1U1S1S1U1U4F1J-14.6.13-n 的 ANSI/VITA 65.1 槽位配置档　…　106
- 表 24 SLT3-PAY-1F1U1S1S1U1U4F1J-14.6.13-n 的 ANSI/VITA 65.1 模块配置档　…　106
- 表 25 SLT3-SWH-6F8U-14.4.15 的 ANSI/VITA 65.1 模块配置档　…　107
- 表 26 SLT3-SWH-6F1U7U-14.4.14 的 ANSI/VITA 65.1 模块配置档　…　108
- 表 27 SLT3-SWH-4F1U7U1J-14.8.7-n 的 ANSI/VITA 65.1 模块配置档　…　109
- 表 28 SLT3-SWH-1F1S1S1U1U1K-14.8.8-n 的 ANSI/VITA 65.1 模块配置档　…　110
- 表 29 SLT3x-TIM-2S1U22S1U2U1H-14.9.2-n 的 VITA 65.1 槽位配置档　…　111
- 表 30 SLT3x-TIM-2S1U22S1U2U1H-14.9.2-n 的 VITA 65.1 模块配置档　…　111
- 表 31 SLT3-PAY-2U2U-14.2.17 的 ANSI/VITA 65.1 模块配置档　…　112
- 表 32 SLT6-PAY-4F2Q1H4U1T1S1S1TU2U2T1H-10.6.4-n 的 ANSI/VITA 65.1 槽位配置档　…　114
- 表 33 SLT6-PAY-4F2Q1H4U1T1S1S1TU2U2T1H-10.6.4-n 的 ANSI/VITA 65.1 模块配置档　…　115
- 表 34 SLT6-PAY-4F1Q1H4U1T1S1S1TU2U2T1H-10.6.3-n 的 ANSI/VITA 65.1 模块配置档　…　116
- 表 35 SLT6-SWH-14F16U1U15U1J-10.8.1-n 的 ANSI/VITA 65.1 槽位配置档　…　118
- 表 36 SLT6-SWH-14F16U1U15U1J-10.8.1-n 的 ANSI/VITA 65.1 模块配置档　…　118
- 表 37 SLT6-PAY-4U2U-10.2.8 的 ANSI/VITA 65.1 模块配置档　…　121
- 表 38 维护控制台端口信号电平　…　125
- 表 39 通用系统管理交互　…　134
- 表 40 任务管理交互表　…　139
- 表 41 射频信号层模块交互表　…　148
- 表 42 RF 信号层模块交互端点　…　155
- 表 43 跟踪器模块交互　…　159
- 表 44 其他跟踪器交互　…　160
- 表 45 AMTI SAA 任务配置数据　…　161
- 表 46 宿主平台接口交互　…　163
- 表 47 AV-2 集成词典（SOSA 术语总表）

<!-- /装置 中文目录 -->

<!-- 原书 p.ix ｜ PDF p.9 -->

## Preface ｜ 前言

## Executive Summary ｜ 执行摘要

This document constitutes a "Snapshot" of the Technical Standard for SOSA™ (Sensor Open Systems Architecture) Reference Architecture, Edition 1.0 in support of United States Department of Defense (DoD) Command, Control, Communications, Computer, Intelligence, Surveillance, and Reconnaissance (C4ISR) development. The goal of The Open Group SOSA Consortium is to develop open architecture at the right level for Communications, Electro-Optical/Infra-Red (EO/IR), Electronic Warfare (EW), Radar, and Signals Intelligence (SIGINT). The SOSA Consortium strives to develop an ecosystem that allows interoperability, reuse, and faster delivery of products to market through vertical integration from cables, mechanical interfaces, hardware, software, and system designs.

本文件是《SOSA™（传感器开放系统架构）参考架构技术标准》第 1.0 版的一份"快照版"，用以支撑美国国防部（DoD）指挥、控制、通信、计算机、情报、监视与侦察（C4ISR）的开发。The Open Group SOSA 联盟的目标，是为通信、光电／红外（EO/IR）、电子战（EW）、雷达与信号情报（SIGINT）在恰当的层级建立开放架构。SOSA 联盟力求建立一个生态：由电缆、机械接口、硬件、软件与系统设计自上而下贯通，实现互操作、复用，并更快把产品交付市场。

## Background ｜ 背景

Today's development of sensor systems typically entails a unique set of requirements and a single vendor. This form of development has served the military sensor community well; however, this stovepipe development process has had some undesired side-effects including long lead times, cumbersome improvement processes, lack of hardware, software, and system reuse between various sensors and platforms that result in platform-unique designs that are locked to a single deployed platform.

当今传感器系统的开发，通常意味着一套独特的需求与单一供应商。这种开发方式曾很好地服务了军用传感器界；然而这种"烟囱式"开发过程也带来一些不希望的副作用，包括交付周期长、改进流程笨重、不同传感器与平台之间缺乏硬件、软件与系统复用，最终形成锁定于单一在役平台的平台专用设计。

As the complexity of sensor and mission equipment has increased, this has resulted in increased cost and development times, and impeded the ability to integrate new hardware, software, or entire payloads into deployable platform systems. This — combined with the extensive testing and airworthiness/ground/sea/space qualification requirements — has begun to affect the ability of the military sensor community to rapidly deploy new capabilities across the military fleet.

随着传感器与任务设备复杂度的提高，成本与开发周期随之上升，把新硬件、新软件或整个载荷集成进可部署平台系统的能力也受到妨碍。这一点——再加上大量的测试与适航／地面／海上／空间鉴定要求——已开始影响军用传感器界在全军机队中快速部署新能力的本领。

The current C4ISR community procurement system does not promote the process of hardware; software, and payload reuse. Furthermore, the sensors development community has not created standards that facilitate the reuse of components.

当前的 C4ISR 界采办体系并不促进硬件、软件与载荷的复用；此外，传感器开发界也未建立便于组件复用的标准。

Part of the reason for this is the relatively small size of the military market. Another contributing factor is the difficulty of developing qualified sensors payloads. An additional problem is the inability to use current commercial standards because they do not adhere to the stringent safety requirements intended to reduce risk and the likelihood of loss of host platform, reduced mission capability, and ultimately loss of life.

部分原因在于军用市场规模相对较小；另一个成因是开发合格传感器载荷的难度；还有一个问题是无法直接采用现行商业标准——它们不满足那些旨在降低风险、降低宿主平台损失可能性、降低任务能力受损乃至最终降低人员生命损失的严苛安全要求。

To counter these trends, the Air Force, Army, and Navy, enabled by the expertise and experience of the defense industrial base, are promoting a new approach.

为扭转这些趋势，空军、陆军与海军在国防工业基础的专长与经验支撑下，正在推行一种新的做法。

## Approach ｜ 做法

The SOSA initiative, formed as a Consortium of The Open Group, addresses the challenges of rapid, affordable capability evolution for today's military community. Part of the SOSA approach is to develop an Open Systems Architecture (OSA), captured in the SOSA Technical

SOSA 倡议以 The Open Group 联盟的形式组建，回应今日军事界对快速、可负担能力演进的挑战。SOSA 做法的一部分，是建立一套开放系统架构（OSA），并记载于 SOSA 技术标准之中，覆盖软件、硬件与接口。

<!-- 原书 p.x ｜ PDF p.10 -->

Standard that addresses software, hardware, and interfaces. This OSA is designed to promote portability and create product families across the Communications, EO/IR, EW, Radar, and SIGINT community. The SOSA Technical Standard is intended to promote the development of reusable sensor components applicable to a broad class of sensors and host platforms.

这套 OSA 旨在促进可移植性，并在通信、光电／红外、电子战、雷达与信号情报各界之间形成产品族。SOSA 技术标准意在促进可复用传感器组件的开发，使其适用于广泛类别的传感器与宿主平台。

Another aspect of the SOSA approach is to develop an Open Business Model that addresses the needs of the acquisition community and ensures a strong industrial base. It includes business processes to adapt the procurement to a Modular Open Systems Approach (MOSA) reality, protect industry Intellectual Property (IP), and incentivize industry to invest in broadly applicable technologies that can be applied to a wide variety of sensors.

SOSA 做法的另一方面，是建立一套开放业务模式，回应采办界的需要并确保雄厚的工业基础。它包含若干业务过程：使采办适应模块化开放系统方法（MOSA）的现实、保护产业知识产权（IP）、并激励产业投入可广泛适用的技术、以用于多种传感器。

The SOSA approach allows "capabilities" to be developed as components that are exposed to other components through well-defined interfaces. It also provides for the reuse of SOSA module functionality across different environments. A SOSA module will have a core set of mandatory functionality, but different variants may be developed over time and different systems may have different additional characteristics (e.g., special environmental conditions, higher throughput, higher reliability, etc). These variants will be considered for incorporation into later editions of the SOSA Technical Standard. The SOSA Technical Standard does not guarantee compliance with any safety certification standard, but instead provides all the necessary capabilities to achieve that in the implementation phase by the vendors.

SOSA 做法允许把"能力"作为组件来开发，并经良好定义的接口把这些组件暴露给其他组件；它还使 SOSA 模块的功能得以在不同环境间复用。一个 SOSA 模块将具备一套必选的核心功能，但随时间可能衍生不同变体，不同系统也可能具有不同的附加特性（如特殊环境条件、更高吞吐、更高可靠性等）。这些变体将被考虑纳入 SOSA 技术标准的后续版本。SOSA 技术标准不保证对任何安全认证标准的**符合程度**达到要求，而是提供全部必要能力，供厂商在实现阶段达成该认证。

Ultimately, the SOSA Consortium key objectives are to reduce development, integration costs, and time to field sensor capabilities, and promote affordable capability evolution.

归根结底，SOSA 联盟的关键目标，是降低传感器能力的开发与集成成本、缩短列装时间，并促进可负担的能力演进。

The Open Group

The Open Group（开放群组）

The Open Group is a global consortium that enables the achievement of business objectives through technology standards. Our diverse membership of more than 600 organizations includes customers, systems and solutions suppliers, tools vendors, integrators, academics, and consultants across multiple industries.

The Open Group 是一个全球性联盟，通过技术标准帮助各方达成业务目标。其成员逾 600 家组织，涵盖多个行业中的客户、系统与解决方案供应方、工具厂商、集成商、学术界与咨询机构。

The mission of The Open Group is to drive the creation of Boundaryless Information Flow™ achieved by:

The Open Group 的使命，是推动"无边界信息流™"（Boundaryless Information Flow™）的建成，其途径包括：

Working with customers to capture, understand, and address current and emerging requirements, establish policies, and share best practices Working with suppliers, consortia, and standards bodies to develop consensus and facilitate interoperability, to evolve and integrate specifications and open source technologies Offering a comprehensive set of services to enhance the operational efficiency of consortia Developing and operating the industry's premier certification service and encouraging procurement of certified products Further information on The Open Group is available at www.opengroup.org.

与客户合作，捕捉、理解并应对当前与新兴的需求，确立政策并分享最佳实践；与供应方、联盟及标准机构合作，形成共识并促进互操作，演进并集成规范与开源技术；提供一整套服务以提升联盟的运行效率；建立并运营业界一流的认证服务，并鼓励采购经认证的产品。有关 The Open Group 的更多信息见 www.opengroup.org。

The Open Group publishes a wide range of technical documentation, most of which is focused on development of Standards and Guides, but which also includes white papers, technical studies, certification and testing documentation, and business titles. Full details and a catalog are available at www.opengroup.org/library.

The Open Group 出版范围广泛的技术文档，多数聚焦标准与指南的制定，也包括白皮书、技术研究、认证与测试文档以及业务类出版物。详情与目录见 www.opengroup.org/library。

<!-- 原书 p.xi ｜ PDF p.11 -->

## This Document ｜ 本文件

This document is a Snapshot of what will, after maturation, become the Technical Standard for SOSA™ (Sensor Open Systems Architecture) Reference Architecture, Edition 1.0. This document is developed and maintained by the SOSA Consortium.

本文件是《SOSA™（传感器开放系统架构）参考架构技术标准》第 1.0 版成熟之前的快照版。本文件由 SOSA 联盟开发与维护。

<!-- 原书 p.xii ｜ PDF p.12 -->

## Trademarks ｜ 商标

ArchiMate®, DirecNet®, Making Standards Work®, Open O® logo, Open O and Check® Certification logo, OpenPegasus®, Platform 3.0®, The Open Group®, TOGAF®, UNIX®, UNIXWARE®, and the Open Brand X® logo are registered trademarks and Boundaryless Information Flow™, Build with Integrity Buy with Confidence™, Dependability Through Assuredness™, Digital Practitioner Body of Knowledge™, DPBoK™, EMMM™, FACE™, the FACE™ logo, IT4IT™, the IT4IT™ logo, O-DEF™, O-HERA™, O-PAS™, Open FAIR™, Open Platform 3.0™, Open Process Automation™, Open Subsurface Data Universe™, Open Trusted Technology Provider™, Sensor Integration Simplified™, SOSA™, and the SOSA™ logo are trademarks of The Open Group.

ArchiMate®、DirecNet®、Making Standards Work®、Open O® 标识、Open O and Check® 认证标识、OpenPegasus®、Platform 3.0®、The Open Group®、TOGAF®、UNIX®、UNIXWARE® 以及 Open Brand X® 标识是注册商标；Boundaryless Information Flow™、Build with Integrity Buy with Confidence™、Dependability Through Assuredness™、Digital Practitioner Body of Knowledge™、DPBoK™、EMMM™、FACE™、FACE™ 标识、IT4IT™、IT4IT™ 标识、O-DEF™、O-HERA™、O-PAS™、Open FAIR™、Open Platform 3.0™、Open Process Automation™、Open Subsurface Data Universe™、Open Trusted Technology Provider™、Sensor Integration Simplified™、SOSA™ 以及 SOSA™ 标识是 The Open Group 的商标。

Excel® and Microsoft® are registered trademarks of Microsoft Corporation in the United States and/or other countries.

Excel® 与 Microsoft® 是 Microsoft Corporation 在美国和／或其他国家的注册商标。

Java® is a registered trademark of Oracle and/or its affiliates.

Java® 是 Oracle 和／或其关联方的注册商标。

OpenVPX™ and VITA™ are trademarks of VITA in the United States and other countries.

OpenVPX™ 与 VITA™ 是 VITA 在美国和其他国家的商标。

POSIX® is a registered trademark of the Institute of Electrical and Electronic Engineers, Inc.

POSIX® 是美国电气与电子工程师学会（IEEE）公司的注册商标。

Python™ is a trademark of the Python Software Foundation.

Python™ 是 Python Software Foundation 的商标。

SAE™ is a trademark of SAE International.

SAE™ 是 SAE International 的商标。

UML® is a registered trademark and Data Distribution Service™, DDS™, and Unified Modeling Language™ are trademarks of Object Management Group, Inc. in the United States and/or other countries.

UML® 是注册商标；Data Distribution Service™、DDS™ 与 Unified Modeling Language™ 是 Object Management Group, Inc. 在美国和／或其他国家的商标。

All other brands, company, and product names are used for identification purposes only and may be trademarks that are the sole property of their respective owners.

其他所有品牌、公司与产品名称仅用于标识目的，可能是各自所有者独有的商标。

<!-- 原书 p.xiii ｜ PDF p.13 -->

## Acknowledgements ｜ 致谢

The Open Group gratefully acknowledges the contribution of the following people in the development of this Snapshot:

The Open Group 谨对本快照版开发中下列人士的贡献致以谢意：

Principal Authors

主要作者

Rusty Baldwin, Riverside Research, (former member of the) Software WG Gerry Bezenek, Northrop Grumman, Hardware WG Nathan Binkley, KeyW Corporation, Electrical Mechanical WG Jeffrey Bryant, BAE, Vice-Chair Steering Committee Paul Clarke, NGC, Vice-Chair Architecture WG Charles Patrick Collier, Harris, Chair Hardware WG

Rusty Baldwin（Riverside Research，软件工作组〔前成员〕）、Gerry Bezenek（Northrop Grumman，硬件工作组）、Nathan Binkley（KeyW Corporation，电气机械工作组）、Jeffrey Bryant（BAE，指导委员会副主席）、Paul Clarke（NGC，架构工作组副主席）、Charles Patrick Collier（Harris，硬件工作组主席）

George Dalton, KeyW, Vice-Chair Electrical Mechanical WG Steve Davidson, Raytheon Company, Chair Architecture WG Jason Dirner, CERDEC, Vice-Chair Hardware WG Scott Hinnershitz, Lockheed Martin, Hardware WG Tim Ibrahim, L-3 Technologies, Chair Electrical Mechanical WG David Linden, Leidos, Electrical Mechanical WG Michael Moore, Aspen Consulting Group, Architecture WG, Vice-Chair Software WG Michael Orlovsky, Lockheed Martin Fire and Missiles, Chair Software WG Shawn Reese, General Dynamics – MS, Architecture/Software WG Lee Riddle, Georgia Tech Research Institute, Hardware WG Greg Rocco, MIT Lincoln Laboratory, Hardware WG Ned Saunders, CEREC, Architecture/Software WG Trent Styrcula, CERDEC, Hardware WG Dan Toohey, Mercury, Hardware WG John Topping, Leidos, Electrical Mechanical WG

George Dalton（KeyW，电气机械工作组副主席）、Steve Davidson（Raytheon Company，架构工作组主席）、Jason Dirner（CERDEC，硬件工作组副主席）、Scott Hinnershitz（Lockheed Martin，硬件工作组）、Tim Ibrahim（L-3 Technologies，电气机械工作组主席）、David Linden（Leidos，电气机械工作组）、Michael Moore（Aspen Consulting Group，架构工作组、软件工作组副主席）、Michael Orlovsky（Lockheed Martin Fire and Missiles，软件工作组主席）、Shawn Reese（General Dynamics – MS，架构／软件工作组）、Lee Riddle（Georgia Tech Research Institute，硬件工作组）、Greg Rocco（MIT Lincoln Laboratory，硬件工作组）、Ned Saunders（CEREC，架构／软件工作组）、Trent Styrcula（CERDEC，硬件工作组）、Dan Toohey（Mercury，硬件工作组）、John Topping（Leidos，电气机械工作组）

Additional Contributors

其他贡献者

John Bowling, USAF, Chair Business WG

John Bowling（USAF，业务工作组主席）

<!-- 原书 p.xiv ｜ PDF p.14 -->

Robert Guessferd, BAE, former Vice-Chair Business WG Donald F. Herrick, formerly Raytheon Company, former Chair Business WG Jason Jundt, GE Aviation, Vice-Chair Business WG

Robert Guessferd（BAE，业务工作组前副主席）、Donald F. Herrick（原 Raytheon Company，业务工作组前主席）、Jason Jundt（GE Aviation，业务工作组副主席）

Ilya Lipkin, USAF, Chair Steering Committee

Ilya Lipkin（USAF，指导委员会主席）

Funding for the SOSA Consortium and its work products comes from its member organizations, which are listed at https://www.opengroup.org/sosa/members.

SOSA 联盟及其工作产品的经费来自其成员组织，成员名录见 https://www.opengroup.org/sosa/members。

And Naval Air System Command (NAVAIR) under NAVAIR Cooperative Agreement No. N00421-12-2-0004. The US not withstanding any copyright notation thereon. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of the Naval Air Warfare Center Aircraft Division or the US Government.

以及海军航空系统司令部（NAVAIR），依据 NAVAIR 合作协议 N00421-12-2-0004。美方对其上的任何著作权标注不予主张（原文：The US not withstanding any copyright notation thereon）。本文件所载观点与结论为作者所有，**不宜**解释为海军航空作战中心飞机分部或美国政府的官方政策，无论明示或默示。

<!-- 原书 p.xv ｜ PDF p.15 -->

## Referenced Documents ｜ 引用文件

Order of Precedence

效力顺序

In the event of a conflict between the text of this document and the references cited herein, the text of this document takes precedence. Nothing in this document, however, supersedes applicable laws and regulations unless a specific exemption has been obtained.

若本文件正文与本文所引参考文献之间发生冲突，以本文件正文为准。但本文件任何内容均不取代适用的法律与法规，除非已取得专门豁免。

Normative References

规范性引用文件

Normative references for the SOSA Technical Standard are defined in Section 1.4.

SOSA 技术标准的规范性引用文件见第 1.4 节。

Informative References

资料性引用文件

> **译注**：以下清单首句（`The following documents are referenced in this Snapshot. Please note that the links below are good at the time of writing but cannot be guaranteed for the future.)`）即「本快照版引用了下列文件；请注意：以下链接在写作时有效，未来不保证」，其下题名清单不译。

<!-- 未译 引用文件的标准题名清单 -->

The following documents are referenced in this Snapshot. Please note that the links below are good at the time of writing but cannot be guaranteed for the future.) ANSI/VITA 42.0-2016: XMC: Switched Mezzanine Card Base Specification ANSI/VITA 42.3-2014: XMC: PCI Express Protocol Layer ANSI/VITA 46.0-2013: VPX: Baseline

ANSI/VITA 46.3-2012 (R2018): VPX: 4x Serial Rapid IO Signal Mapping ANSI/VITA 46.9-2018: VPX: PMC/XMC Rear I/O Fabric Signal Mapping on 3U and 6U VPX Modules ANSI/VITA 46.11-2015: VPX: System Management ANSI/VITA 47.3 (DRAFT): Environments, Design and Construction, Safety, and Quality for Plug-in Units ANSI/VITA 48.2-2010: Mechanical Standard for Conduction Cooling VPX ANSI/VITA 48.8-2017: VPX REDI: Mechanical Specification Using Air Flow-by Cooling Applied to VPX ANSI/VITA 49.2-2017: VITA Radio Transport (VRT) Electromagnetic Spectrum: Signals and Applications ANSI/VITA 62.0-2016: VPX: Modular Power Supply ANSI/VITA 65.0-2017: OpenVPX™ System ANSI/VITA 65.1-2017: Profile Tables

ANSI/VITA 66.0-2016: VPX: Optical Interconnect on VPX – Base Standard

<!-- 原书 p.xvi ｜ PDF p.16 -->

ANSI/VITA 67.0-2012: VPX: Coaxial Interconnect – Base Standard

ANSI/VITA 67.3-2017: VPX: Coaxial Interconnect, 6U, 4 Position SMPM Configuration Anti-Tamper (AT) Technical Implementation Guide (TIG), Version 1.0, November 2016;

reference available to personnel authorized by the US Government – request a copy from the US DoD Anti-Tamper Executive Agent AS6129: Interface Standard, Airborne EO/IR Systems, Electrical, SAE, December 2012 AS6169: Interface Standard, Airborne EO/IR Systems, Mechanical, SAE, February 2013 AS39029/28: Contacts, Electrical Connector, Pin, Crimp Removable, Shielded, Size 12 (for MIL-DTL-38999 Series I, II, III, and IV Connectors), SAE International AS39029/56: Contacts, Electrical Connector, Socket, Crimp Removable (for MIL-C-38999 Series I, III, and IV Connectors), SAE International AS39029/58: Contacts, Electrical Connector, Pin, Crimp Removable (for MIL-DTL-24308, MIL-DTL-38999 Series I, II, III, and IV, and MIL-DTL-55302/69 and MIL-DTL-

83733 Connectors), SAE International AS39029/75: Contacts, Electrical Connector, Socket, Crimp Removable, Shielded, Size 12 (for MIL-DTL-38999 Series I, III, and IV Connectors), SAE International AS39029/90: Contact, Electrical Connector, Concentric Twinax, Pin Size 8, SAE International AS39029/91: Contact, Electrical Connector, Concentric Twinax, Socket, Shielded, Size 8, SAE International Cyber Survivability Endorsement Implementation Guide, Version 1.01, Joint Chiefs of Staff, 2016; US Government authorized personnel may refer to: https://go.intelink.gov/my.policy DO-178: Software Considerations in Airborne Systems and Equipment Certification, Radio Technical Commission for Aeronautics, Inc. (RTCA)

DoDAF Architecture Framework Version 2.02, August 2010; refer to:

http://dodcio.defense.gov/Library/DoD-Architecture-Framework/ FACE™ Technical Standard, Edition 3.0, The Open Group Standard (C17C), November 2017, published by The Open Group; refer to: www.opengroup.org/library/c17c FROST Architecture Specification, Version 1.0, FROST Interface Control Document, December 2018, available upon request to personnel authorized by the US Government I²C Bus Specification Version 2.1, January 2000 ICD-GPS-060B: GPS User Equipment (Phase III) Interface Control Document (ICD) for the Precise Time and Time Interval (PTTI) Interface. February 2002 IEEE Std 802.3-2008: IEEE Standard for Information Technology – Telecommunications and Information Exchange Between Systems – Local and Metropolitan Area Networks – Specific Requirements Part 3: Carrier Sense Multiple Access with Collision Detection

(CSMA/CD) Access Method and Physical Layer Specifications

<!-- 原书 p.xvii ｜ PDF p.17 -->

ISO/IEC 11801:2002: Information Technology – Generic Cabling for Customer Premises;

refer to: https://www.iso.org/standard/36491.html MIL-PRF-29504/4: Termini, Fiber Optic, Connector, Removable, Environment Resisting;

Pin Terminus, Size 16, Rear Release, MIL-DTL-38999 Series III, December 2006 MIL-PRF-29504/5: Termini, Fiber Optic, Connector, Removable, Environment Resisting Socket Terminus, Size 16, Rear Release, MIL-DTL-38999 Series III, December 2006 MIL-PRF-39012: Performance Specification: Connectors, Coaxial, Radio Frequency,

General Specification for MIL-STD-464, April 2005

MIL-STD-464, Department of Defense Interface Standard: Electromagnetic Environmental Effects Requirements for Systems, December 2010 MIL-HDBK-516C, Department of Defense Handbook: Airworthiness Certification Criteria, December 2015 MIL-STD-704F, Department of Defense Interface Standard: Aircraft Electric Power Characteristics, March 2004 MIL-STD-1344, Department of Defense Military Standard: Test Methods for Electrical Connectors, September 1977 MIL-STD 1553B, Department of Defense Military Standard: Aircraft Internal Time Division Command/Response Multiplex Data Bus, September 1978; refer to: http://everyspec.com/MIL-STD/MIL-STD-1500-1599/download.php?spec=MIL-STD-

1553B.002938.pdf

Modular Open RF Architecture (MORA) Specification, Version 2.1, June 01, 2017 The current version of this specification is available via the VICTORY Portal at https://victory-standards.org/index.php/vic-port. For more information, contact usarmy.apg.cerdec.mail.cerdec@mail.mil.

Open Trusted Technology Provider™ Standard (O-TTPS) – Mitigating Maliciously Tainted and Counterfeit Products: Part 1: Requirements and Recommendations, Version 1.1.1 (technically equivalent to ISO/IEC 20243-1:2018), The Open Group Standard (C185-1), September 2018, published by The Open Group; refer to: www.opengroup.org/library/c185-1 PCIe Version 3.0: Peripheral Computer Interface extended – PCI Express Base Specification, November 2010 REDHAWK Framework and Tactical Open Architecture (TOA), February 2018; refer to:

http://redhawksdr.github.io/Documentation/index.html Risk Management Framework (RMF) for DoD Information Technology (IT), Department of Defense Instruction 8510.01, July 2017; refer to: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/851001_2014.pdf

SMPTE Std 292:2011: 1.5 Gb/s Signal/Data Serial Interface, IEEE

SMPTE Std 297:2006: For Television – Serial Digital Fiber Transmission System for

SMPTE 259M, SMPTE 344M, SMPTE 292, and SMPTE 424M Signals, IEEE

<!-- 原书 p.xviii ｜ PDF p.18 -->

SMPTE Std 424:2012: 3 Gb/S Signal/Data Serial Interface, IEEE SOSA Business Guide, Version 0.8, Open Group Guide (G177), October 2017, published by The Open Group; refer to: www.opengroup.org/library/g177 STANAG 4586, NATO Standardization Agreement: Standard Interfaces of UAV Control System (UCS) for NATO UAV Interoperability, November 2007 TIA-232: Telecommunications Industry Association Standard: Interface Between Data Terminal Equipment and Data Circuit-Terminating Equipment Employing Serial Binary Data Interchange, October 1997; refer to: WWW.tiaonline.org TIA-422: Telecommunications Industry Association Standard: Electrical Characteristics of Balanced Voltage Digital Interface Circuits, January 2000; refer to: www.tiaonline.org Universal Serial Bus (USB) 2.0 Specification, April 2000 Universal Serial Bus (USB) 3.0 Specification, November 2008 VICTORY: Vehicular Integration for C4ISR/EW Interoperability Standard Specifications, Version 1.7, February 15, 2018; refer to: https://victory-standards.org/

<!-- 原书 p.xix ｜ PDF p.19 -->

<!-- 原书 p.xx ｜ PDF p.20 -->

<!-- /未译 引用文件的标准题名清单 -->
