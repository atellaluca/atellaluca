---
title: "Casi Studio Tecnici - Luca Atella"
description: "Casi studio tecnici su architetture backend cloud-portable, runtime governance, AWS, IoT, Digital Twin e pipeline geospaziali."
image: "assets/images/case-studies/cloud-portable-fleet-platform/cloud-portable-fleet-management-platform-aws-fastapi-architecture.png"
image_alt: "Casi studio backend architecture e AWS di Luca Atella"
schema_type: "CollectionPage"
---

# Casi Studio

Questa sezione raccoglie progetti e casi studio architetturali.

Ogni pagina spiega il problema, la forma del sistema, le decisioni tecniche principali e perché quelle decisioni contano nella pratica.

Usala come livello di evidenza tecnica del portfolio: ogni pagina collega un problema tecnico a confini architetturali, decisioni runtime e trade-off implementativi.

---

## Cloud-Portable Fleet Management Platform

Fleet Management System in uso presso Studio Lambda per gestire il turnover dei veicoli di 50 dipendenti. È deployato su AWS e progettato per separare logica applicativa, persistenza, servizi cloud e runtime web.

- Focus: cloud portability, astrazione infrastrutturale, deployment in produzione
- Topics: AWS, FastAPI, React, DynamoDB, S3, Docker Compose, CloudFormation

→ [Leggi il caso studio](cloud-portable-fleet-platform/index.md)

## ImportSpy

Progetto open-source Python per runtime contract validation di moduli e sistemi plugin-based.

- Focus: runtime contracts, sicurezza modulare, invarianti architetturali
- Topics: plugin governance, errori deterministici, modelli di validazione

→ [Leggi il caso studio](importspy/index.md)

## B3DO

Pipeline geospaziale per trasformare dataset pubblici di Basilicata in modelli 3D del terreno.

- Focus: geospatial data processing, generazione di modelli 3D, pipeline riproducibili
- Topics: GDAL, Rasterio, NumPy, PyVista, Fiona, Typer

→ [Leggi il caso studio](b3do/index.md)

## Unified Backend Architecture

Framework backend plugin-driven che ho sviluppato in Vemar e su cui si fonda delis.app, presentato in forma SAFE per evidenziare separazione delle integrazioni, contratti e superficie API unificata.

→ [Leggi il caso studio](unified-backend/index.md)

## Compatibilità e isolamento dei runtime per gli applicativi Agenzia delle Entrate

Intervento presso uno studio commercialista per mantenere utilizzabili applicativi fiscali di annualità diverse, isolando runtime Java, modalità JNLP/LaunchAnywhere e requisiti Desktop Telematico/Entratel.

- Focus: diagnosi legacy, isolamento dipendenze, continuità operativa
- Topics: Windows, Java runtime, JNLP, LaunchAnywhere, Entratel, truststore

→ [Leggi il caso studio](agenzia-entrate-runtime-isolation/index.md)

## IoT Data Aggregation Architecture

Architettura edge-to-cloud per raccogliere dati IoT eterogenei e renderli utilizzabili in sistemi Digital Twin.

→ [Leggi il caso studio](iot-data-aggregation-digital-twin/index.md)

## Fleet Tracking Platform

Backend di telemetria real-time distinto dal progetto Studio Lambda: infrastruttura per 80 tracker progettata e realizzata personalmente in Vemar, con socket, dati CAN bus, persistenza e API REST.

→ [Leggi il caso studio](fleet-tracking/index.md)

## HumaxGuardian

Un'indagine di reverse engineering embedded del 2026: policy dei comandi su ESP32, interazione controllata con MBoot, acquisizione verificata di 8 MiB di SPI e analisi offline della flash.

- Focus: interazione sicura con il dispositivo, integrità dell'acquisizione, analisi basata su evidenze
- Topics: ESP32, UART, MStar MBoot, strumenti Python, SPI NOR, LZMA

→ [Leggi il caso studio HumaxGuardian](humax-guardian/index.md)
