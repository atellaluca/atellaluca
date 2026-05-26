---
title: "B3DO | Pipeline Geospaziale per Modelli 3D del Territorio"
description: "Caso studio B3DO di Luca Atella: pipeline geospaziale Python con GDAL, Rasterio, NumPy e PyVista per generare modelli 3D da open data della Basilicata."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "B3DO pipeline geospaziale per modelli 3D della Basilicata"
schema_type: "TechArticle"
---

# B3DO — Basilicata 3D Open

**Tipo:** pipeline geospaziale  
**Ruolo:** Project Lead · Software Architect · Data Pipeline Engineer  
**Stato:** in sviluppo  
**Dominio:** geospatial data, terrain modeling, 3D model generation, open data  

---

## Overview

B3DO è una pipeline Python pensata per trasformare dataset pubblici del territorio lucano in modelli 3D del terreno.

Il progetto nasce dall’interesse per Basilicata, open data e sistemi di processing riproducibili: non un workflow GIS manuale, ma una pipeline tecnica che separa sorgenti, dati processati, artifact intermedi e modelli finali.

---

## Cosa Fa

- merge di tile DTM
- estrazione dei confini regionali
- clipping raster
- generazione LOD multi-risoluzione
- mesh 3D del terreno
- hillshade e hypsometric color relief
- overlay idrografico
- preview e output testurizzati

---

## Stack

- Python
- GDAL
- Rasterio
- NumPy
- PyVista
- Fiona
- Typer

---

## Valore Architetturale

B3DO dimostra come principi di backend architecture possano essere applicati anche a pipeline dati: input espliciti, step riproducibili, separazione degli artifact, diagnostica e workflow CLI.

È anche un progetto legato al territorio: usa dati pubblici della Basilicata per generare rappresentazioni tecniche e visive del territorio lucano.
