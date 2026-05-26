---
title: "Architettura IoT Data Aggregation | Digital Twin Edge-to-Cloud"
description: "Caso studio di Luca Atella per IoT data aggregation e Digital Twin architecture: edge acquisition, gateway, GraphQL API, microfrontends e storage layers."
image: "assets/images/case-studies/iot-data-aggregation-digital-twin/iot-data-aggregation-digital-twin-edge-cloud-architecture.png"
image_alt: "Diagramma edge-to-cloud IoT data aggregation e Digital Twin architecture"
schema_type: "TechArticle"
---

# IoT Data Aggregation Architecture per Digital Twin

## Overview

Questo caso studio descrive un’architettura edge-to-cloud per acquisire, normalizzare e aggregare dati IoT eterogenei in scenari Digital Twin.

L’obiettivo è rendere osservabili e utilizzabili dati provenienti da sensori, videocamere, dispositivi e gateway, mantenendo separati acquisition, ingestion, API, storage e visualizzazione.

![Architettura edge-to-cloud per IoT data aggregation e Digital Twin con sensori, gateway, ingestion, GraphQL API, microfrontends e storage layers](../../assets/images/case-studies/iot-data-aggregation-digital-twin/iot-data-aggregation-digital-twin-edge-cloud-architecture.png)

---

## Componenti Principali

- edge acquisition da sensori, camere e dispositivi
- comunicazione BLE/Zigbee mesh e gateway
- ingestion layer per dati real-time, GeoJSON e domain-specific
- GraphQL API
- data-specific application layers
- microfrontends
- storage gateway
- AI-assisted processing

---

## Decisioni Architetturali

L’architettura separa le responsabilità per evitare che dispositivi, protocolli e storage influenzino direttamente il modello applicativo.

I gateway raccolgono e normalizzano il dato, l’ingestion layer gestisce validazione e routing, mentre API e microfrontends consumano dati già stabilizzati.

---

## Cosa Dimostra

- edge/cloud integration
- sistemi IoT eterogenei
- data aggregation per Digital Twin
- separazione tra acquisition, ingestion e presentation
- architetture pronte per evolvere con nuove sorgenti dati
