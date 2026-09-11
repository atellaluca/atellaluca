---
title: "Backend Unificato per Sorgenti Eterogenee | Framework delis.app"
description: "Caso studio SAFE sul framework backend sviluppato da Luca Atella in Vemar e alla base di delis.app, con integrazioni eterogenee, plugin architecture, REST API e WebSocket."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "Unified backend architecture per sorgenti dati IoT eterogenee"
schema_type: "TechArticle"
---

# Unified Backend for Heterogeneous Data Sources (SAFE)

## Sintesi

- **Contesto:** in Vemar serviva un framework backend capace di collegare sorgenti dati eterogenee e dispositivi diversi dietro API e modelli coerenti.
- **Mio ruolo:** come Tech Lead ho sviluppato il framework su cui si fonda delis.app e ho coordinato tecnicamente un team di 4 persone.
- **Problema:** integrazioni e protocolli diversi rischiavano di produrre logica duplicata, accoppiamenti nascosti e diagnosi difficili.
- **Intervento:** ho progettato confini plugin-based, contratti di integrazione, API REST/WebSocket e separazione tra core e adapter.
- **Risultato osservato:** il framework è diventato la base tecnica di delis.app.

Questo caso è presentato in forma SAFE: descrive il framework e le scelte architetturali trasferibili, senza attribuire automaticamente a delis.app ogni generalizzazione o proprietà astratta illustrata nella pagina.

## Contesto

Le piattaforme moderne devono spesso integrare sorgenti dati molto diverse: dispositivi IoT, API esterne, stream di eventi, sistemi legacy e sensori domain-specific.

Questo caso studio parte dal framework che ho sviluppato in Vemar e su cui si fonda delis.app. La pagina astrae nomi, dettagli proprietari e implementazioni sensibili, ma mantiene riconoscibile il contributo concreto: sviluppo del framework, responsabilità tecnica e separazione delle integrazioni.

---

## Obiettivi

- integrare producer eterogenei
- normalizzare formati incompatibili
- validare dati in ingresso
- isolare la logica di ingestion
- evolvere schema e plugin senza destabilizzare il core
- migliorare osservabilità e developer experience

---

## Architettura

Il sistema è organizzato in layer:

1. ingestion plugin
2. normalizzazione
3. runtime validation
4. service layer e API

Ogni layer è progettato per essere testabile, sostituibile e scalabile.

---

## Valore

L’architettura trasforma un backend statico in una piattaforma di integrazione governata, dove nuove sorgenti dati possono essere aggiunte senza riscrivere il core.
