---
title: "Architettura Fleet Telemetry | Backend Real-Time GPS e CAN Bus"
description: "Approfondimento architetturale per backend fleet telemetry real-time con GPS tracking, normalizzazione CAN bus, event-driven processing, API e comunicazione sicura."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "Architettura fleet telemetry backend GPS e CAN bus"
schema_type: "TechArticle"
---

# Architettura

Il sistema è un backend real-time per ingestire, normalizzare, validare ed esporre dati fleet provenienti da tracking device eterogenei.

---

## Pipeline

- device communication
- telemetry ingestion
- data normalization
- validation
- persistence
- API exposure
- aggiornamenti real-time

---

## Principi

- separazione tra protocolli e dominio
- gestione esplicita degli errori
- sicurezza nella comunicazione
- scalabilità della pipeline
- osservabilità operativa

---

## Risultato

L’architettura permette di gestire dati real-time mantenendo il backend leggibile, estendibile e adatto a contesti operativi.
