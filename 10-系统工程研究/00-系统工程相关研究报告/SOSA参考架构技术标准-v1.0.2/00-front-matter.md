# 前置：封面·目录·图表清单·序

> 原书 p.i–xx ｜ PDF p.1–20

The Open Group Snapshot

Technical Standard for SOSA™ Reference Architecture,

Edition 1.0, Version 2

- You have a choice: you can either create your own future, or you can become the victim of a future that someone else creates for you. By seizing the transformation opportunities, you are seizing the opportunity to create your own future.

Vice Admiral (ret.) Arthur K. Cebrowski

NOTICE

Snapshots are draft documents, which provide a mechanism for The Open Group to disseminate information on its current direction and thinking to an interested audience, in advance of formal publication, with a view to soliciting feedback and comment. A Snapshot represents the interim results of a technical activity. Although at the time of publication The Open Group intends to progress the activity towards publication of a Preliminary Standard or Open Group Standard, The Open Group is a consensus organization, and makes no commitment regarding publication. Similarly, a Snapshot does not represent any commitment by any member of The Open Group to make any specific products available. This Snapshot is intended to make public the direction, thinking and path the SOSA Consortium is taking in the development of the SOSA Reference Architecture. We invite your feedback and guidance. To provide feedback on this Snapshot, please send comments by email to ogsosa-admin@opengroup.us no later than December 31, 2019. This Snapshot document is valid through December 31, 2019 only. For information on joining The Open Group SOSA™ Consortium, please send email to ogsosa-admin@opengroup.us or visit our website at www.opengroup.org/sosa.

Case: 88ABW-2019-0039; Cleared: 2019-01-07

<!-- 原书 p.i ｜ PDF p.1 -->

Copyright © 2019, The Open Group LLC for the benefit of the SOSA Consortium Members. All rights reserved. The Open Group hereby authorizes you to use this document for any purpose, PROVIDED THAT any copy of this document, or any part thereof, which you make shall retain all copyright and other proprietary notices contained herein. This document may contain other proprietary notices and copyright information. Nothing contained herein shall be construed as conferring by implication, estoppel, or otherwise any license or right under any patent or trademark of The Open Group or any third party. Except as expressly provided above, nothing contained herein shall be construed as conferring any license or right under any copyright of The Open Group. Note that any product, process, or technology in this document may be the subject of other intellectual property rights reserved by The Open Group, and may not be licensed hereunder. This document is provided "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT. Some jurisdictions do not allow the exclusion of implied warranties, so the above exclusion may not apply to you. Any publication of The Open Group may include technical inaccuracies or typographical errors. Changes may be periodically made to these publications; these changes will be incorporated in new editions of these publications. The Open Group may make improvements and/or changes in the products and/or the programs described in these publications at any time without notice. Should any viewer of this document respond with information including feedback data, such as questions, comments, suggestions, or the like regarding the content of this document, such information shall be deemed to be non-confidential and The Open Group shall have no obligation of any kind with respect to such information and shall be free to reproduce, use, disclose, and distribute the information to others without limitation. Further, The Open Group shall be free to use any ideas, concepts, know-how, or techniques contained in such information for any purpose whatsoever including but not limited to developing, manufacturing, and marketing products incorporating such information. If you did not obtain this copy through The Open Group, it may not be the latest version. For your convenience, the latest version of this publication may be downloaded at www.opengroup.org/library.

The Open Group Snapshot Technical Standard for SOSA™ Reference Architecture, Edition 1.0, Version 2 Document Number: S180

Authored by The Open Group SOSA™ Consortium. Published by The Open Group, January 2019. Comments relating to the material contained in this document may be submitted to: The Open Group, 800 District Avenue, Suite 150, Burlington, MA 01803, United States or by electronic mail to: ogsosa-admin@opengroup.us

<!-- 原书 p.ii ｜ PDF p.2 -->

## Contents

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

<!-- 原书 p.ix ｜ PDF p.9 -->

## Preface

## Executive Summary

This document constitutes a "Snapshot" of the Technical Standard for SOSA™ (Sensor Open Systems Architecture) Reference Architecture, Edition 1.0 in support of United States Department of Defense (DoD) Command, Control, Communications, Computer, Intelligence, Surveillance, and Reconnaissance (C4ISR) development. The goal of The Open Group SOSA Consortium is to develop open architecture at the right level for Communications, Electro-Optical/Infra-Red (EO/IR), Electronic Warfare (EW), Radar, and Signals Intelligence (SIGINT). The SOSA Consortium strives to develop an ecosystem that allows interoperability, reuse, and faster delivery of products to market through vertical integration from cables, mechanical interfaces, hardware, software, and system designs.

