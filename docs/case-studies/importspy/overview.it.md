---
title: "ImportSpy | Runtime Contract Validation per Python Modulare"
description: "Caso studio ImportSpy di Luca Atella: runtime contract engine open-source per Python, validazione dei plugin, confini architetturali e diagnostica deterministica."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "ImportSpy runtime contract validation per sistemi Python modulari"
schema_type: "SoftwareSourceCode"
---

# ImportSpy — Runtime Import Contracts per Sistemi Python Modulari

**Tipo:** progetto open-source  
**Ruolo:** Project Lead & Software Architect  
**Periodo:** 2024 - Present  
**Dominio:** Python, sistemi modulari, runtime validation  
**Repository:** [ImportSpy su GitHub](https://github.com/atellaluca/importspy)  
**Adozione:** 15.000+ download su PyPI  

---

## Panoramica

ImportSpy è una libreria Python open-source progettata per applicare contratti runtime durante l’import dei moduli.

Il problema nasce nei sistemi modulari, plugin-based ed estendibili: i componenti caricati dinamicamente spesso vengono considerati validi sulla base di assunzioni implicite. ImportSpy introduce un layer di validazione contract-driven che intercetta l’import e verifica struttura, contesto e ambiente prima dell’esecuzione.

---

## Problema

Il sistema di import di Python non verifica automaticamente:

- presenza di funzioni, classi o interfacce richieste
- compatibilità con versione Python, OS o environment
- vincoli strutturali
- condizioni minime di esecuzione

Questo porta a errori tardivi, integrazioni fragili e debugging complesso.

---

## Obiettivi di Design

- fallire presto, al momento dell’import
- descrivere i requisiti in contratti dichiarativi
- mantenere basso il coupling tra contratto e implementazione
- impedire l’ingresso di moduli incompatibili nel sistema
- produrre diagnostica chiara e deterministica

---

## Architettura

ImportSpy opera come pipeline di runtime governance:

1. intercetta una richiesta di import
2. carica il contratto associato
3. valuta requisiti strutturali e contestuali
4. restituisce un risultato valido o una violazione strutturata
5. consente l’esecuzione solo se il modulo rispetta il contratto

---

## Scenari d'Uso

ImportSpy è utile per:

- sistemi plugin-based
- backend modulari
- CI/CD validation
- piattaforme IoT ed edge
- ambienti runtime sicuri
- sistemi Python long-running

---

## Community

I concetti architetturali di ImportSpy sono stati presentati al GDG Basilicata nel talk “Quando i moduli Python sanno dire di no”, dedicato agli import-time contracts e alla governance runtime dei sistemi modulari.

**Risorse**

- [Slide italiane](../../assets/talks/importspy-gdg-basilicata-it.pdf)
- [Slide inglesi](../../assets/talks/importspy-runtime-contract-validation-en.pdf)
- [Evento GDG Basilicata](https://gdg.community.dev/events/details/google-gdg-basilicata-presents-flash-talks-arena/)
