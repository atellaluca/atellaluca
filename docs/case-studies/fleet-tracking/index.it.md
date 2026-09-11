---
title: "Backend Telemetria Fleet Real-Time | Architettura GPS e CAN Bus"
description: "Caso studio fleet tracking backend di Luca Atella per ingestione real-time della telemetria, normalizzazione dati GPS e CAN bus, API, comunicazione sicura e sistemi logistici."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "Backend real-time fleet telemetry architecture"
schema_type: "TechArticle"
---

# End-to-End Real-Time Fleet Telemetry Backend

## Sintesi

- **Contesto:** esperienza in Vemar su infrastruttura di telemetria fleet real-time.
- **Mio ruolo:** ho progettato e realizzato personalmente l’intera infrastruttura per 80 tracker.
- **Problema:** acquisire, normalizzare, persistere ed esporre dati da tracker e CAN bus in modo utilizzabile dai flussi operativi.
- **Intervento:** comunicazione via socket con i dispositivi, gestione dati CAN bus, persistenza e API REST.
- **Risultato osservato:** infrastruttura realizzata per rendere disponibili dati di telemetria a valle dei tracker.

Questo progetto è distinto dalla [Piattaforma Fleet Cloud-Portable](../cloud-portable-fleet-platform/index.md), in uso presso Studio Lambda per il turnover dei veicoli di 50 dipendenti.

## Contesto

I sistemi logistici e mobility dipendono da telemetria continua per monitorare veicoli, asset, percorsi e stato operativo in tempo reale.

Questo caso studio descrive il backend che ho realizzato per l’ingestione, la normalizzazione, la persistenza e l’esposizione di dati provenienti da dispositivi GPS e CAN bus.

---

## Obiettivi

- ingestione real-time di telemetria
- normalizzazione dati GPS e CAN bus
- API per monitoraggio e analytics
- comunicazione sicura con dispositivi
- separazione tra gestione dei protocolli e business logic
- affidabilità in ambienti misti embedded/cloud

---

## Valore Architetturale

Il sistema evidenzia competenze in data pipeline real-time, networking, API design e backend per dispositivi eterogenei.