## Background

Today's development of sensor systems typically entails a unique set of requirements and a single vendor. This form of development has served the military sensor community well; however, this stovepipe development process has had some undesired side-effects including long lead times, cumbersome improvement processes, lack of hardware, software, and system reuse between various sensors and platforms that result in platform-unique designs that are locked to a single deployed platform.

As the complexity of sensor and mission equipment has increased, this has resulted in increased cost and development times, and impeded the ability to integrate new hardware, software, or entire payloads into deployable platform systems. This — combined with the extensive testing and airworthiness/ground/sea/space qualification requirements — has begun to affect the ability of the military sensor community to rapidly deploy new capabilities across the military fleet.

The current C4ISR community procurement system does not promote the process of hardware; software, and payload reuse. Furthermore, the sensors development community has not created standards that facilitate the reuse of components.

Part of the reason for this is the relatively small size of the military market. Another contributing factor is the difficulty of developing qualified sensors payloads. An additional problem is the inability to use current commercial standards because they do not adhere to the stringent safety requirements intended to reduce risk and the likelihood of loss of host platform, reduced mission capability, and ultimately loss of life.

To counter these trends, the Air Force, Army, and Navy, enabled by the expertise and experience of the defense industrial base, are promoting a new approach.

## Approach

The SOSA initiative, formed as a Consortium of The Open Group, addresses the challenges of rapid, affordable capability evolution for today's military community. Part of the SOSA approach is to develop an Open Systems Architecture (OSA), captured in the SOSA Technical

<!-- 原书 p.x ｜ PDF p.10 -->

Standard that addresses software, hardware, and interfaces. This OSA is designed to promote portability and create product families across the Communications, EO/IR, EW, Radar, and SIGINT community. The SOSA Technical Standard is intended to promote the development of reusable sensor components applicable to a broad class of sensors and host platforms.

Another aspect of the SOSA approach is to develop an Open Business Model that addresses the needs of the acquisition community and ensures a strong industrial base. It includes business processes to adapt the procurement to a Modular Open Systems Approach (MOSA) reality, protect industry Intellectual Property (IP), and incentivize industry to invest in broadly applicable technologies that can be applied to a wide variety of sensors.

The SOSA approach allows "capabilities" to be developed as components that are exposed to other components through well-defined interfaces. It also provides for the reuse of SOSA module functionality across different environments. A SOSA module will have a core set of mandatory functionality, but different variants may be developed over time and different systems may have different additional characteristics (e.g., special environmental conditions, higher throughput, higher reliability, etc). These variants will be considered for incorporation into later editions of the SOSA Technical Standard. The SOSA Technical Standard does not guarantee compliance with any safety certification standard, but instead provides all the necessary capabilities to achieve that in the implementation phase by the vendors.

Ultimately, the SOSA Consortium key objectives are to reduce development, integration costs, and time to field sensor capabilities, and promote affordable capability evolution.

The Open Group

The Open Group is a global consortium that enables the achievement of business objectives through technology standards. Our diverse membership of more than 600 organizations includes customers, systems and solutions suppliers, tools vendors, integrators, academics, and consultants across multiple industries.

The mission of The Open Group is to drive the creation of Boundaryless Information Flow™ achieved by:

Working with customers to capture, understand, and address current and emerging requirements, establish policies, and share best practices Working with suppliers, consortia, and standards bodies to develop consensus and facilitate interoperability, to evolve and integrate specifications and open source technologies Offering a comprehensive set of services to enhance the operational efficiency of consortia Developing and operating the industry's premier certification service and encouraging procurement of certified products Further information on The Open Group is available at www.opengroup.org.

The Open Group publishes a wide range of technical documentation, most of which is focused on development of Standards and Guides, but which also includes white papers, technical studies, certification and testing documentation, and business titles. Full details and a catalog are available at www.opengroup.org/library.

<!-- 原书 p.xi ｜ PDF p.11 -->

## This Document

This document is a Snapshot of what will, after maturation, become the Technical Standard for SOSA™ (Sensor Open Systems Architecture) Reference Architecture, Edition 1.0. This document is developed and maintained by the SOSA Consortium.

