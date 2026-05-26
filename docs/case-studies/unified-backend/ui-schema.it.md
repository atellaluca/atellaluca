---
title: "Declarative UI Schema | Widget DSL per Backend Eterogenei"
description: "Caso studio declarative UI schema per interfacce guidate dal backend, widget DSL, dispositivi eterogenei e contratti frontend-backend manutenibili."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "Declarative UI schema e widget DSL per backend eterogenei"
schema_type: "TechArticle"
---

# Declarative UI Schema

Nei sistemi con dispositivi eterogenei, la complessità frontend cresce rapidamente: ogni famiglia di dispositivi può richiedere viste, controlli e dati diversi.

Un declarative UI schema permette al backend di descrivere la struttura dell’interfaccia tramite un contratto leggibile e versionabile.

---

## Obiettivi

- ridurre logica hardcoded nel frontend
- descrivere widget e dati in modo dichiarativo
- mantenere coerenza tra device model e UI
- supportare nuove tipologie di dispositivi
- rendere esplicito il contratto frontend-backend

---

## Valore

Il widget DSL sposta parte della complessità in uno schema controllato, rendendo l’interfaccia più adattabile senza perdere governance.
