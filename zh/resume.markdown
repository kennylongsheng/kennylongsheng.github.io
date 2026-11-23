---
layout: page
title: 履歷
lang: zh-Hant
translation_key: resume
permalink: /zh-tw/resume/
description: Lee Long Sheng 的 DRAM 控制器韌體與驗證經歷。下載韌體履歷、驗證履歷或完整專業 CV。
---

我是韌體工程師，專注於 SSD 控制器內的 DRAM 子系統韌體與驗證。工作結合裸機 C 初始化及訓練韌體開發、時序與電壓特性分析、Python 分析工具，以及 SSD 客戶退回品的問題調查。

{% include resume-downloads.html %}

## 工作經歷 {#experience}

<div class="experience-heading">
  <h3 id="phison-electronics-corp">群聯電子（Phison Electronics Corp.）</h3>
  <p class="experience-location">台灣新竹</p>
  <p class="experience-role"><strong>資深韌體工程師</strong> <span class="experience-dates">2024 年 11 月至 2026 年 8 月</span></p>
  <p class="experience-role"><strong>韌體工程師</strong> <span class="experience-dates">2021 年 3 月至 2024 年 10 月</span></p>
</div>

- 透過二維 delay/Vref 掃描與手動調校分析 DRAM 時序與電壓裕量，並以示波器波形分析進一步除錯。
- 與數位及類比設計工程師協作開發 DRAM 介面訓練演算法，並以裸機 C 實作 DDR4、LPDDR4 與 LPDDR5 的初始化及訓練韌體。
- 針對 SSD 客戶退回品重現失效問題並分析根本原因；在適用情況下，實作與驗證韌體修正。
- 建立 Python 工具，解析日誌、解碼暫存器傾印資料、比對通過與失敗的測試結果，並擷取 DRAM 訓練設定。
- 調查 DRAM 介面失效問題時，依相關 JEDEC 要求檢視 PCB 佈局，並將分析結果提供給硬體設計工程師。
- 開發初始化階段的訓練韌體，以因應同一控制器設計下不同晶片個體的差異，並與 SSD 韌體團隊共同改進訓練演算法。
- 審查韌體程式碼與測試計畫，並為新進工程師提供技術指導。

## 技術專長 {#technical-background}

- **韌體：** C、Python、ARM Cortex 與裸機韌體。
- **DRAM：** 具備 DDR4、LPDDR4、LPDDR5 初始化與訓練的實作經驗；DDR5 僅限規範研讀。
- **特性分析：** 二維 delay/Vref 掃描、時序對齊、Vref 調校與初始化階段校準。
- **除錯：** 搭配 Eclipse 使用 In-Circuit Emulator（ICE）probe 存取暫存器；UART 日誌；以 Python 分析日誌、暫存器傾印資料及通過與失敗的測試結果；Git；各通道的示波器波形分析。

## 學歷 {#education-projects}

### 國立交通大學

<p class="education-degree">資訊工程學士 · 2016–2021 年 · 台灣</p>

**[擴增實境魔術方塊解題引導（Rubik's Cube Solving Guides with AR）]({{ '/blog/rubiks-cube-solving-guides-with-ar/' | relative_url }})** · 畢業專題，與一位組員共同開發。文章為英文。

探索以影像輸入魔術方塊狀態、透過深度強化學習選擇轉動步驟，並以擴增實境提供解題引導。相較於傳統解題演算法，硬體需求與訓練時間限制了此方法的實用性。

## 社團幹部與活動 {#activities}

- **國立交通大學馬來西亞同學會會長** · 2018 年 6 月至 2019 年 6 月。與校內各單位協調學生支援事務，並透過 Facebook Messenger 維護馬來西亞學生聯絡名錄。
- **國立交通大學單車社活動負責人** · 2016 年 6 月至 2017 年 6 月。與國立清華大學共同籌辦新生週單車活動。

## 語言能力 {#languages}

中文：母語 · 英文：專業工作能力 · 馬來文：有限工作能力。

## 聯絡方式 {#contact}

[電子郵件](mailto:{{ site.email }}) · [LinkedIn](https://www.linkedin.com/in/kennylongsheng/) · [GitHub](https://github.com/{{ site.github_username }})