<!-- 原书 p.xii ｜ PDF p.12 -->

## Trademarks

ArchiMate®, DirecNet®, Making Standards Work®, Open O® logo, Open O and Check® Certification logo, OpenPegasus®, Platform 3.0®, The Open Group®, TOGAF®, UNIX®, UNIXWARE®, and the Open Brand X® logo are registered trademarks and Boundaryless Information Flow™, Build with Integrity Buy with Confidence™, Dependability Through Assuredness™, Digital Practitioner Body of Knowledge™, DPBoK™, EMMM™, FACE™, the FACE™ logo, IT4IT™, the IT4IT™ logo, O-DEF™, O-HERA™, O-PAS™, Open FAIR™, Open Platform 3.0™, Open Process Automation™, Open Subsurface Data Universe™, Open Trusted Technology Provider™, Sensor Integration Simplified™, SOSA™, and the SOSA™ logo are trademarks of The Open Group.

Excel® and Microsoft® are registered trademarks of Microsoft Corporation in the United States and/or other countries.

Java® is a registered trademark of Oracle and/or its affiliates.

OpenVPX™ and VITA™ are trademarks of VITA in the United States and other countries.

POSIX® is a registered trademark of the Institute of Electrical and Electronic Engineers, Inc.

Python™ is a trademark of the Python Software Foundation.

SAE™ is a trademark of SAE International.

UML® is a registered trademark and Data Distribution Service™, DDS™, and Unified Modeling Language™ are trademarks of Object Management Group, Inc. in the United States and/or other countries.

All other brands, company, and product names are used for identification purposes only and may be trademarks that are the sole property of their respective owners.

<!-- 原书 p.xiii ｜ PDF p.13 -->

## Acknowledgements

The Open Group gratefully acknowledges the contribution of the following people in the development of this Snapshot:

Principal Authors

Rusty Baldwin, Riverside Research, (former member of the) Software WG Gerry Bezenek, Northrop Grumman, Hardware WG Nathan Binkley, KeyW Corporation, Electrical Mechanical WG Jeffrey Bryant, BAE, Vice-Chair Steering Committee Paul Clarke, NGC, Vice-Chair Architecture WG Charles Patrick Collier, Harris, Chair Hardware WG

George Dalton, KeyW, Vice-Chair Electrical Mechanical WG Steve Davidson, Raytheon Company, Chair Architecture WG Jason Dirner, CERDEC, Vice-Chair Hardware WG Scott Hinnershitz, Lockheed Martin, Hardware WG Tim Ibrahim, L-3 Technologies, Chair Electrical Mechanical WG David Linden, Leidos, Electrical Mechanical WG Michael Moore, Aspen Consulting Group, Architecture WG, Vice-Chair Software WG Michael Orlovsky, Lockheed Martin Fire and Missiles, Chair Software WG Shawn Reese, General Dynamics – MS, Architecture/Software WG Lee Riddle, Georgia Tech Research Institute, Hardware WG Greg Rocco, MIT Lincoln Laboratory, Hardware WG Ned Saunders, CEREC, Architecture/Software WG Trent Styrcula, CERDEC, Hardware WG Dan Toohey, Mercury, Hardware WG John Topping, Leidos, Electrical Mechanical WG

Additional Contributors

John Bowling, USAF, Chair Business WG

<!-- 原书 p.xiv ｜ PDF p.14 -->

Robert Guessferd, BAE, former Vice-Chair Business WG Donald F. Herrick, formerly Raytheon Company, former Chair Business WG Jason Jundt, GE Aviation, Vice-Chair Business WG

Ilya Lipkin, USAF, Chair Steering Committee

Funding for the SOSA Consortium and its work products comes from its member organizations, which are listed at https://www.opengroup.org/sosa/members.

And Naval Air System Command (NAVAIR) under NAVAIR Cooperative Agreement No. N00421-12-2-0004. The US not withstanding any copyright notation thereon. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of the Naval Air Warfare Center Aircraft Division or the US Government.

<!-- 原书 p.xv ｜ PDF p.15 -->

## Referenced Documents

Order of Precedence

In the event of a conflict between the text of this document and the references cited herein, the text of this document takes precedence. Nothing in this document, however, supersedes applicable laws and regulations unless a specific exemption has been obtained.

Normative References

Normative references for the SOSA Technical Standard are defined in Section 1.4.

Informative References

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