---
title: "Casi Studio | Backend Architecture, AWS, IoT e Runtime Validation"
description: "Casi studio di Luca Atella su cloud-portable backend architecture, AWS serverless deployment, FastAPI, runtime contract validation, sistemi IoT e pipeline geospaziali."
image: "assets/images/case-studies/cloud-portable-fleet-platform/cloud-portable-fleet-management-platform-aws-fastapi-architecture.png"
image_alt: "Casi studio backend architecture e AWS di Luca Atella"
schema_type: "CollectionPage"
---

# Casi Studio

Questa sezione raccoglie progetti e casi studio architetturali.

Ogni pagina spiega il problema, la forma del sistema, le decisioni tecniche principali e perché quelle decisioni contano nella pratica.

---

## Cloud-Portable Fleet Management Platform

Piattaforma per gestione veicoli, prenotazioni, viaggi, rifornimenti, manutenzioni, documenti e report. È stata adottata in un contesto reale ed è stata progettata per girare localmente con Docker o in produzione su AWS.

- Focus: cloud portability, astrazione infrastrutturale, deployment in produzione
- Topics: AWS, FastAPI, React, DynamoDB, S3, Docker Compose, CloudFormation

→ [Leggi il caso studio](cloud-portable-fleet-platform/overview.md)

## ImportSpy

Progetto open-source Python per runtime contract validation di moduli e sistemi plugin-based.

- Focus: runtime contracts, sicurezza modulare, invarianti architetturali
- Topics: plugin governance, errori deterministici, modelli di validazione

→ [Leggi il caso studio](importspy/overview.md)

## B3DO

Pipeline geospaziale per trasformare dataset pubblici di Basilicata in modelli 3D del terreno.

- Focus: geospatial data processing, generazione di modelli 3D, pipeline riproducibili
- Topics: GDAL, Rasterio, NumPy, PyVista, Fiona, Typer

→ [Leggi il caso studio](b3do/overview.md)

## Unified Backend Architecture

Architettura backend plugin-driven per gestire dispositivi IoT eterogenei dietro un modello dati e una superficie API unificata.

→ [Leggi il caso studio](unified-backend/overview.md)

## IoT Data Aggregation Architecture

Architettura edge-to-cloud per raccogliere dati IoT eterogenei e renderli utilizzabili in sistemi Digital Twin.

→ [Leggi il caso studio](iot-data-aggregation-digital-twin/overview.md)

## Fleet Tracking Platform

Backend per ingestione real-time di telemetria GPS e CAN bus, con monitoraggio fleet, analytics e workflow operativi.

→ [Leggi il caso studio](fleet-tracking/overview.md)
