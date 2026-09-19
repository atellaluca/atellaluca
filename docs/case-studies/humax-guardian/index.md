---
title: "HumaxGuardian | Embedded Reverse Engineering & Firmware Analysis"
description: "A 2026 case study by Luca Atella: from an undocumented MStar UART to ESP32 command policy, verified SPI acquisition and offline firmware analysis."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "Luca Atella — embedded reverse engineering and firmware analysis"
schema_type: "TechArticle"
date: "2026-09-19"
---

<p class="portfolio-eyebrow">2026 / EMBEDDED REVERSE ENGINEERING · FIRMWARE ANALYSIS</p>

# HumaxGuardian

<p class="portfolio-lead">From an undocumented UART to a verified firmware image.</p>

A controlled reverse-engineering workflow for an MStar-based embedded system, combining an ESP32 policy boundary, MBoot interaction, verified SPI acquisition and offline firmware analysis.

**Type:** Case Study / Open Source Tooling<br>
**Role:** Independent Research & Engineering<br>
**Period:** 2026<br>
**Domain:** Embedded Systems · Firmware · Reverse Engineering<br>
**Repository:** [HumaxGuardian on GitHub](https://github.com/atellaluca/humax-mstar-guardian)

---

## The challenge

The starting point was a Humax/Changhong DVB-T receiver built around an undocumented MStar platform. I wanted to understand how it booted and acquire a verifiable representation of its firmware while keeping the target SPI unmodified.

Board markings and boot output progressively identified the system: **MStar MSD3T273 / MSA3T273Z-Z00-DA0E**, **U-Boot 2011.06 / custom MStar MBoot**, with an internal MBoot build dated **Apr 27 2020**. Application evidence later pointed to a **CH_RTOS / eCos-related environment**. This was not a conventional Linux system: the investigation had to follow the interfaces and structures actually present.

The first problem was therefore visibility. Each experiment needed to answer a limited question, preserve enough evidence to check the result and inform the next step. HumaxGuardian grew out of those constraints.

<div class="portfolio-proof" markdown>
**Reading the evidence**

*Observed* means obtained directly from the board, UART, bootloader or acquired dump. *Verified* means confirmed through an additional check. *Inferred* marks an interpretation supported by evidence whose meaning has not been fully demonstrated.
</div>

## Finding a way in

A UART connection exposed the boot sequence at **115200 baud, 8N1**. An **ESP32-WROOM-32** sat between the target and the host computer, providing a place to observe serial events and control power locally.

| Connection | Research setup |
| --- | --- |
| Humax TX → ESP32 RX2 | `GPIO16` |
| Humax RX ← ESP32 TX2 | `GPIO17` |
| Ground | Common GND |
| ESP32 USB serial → host | `921600` baud |
| Relay control | `GPIO25`, active LOW; switches target `+12 V` |

The relay made cold-boot experiments repeatable. Power cycling and UART observation could be coordinated by the ESP32 instead of depending on the timing of a manual power connection or a host-side serial round trip.

## A zero-delay bootloader

The observed configuration contained `bootdelay=0`. There was effectively no ordinary interactive autoboot window, so manually typing into the console did not provide a dependable way to stop booting.

Repeated cold boots exposed a useful timing marker in the UART output: `Changelist`. On the tested MBoot build, sending **one carriage return (`0x0D`)** when that marker appeared interrupted autoboot and produced the prompt `k5tn#`.

The ESP32 detected the marker locally and injected the CR before forwarding telemetry to the host. Prompt recognition then disarmed the interception. This describes experimentally observed behavior on that specific build; it is not a claim of a general bootloader exploit.

## From bridge to guardian

The initial serial bridge solved access. Once a bootloader console was available, however, a transparent path from operator input to MBoot also exposed powerful commands to typing mistakes and host-side errors. The next engineering decision was to move command policy into the ESP32.

<div class="portfolio-card-grid" markdown>
<div class="portfolio-proof" markdown>
**Transparent bridge**

Host ↔ UART ↔ Target

Operator input reaches the bootloader through a forwarding path.
</div>
<div class="portfolio-proof" markdown>
**Guardian**

Host → ESP32 policy → Target

**Default: deny.** MBoot command strings must match the firmware allowlist exactly.
</div>
</div>

<figure class="case-study-visual" markdown>
![Target SPI and MBoot connect through UART to the ESP32 policy boundary, then to Python host tooling and offline analysis. MBoot exports the dump to external USB storage.](../../assets/visuals/humax-guardian-pipeline.svg){ width="380" height="844" loading="lazy" decoding="async" }
<figcaption>The ESP32 governs live commands. The acquisition data travels from target RAM to external USB storage through MBoot.</figcaption>
</figure>

**Safety by architecture:** the ESP32 is the command-policy authority. It controls target power, detects boot events, times the CR, recognizes the prompt, checks the exact allowlist and reports UART data and guardian events. Execution requests are rejected if the console is not ready or the command is absent from the allowlist.

The Python host provides the operator UI, text and raw logging, and lifecycle management. Changing the Python client alone does not permit arbitrary MBoot commands through the public guardian firmware.

Fail-safe behavior has a defined scope: the ESP32 initializes the relay with target power off; Python attempts to disarm interception and switch power off during cleanup, including handled serial errors and Ctrl+C. The public implementation does not provide a watchdog guarantee that a disconnected host will cause immediate power-off.

The command categories separate inspection, target-device reads, USB reads and USB writes. **No SPI erase/write operation is intentionally exposed by the public allowlist.** `fatwrite` writes to an external USB FAT filesystem, so the complete workflow is not read-only. **The target SPI remained unmodified during acquisition.**

## From SPI to a verified image

The target used a **W25Q64FV SPI NOR**: **8 MiB (`0x00800000` bytes)**, organized here as **128 sectors of 64 KiB (`0x10000` bytes)**. MBoot exposed a primitive that could copy the complete flash into RAM in one operation:

```text
spi rdc 0x81000000 0x00000000 0x00800000
```

A CRC32 over that RAM buffer returned `89BFAD81`. The next step exported the buffer to FAT storage connected to the target's USB port. An observed MBoot quirk mattered: **the destination file had to pre-exist** for the successful `fatwrite` workflow.

The allowlisted export was `fatwrite usb 0 0x81000000 firmware.bin 0x00800000`. The resulting `firmware.bin` contained **8,388,608 bytes**. To check the USB round trip, I reloaded it into a separate RAM region:

```text
fatload usb 0:1 0x82000000 firmware.bin
```

The CRC32 after reload was again `89BFAD81`. Offline, the verified master and its copy also produced the same SHA-256.

<div class="portfolio-proof" markdown>
**Acquisition verification**

- **SPI NOR:** 8 MiB
- **Dump size:** 8,388,608 bytes
- **CRC32, source RAM and USB reload:** `89BFAD81`

<p><strong>SHA-256, verified master and copy:</strong><br><code class="case-study-digest">de7b98ffea94c77f15e12c8e644d52586ba6dff24c5ae3f08108f9f1ed252e64</code></p>
</div>

Matching CRC32 values are strong evidence that the export and reload preserved the data, but they are not mathematical proof of byte-for-byte identity. Matching SHA-256 values provided the stronger offline integrity check used for the master/copy pair. Neither checksum establishes that the firmware itself is trustworthy or completely understood.

## Moving the investigation offline

Once the complete image had been acquired and checked, most questions no longer required a live console. Analysis moved to the verified copy, reducing interaction with the target and making each inspection repeatable without another boot cycle.

The observed boot command supplied a concrete hypothesis about the application layout:

```text
spi_rdc 0x82B00000 0x00120000 0x4e0000;
LzmaDec 0x82B00000 0x4e0000 0x80000180 0x82500000;
go 0x80000224;
```

The sequence indicated application data starting around SPI offset `0x120000`, followed by decompression and execution in RAM. **Verified:** a valid LZMA stream was found at that offset in the dump; offline decompression produced an application image of roughly **16.2 MB**. This connected the live boot behavior to a structure that could be examined independently.

The decompressed application contained `CHANGHONG Application R&d`, `Chip MSD3T273`, `CH_RTOS` and the internal firmware string **`Build Feb 24 2022`**. That last date belongs to the target firmware; **this research project is from 2026**.

Other evidence included `MXL608`, `DVB-T` / `DVB-T2`, `PVR`, `Wi-Fi`, `Ethernet` and `FTP`. The presence of related code and strings indicates material available for further analysis. It does not establish that Wi-Fi, FTP or every referenced feature was enabled in the commercial product.

## Reconstructing the flash

Boot parameters, decompression and inspection of the acquired bytes supported a working map of the 8 MiB image. It separated boot code, the compressed application, graphical resources and persistent data while leaving uncertain regions explicitly unclassified.

<figure class="case-study-visual" markdown>
![Vertical map of the full 8 MiB SPI, from MBoot at 0x000000 to the end at 0x800000, with application, resources, unclassified regions and four A/B pairs.](../../assets/visuals/humax-guardian-flashmap.svg){ width="380" height="1010" loading="lazy" decoding="async" }
<figcaption>A working map, with small records expanded for readability. Approximate boundaries and incomplete classifications remain explicit.</figcaption>
</figure>

| SPI offset / range | Working interpretation |
| --- | --- |
| `0x000000` | Bootloader / MBoot |
| Approximately `0x09xxxx` | Beginning of a mostly erased region; boundary approximate |
| `0x100000` / `0x110000` | Loader Info A / B |
| `0x120000` | CHANGHONG compressed application; valid LZMA stream |
| Around `0x600000` | Graphical / OSD resources, including `.gam` assets |
| Around `0x700000` | Persistent / configuration area, not completely classified |
| `0x710000–0x75FFFF` | Database A |
| `0x760000–0x7AFFFF` | Database B |
| `0x7B0000` | Mostly erased |
| `0x7C0000` / `0x7D0000` | System Info A / B |
| `0x7E0000` / `0x7F0000` | Environment A / B |
| `0x800000` | End of SPI |

This map is a basis for investigation, not a claim that every structure was reverse engineered. A recognizable region and a fully decoded data format are different results.

## Discovering redundancy

The persistent structures revealed four pairs: **Loader Info A/B, Database A/B, System Info A/B and Environment A/B**. The corresponding examined A/B pairs were identical in the acquired dump.

That comparison verifies duplication in this image. Redundancy is a supported interpretation of the layout, but the comparison alone does not establish update order, recovery behavior or which copy the running application would prefer after a failure.

Database identifiers included `xpdr0001`, `serv0001` and `tmer0001`. **Inferred:** these are consistent with transponder, service/channel and timer structures respectively. Their presence helped organize further analysis; the database format was not fully decoded.

## What the investigation produced

The result was a connected set of engineering artifacts:

- A repeatable cold-boot setup and an experimentally established way to reach the tested MBoot prompt.
- ESP32/C++ guardian firmware that enforces exact command policy locally, paired with Python tooling for operation, lifecycle and evidence logging.
- A complete 8 MiB acquisition, checked through the USB round trip and offline master/copy hashes.
- A decompressed application, a working flash map and confirmed duplicate pairs, with remaining interpretation limits recorded.
- Public source code and technical documentation describing the tooling and its target-specific constraints.

The sequence connected board-level observation to serial timing, bootloader behavior, embedded policy, acquisition integrity and binary analysis. Each layer supplied evidence for the next.

## Method

<div class="portfolio-proof" markdown>
**Observe → Hypothesize → Test → Verify → Automate → Analyze offline**
</div>

Observation supplied the timing marker; controlled tests established the intervention; the guardian encoded the operational constraints. Verification made it possible to move the investigation away from the live device and examine a stable representation.

The principle is transferable: build a model from evidence, encode the constraints in the tools, and **reduce interaction with the live target once a verified representation exists**.

<div class="portfolio-contact" markdown>

## Explore HumaxGuardian on GitHub

The repository contains ESP32 guardian firmware, Python host tooling and technical documentation for the architecture and protocol. User-authored code is MIT-licensed. **Proprietary device firmware and binary dumps are not distributed.**

[Explore HumaxGuardian on GitHub](https://github.com/atellaluca/humax-mstar-guardian){ .md-button .md-button--primary }

</div>

---

[Back to case studies](../index.md)
