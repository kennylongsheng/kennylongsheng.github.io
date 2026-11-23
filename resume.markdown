---
layout: page
title: Resume
lang: en
translation_key: resume
permalink: /resume/
description: Lee Long Sheng's DRAM controller firmware and validation experience. Download firmware and validation resumes or the full professional CV.
---

Firmware engineer specializing in DRAM subsystem firmware and validation within SSD controllers. My work combines bare-metal C initialization and training firmware with timing/voltage characterization, Python-based analysis, and SSD customer-return investigation.

{% include resume-downloads.html %}

## Experience {#experience}

<div class="experience-heading">
  <h3 id="phison-electronics-corp">Phison Electronics Corp.</h3>
  <p class="experience-location">Hsinchu, Taiwan</p>
  <p class="experience-role"><strong>Senior Firmware Engineer</strong> <span class="experience-dates">Nov 2024–Aug 2026</span></p>
  <p class="experience-role"><strong>Firmware Engineer</strong> <span class="experience-dates">Mar 2021–Oct 2024</span></p>
</div>

- Characterized DRAM timing and voltage margins through two-dimensional delay/Vref sweeps and manual tuning, using per-channel oscilloscope waveform analysis for deeper debugging.
- Collaborated with digital and analog designers on DRAM interface-training algorithms and implemented bare-metal C initialization and training firmware for DDR4, LPDDR4, and LPDDR5.
- Investigated SSD customer-return failures through reproduction and root-cause analysis; implemented and validated firmware fixes where appropriate.
- Built Python tools to parse logs, decode register dumps, compare pass/fail results, and extract DRAM training settings.
- Reviewed PCB layouts against relevant JEDEC requirements during DRAM interface failure investigations and provided findings to hardware designers.
- Developed initialization-time training for chip-to-chip variation within a controller design, refining training algorithms with SSD firmware teams.
- Reviewed firmware code and test plans, and supported new engineers with technical guidance.

## Technical focus {#technical-background}

- **Firmware:** C, Python, ARM Cortex, and bare-metal firmware.
- **DRAM:** Hands-on DDR4, LPDDR4, LPDDR5 initialization and training; DDR5 specification study only.
- **Characterization:** Two-dimensional delay/Vref sweeps, timing alignment, Vref tuning, and initialization-time calibration.
- **Debugging:** In-Circuit Emulator (ICE) probe with Eclipse for register access; UART logging; Python log, register-dump and pass/fail analysis; Git; per-channel oscilloscope waveform analysis.

## Education {#education-projects}

### National Chiao Tung University

<p class="education-degree">Bachelor of Computer Science · 2016–2021 · Taiwan</p>

**[Rubik's Cube Solving Guides with AR]({{ '/blog/rubiks-cube-solving-guides-with-ar/' | relative_url }})** · Final-year project, developed with a teammate.

Explored image-based cube-state input, deep reinforcement learning for move selection, and augmented reality solution guidance. Hardware requirements and training time limited its practicality compared with conventional solving algorithms.

## Leadership & activities {#activities}

- **President, NCTU Malaysian Students Association** · June 2018–June 2019. Coordinated student-support matters with university departments and maintained a Malaysian-student contact directory using Facebook Messenger.
- **Activity Coordinator, NCTU Cycling Club** · June 2016–June 2017. Co-organized a freshman-week cycling event with National Tsing Hua University.

## Languages {#languages}

Chinese: Native · English: Professional working proficiency · Malay: Limited working proficiency.

## Contact {#contact}

[Email](mailto:{{ site.email }}) · [LinkedIn](https://www.linkedin.com/in/kennylongsheng/) · [GitHub](https://github.com/{{ site.github_username }})
