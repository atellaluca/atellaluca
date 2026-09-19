---
title: "HumaxGuardian — Guarded firmware acquisition and boot investigation"
description: "Case study: investigation of an undocumented DVB‑T set‑top box, the experimental method and the design of HumaxGuardian — an ESP32-based guardian used to safely observe and acquire SPI firmware images."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "HumaxGuardian architecture"
schema_type: "SoftwareSourceCode"
---

# HumaxGuardian — guarded firmware acquisition and boot investigation

**Type:** Open-source toolchain & case study  
**Role:** Investigator, designer, implementer  
**Period:** 2022  
**Domain:** Embedded systems, firmware acquisition, reverse engineering, automation  
**Repository:** [HumaxGuardian on GitHub — guardian firmware and host tooling](https://github.com/atellaluca/humax-mstar-guardian)

---

## Overview

This case study explains how an engineering-first, evidence-driven approach was used to investigate an undocumented DVB‑T set‑top box, control its boot process and produce a verified firmware image for offline analysis. The resulting tooling — HumaxGuardian — was created as a consequence of the constraints discovered during the investigation and is published as an open-source companion to this case study.

The emphasis here is on the method: observe → hypothesize → test → verify → automate → analyze offline. The narrative highlights what was observed on the hardware, how experiments were constrained to reduce risk, and how a small embedded guardian was designed to enforce safety policies during live interaction.

## 1. The challenge

Observed: a consumer DVB‑T decoder (Humax/Changhong, MStar platform) with little or no public documentation. The goal was to obtain a verified copy of the SPI flash and to reason about the boot process without risking irreversible changes to the device.

Key constraints that shaped the work:

- limited visibility into the platform and bootloader  
- need for repeatable, low‑risk experiments  
- requirement to stop live manipulation once an offline image was available

## 2. Finding a way in

Observed: a UART header exposed on the motherboard. The interface ran at `115200 8N1`.

Initial bridge wiring (observed):

- Target TX → ESP32 GPIO16  
- Target RX ← ESP32 GPIO17  
- common GND  

An ESP32‑WROOM‑32 module was used as a USB‑serial bridge to the host computer; a relay controlled by the ESP32 allowed deterministic power cycles and cold boots.

## 3. A zero‑delay bootloader

Observed: the bootloader (a MStar-derived MBoot/U‑Boot build) prints boot messages with `bootdelay=0` configured.

Observed (UART excerpt):

```
bootdelay=0
```

Observed: a `Changelist` marker in the bootlog correlated with a narrow timing window. Experimentally, sending a single carriage return (`0x0D`) at that moment produced an interactive prompt on the observed build.

Verified: prompt received in that specific build — `k5tn#` — allowed interaction with MBoot.

Note: this is an experimental observation on the analysed build. It is not presented as a general exploit; it was discovered and used under controlled conditions.

## 4. Building a guardian instead of a bridge

As interaction with MBoot grew more powerful, the risk of accidental destructive commands (for example SPI erase/write) increased.

Design decision: transform the ESP32 from a passive bridge into an active guardian enforcing policy at the hardware boundary. This architectural choice baked safety into the system rather than treating it as an afterthought.

Architecture (conceptual):

![HumaxGuardian pipeline](../../assets/visuals/humax-guardian-pipeline.svg)

Trust boundary summary (Verified by design):

- `Host Python` ↔ `ESP32 policy boundary` ↔ `Target UART`  
- The ESP32 enforces `deny-by-default`, a command allowlist, timed injection of the interrupting CR, local boot event detection, relay-based power control and logging.  
- The host cannot convert the guardian into a transparent MBoot console merely by changing the client — the policy is enforced on the ESP32.

Security properties enforced by architecture (Observed / Verified):

- Deny‑by‑default command handling (Verified).  
- No SPI erase/write operations performed by public tooling (Verified).  
- The pipeline writes to external USB storage (`fatwrite`) — this writes the acquired image to USB, not to the target SPI (Observed & Verified).  
- Important property: the target SPI remained unmodified during acquisition (Verified).

## 5. From SPI to a verified image

Observed in bootlog: boot command reading SPI into DRAM and invoking LZMA decompression:

```
spi_rdc 0x82B00000 0x00120000 0x4e0000;
LzmaDec 0x82B00000 0x4e0000 0x80000180 0x82500000;
go 0x80000224;
```

Interpretation: the application is read from SPI at offset `0x120000` (observed). In the dumped image an LZMA stream was present at the same offset and decompresses to the embedded application (Verified by offline decompression).

Acquisition pipeline (Observed → Verified):

SPI NOR → DRAM (via MBoot primitive) → CRC32 check → USB/FAT write → `firmware.bin` → re‑read into RAM → CRC32 check → offline analysis

Image integrity checks performed (Verified):

- CRC32 of the SPI-loaded RAM image: `89BFAD81`  
- SHA‑256 of the final master image: `de7b98ffea94c77f15e12c8e644d52586ba6dff24c5ae3f08108f9f1ed252e64`

```
CRC32 ... ==> 89BFAD81
SHA256 ... ==> de7b98ffea94c77f15e12c8e644d52586ba6dff24c5ae3f08108f9f1ed252e64
```

Guiding rule: once a verified master image existed, live experimentation was stopped and the rest of the work moved offline.

## 6. Moving the investigation offline

Principle: minimise live interaction once an offline artifact is available. Offline analysis reduces risk and enables deeper, repeatable investigation without placing the target at risk.

## 7. Reconstructing the flash

Offline analysis identified a plausible flash map inside the 8 MiB SPI image. The offsets below are reconstructed from observed evidence and offline interpretation; where appropriate the writeup marks interpretations that are not fully proven.

![Flash map](../../assets/visuals/humax-guardian-flashmap.svg)

Key regions (approximate/observed):

- `0x000000` — Bootloader / MBoot (Observed)  
- `0x100000` — Loader Info A (Observed)  
- `0x110000` — Loader Info B (Observed)  
- `0x120000` — Compressed application (LZMA) (Observed & Verified by decompression)  
- `0x600000` — OSD / graphical resources (Observed)  
- `0x700000` — persistent / configuration area (Observed, partially classified)  
- `0x710000–0x75FFFF` — Database A (Observed)  
- `0x760000–0x7AFFFF` — Database B (Observed)  
- `0x7B0000` — mostly erased (Observed)  
- `0x7C0000` — System Info A (Observed)  
- `0x7D0000` — System Info B (Observed)  
- `0x7E0000` — Environment A (Observed)  
- `0x7F0000` — Environment B (Observed)  
- `0x800000` — end (Observed)

Duplication and redundancy (Inferred / Observed): pairs such as Loader Info A/B, Database A/B, System Info A/B and Environment A/B are present and were identical in the acquired image. This suggests redundancy by design; the interpretation of internal formats remains partial and is presented as an evidence‑led inference, not a full decode.

## 8. What this project demonstrates

This investigation highlights a methodical engineering approach to hardware‑adjacent reverse engineering where the primary artefact of value is the engineering method rather than a single technical trick.

Storyline captured by the workflow:

- board inspection → UART discovery  
- observation of boot behaviour → narrow injection window  
- design of an embedded guardian enforcing policy at the hardware boundary  
- verified readout of SPI → offline verification and analysis  

Skills and domains that naturally emerge from the narrative: embedded systems, serial communication, ESP32 firmware, automation, binary acquisition, offline decompression and analysis, and careful safety‑first engineering. These are shown through the sequence of decisions and verifications rather than as a checklist.

## Explore the code

Explore HumaxGuardian on GitHub — the repository contains the ESP32 guardian firmware, Python host tooling and architecture/protocol documentation. The repository does not contain proprietary device firmware.

[Explore HumaxGuardian on GitHub](https://github.com/atellaluca/humax-mstar-guardian)

---

## Read next

- [Back to case studies](../index.md)
