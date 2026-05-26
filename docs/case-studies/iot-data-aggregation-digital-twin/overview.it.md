---
title: "Architettura IoT Data Aggregation | Digital Twin Edge-to-Cloud"
description: "Caso studio di Luca Atella per IoT data aggregation e Digital Twin architecture: acquisizione edge, gateway, GraphQL API, microfrontend e layer di storage."
image: "assets/images/case-studies/iot-data-aggregation-digital-twin/iot-data-aggregation-digital-twin-edge-cloud-architecture.png"
image_alt: "Diagramma edge-to-cloud IoT data aggregation e Digital Twin architecture"
schema_type: "TechArticle"
---

# IoT Data Aggregation Architecture per Digital Twin

## Panoramica

Questo caso studio descrive un’architettura edge-to-cloud per acquisire, normalizzare e aggregare dati IoT eterogenei in scenari Digital Twin.

L’obiettivo è rendere osservabili e utilizzabili dati provenienti da sensori, videocamere, dispositivi e gateway, mantenendo separati acquisizione, ingestion, API, storage e visualizzazione.

![Architettura edge-to-cloud per IoT data aggregation e Digital Twin con sensori, gateway, ingestion, GraphQL API, microfrontend e layer di storage](../../assets/images/case-studies/iot-data-aggregation-digital-twin/iot-data-aggregation-digital-twin-edge-cloud-architecture.png)

---

## Componenti Principali

- acquisizione edge da sensori, camere e dispositivi
- comunicazione BLE/Zigbee mesh e gateway
- layer di ingestion per dati real-time, GeoJSON e domain-specific
- GraphQL API
- layer applicativi specifici per tipologia di dato
- microfrontends
- storage gateway
- elaborazione assistita da AI

---

## Decisioni Architetturali

L’architettura separa le responsabilità per evitare che dispositivi, protocolli e storage influenzino direttamente il modello applicativo.

I gateway raccolgono e normalizzano il dato, il layer di ingestion gestisce validazione e routing, mentre API e microfrontend consumano dati già stabilizzati.

---

## Cosa Dimostra

- integrazione edge/cloud
- sistemi IoT eterogenei
- data aggregation per Digital Twin
- separazione tra acquisizione, ingestion e presentazione
- architetture pronte per evolvere con nuove sorgenti dati
