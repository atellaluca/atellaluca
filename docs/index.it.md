---
title: "Luca Atella | Software Architect e Backend Engineer"
description: "Luca Atella, Software Architect e sviluppatore backend Python in Basilicata. Progetti con FastAPI, AWS e sistemi IoT. Casi studio, competenze e CV."
image: "assets/luca-atella-portrait.jpg"
image_alt: "Ritratto di Luca Atella, Software Architect e Backend Engineer"
schema_type: "ProfilePage"
hide:
  - navigation
  - toc
---

<div class="portfolio-home" markdown>
<div class="portfolio-hero" markdown>
<div class="portfolio-hero-copy" markdown>
<p class="portfolio-eyebrow">TECH LEAD · BACKEND ENGINEER · PLATFORM ENGINEER</p>

# Luca Atella

<p class="portfolio-lead">Dall’architettura al software<br>che lavora in produzione.</p>

Progetto e sviluppo direttamente backend Python, API e piattaforme cloud. In Vemar sono stato Tech Lead, coordinando tecnicamente un team di 4 persone e realizzando sistemi backend usati in contesti operativi reali.

<p class="portfolio-location">Basilicata, Italia · Collaborazioni da remoto e in modalità ibrida</p>

[Parliamo di un’opportunità](contact.md){ .md-button .md-button--primary }
[Esplora i progetti](#progetti-selezionati){ .md-button }

[Leggi il CV](cv.md) · [LinkedIn](https://www.linkedin.com/in/luca-atella/) · [English version](/)

</div>
<div class="portfolio-identity" markdown>
![Ritratto di Luca Atella, Software Architect e Backend Engineer](assets/luca-atella-portrait.jpg){ width="1032" height="1280" fetchpriority="high" loading="eager" decoding="async" }
<p>Confini chiari.<br>Integrazioni affidabili.<br>Software che può evolvere.</p>
</div>
</div>

<div class="portfolio-proof-grid" markdown>
<div class="portfolio-proof" markdown>
**Esperienza in produzione**

Fleet Management System in uso presso Studio Lambda per il turnover dei veicoli di 50 dipendenti.
</div>
<div class="portfolio-proof" markdown>
**Tech Lead in Vemar**

Coordinamento continuativo di un team di 4 persone, infrastruttura per 80 tracker e framework alla base di delis.app.
</div>
<div class="portfolio-proof" markdown>
**Sviluppo diretto e diagnosi**

Backend, infrastrutture, runtime isolati e contratti espliciti: dal codice alla verifica operativa.
</div>
</div>

## Progetti selezionati

Il problema, le scelte progettuali e il sistema risultante. Ogni caso studio distingue il lavoro in produzione dai progetti open source e dalle architetture di riferimento.

<div class="portfolio-card-grid" markdown>
<div class="portfolio-card" markdown>
<p class="portfolio-eyebrow">01 / PIATTAFORMA IN PRODUZIONE</p>

### Piattaforma Fleet Cloud-Portable

**Il contesto:** Fleet Management System in uso presso Studio Lambda per gestire il turnover dei veicoli di 50 dipendenti.

**Il lavoro:** backend FastAPI, frontend React/TypeScript, astrazione di repository e storage, sviluppo locale riproducibile e deployment effettivo su AWS.

<p class="portfolio-stack">Python · FastAPI · DynamoDB · S3 · Lambda</p>

[Architettura e scelte del progetto →](case-studies/cloud-portable-fleet-platform/index.md)
</div>
<div class="portfolio-card" markdown>
<p class="portfolio-eyebrow">02 / ESPERIENZA VEMAR</p>

### Backend Telemetria Fleet Real-Time

**Il contesto:** infrastruttura progettata e realizzata personalmente in Vemar per 80 tracker.

**Il lavoro:** comunicazione socket, dati CAN bus, persistenza, normalizzazione e API REST per rendere disponibili i dati operativi.

<p class="portfolio-stack">Python · Socket · CAN bus · REST API</p>

[Leggi il caso telemetria →](case-studies/fleet-tracking/index.md)
</div>
<div class="portfolio-card" markdown>
<p class="portfolio-eyebrow">03 / PROGETTO OPEN SOURCE</p>

### ImportSpy: contratti espliciti tra moduli

**Il problema:** i sistemi a plugin possono fallire quando un modulo non rispetta struttura e vincoli di esecuzione attesi.

**Il lavoro:** un motore Python che verifica contratti durante l’import e restituisce violazioni strutturate per rendere diagnosticabili le incompatibilità.

<p class="portfolio-stack">Python · Plugin · Runtime validation · DSL</p>

[Esplora il motore di validazione →](case-studies/importspy/index.md)
</div>
<div class="portfolio-card" markdown>
<p class="portfolio-eyebrow">04 / INTERVENTO PROFESSIONALE</p>

### Runtime isolati per applicativi fiscali

**Il problema:** applicativi Agenzia delle Entrate di annualità diverse richiedevano runtime Java e modalità di avvio non compatibili fra loro.

**Il lavoro:** isolamento dei runtime, gestione JNLP/LaunchAnywhere, trattamento separato di Desktop Telematico/Entratel e verifiche di coesistenza.

<p class="portfolio-stack">Windows · Java runtime · JNLP · Entratel</p>

[Leggi il caso compatibilità →](case-studies/agenzia-entrate-runtime-isolation/index.md)
</div>
<div class="portfolio-card" markdown>
<p class="portfolio-eyebrow">05 / PIPELINE GEOSPAZIALE · NON PUBBLICATA</p>

### B3DO: dati della Basilicata, in tre dimensioni

Una pipeline per trasformare dataset pubblici del terreno in modelli 3D: ritaglio dei raster, livelli di dettaglio, mesh e texture, con un workflow da riga di comando.

<p class="portfolio-stack">Python · GDAL · Rasterio · NumPy · PyVista</p>

[Dal dato al modello 3D →](case-studies/b3do/index.md)
</div>
<div class="portfolio-card" markdown>
<p class="portfolio-eyebrow">06 / ARCHITETTURA DI RIFERIMENTO</p>

### Dati IoT utilizzabili nei Digital Twin

Un’architettura edge-to-cloud per integrare sensori, dispositivi e sorgenti eterogenee: acquisizione, aggregazione e accesso ai dati attraverso confini espliciti.

<p class="portfolio-stack">IoT · Edge/cloud · GraphQL · Data integration</p>

[Esplora l’architettura Digital Twin →](case-studies/iot-data-aggregation-digital-twin/index.md)
</div>
</div>

[Tutti i casi studio, inclusi backend unificato e telemetria →](case-studies/index.md)

## Cosa porto nel team

<div class="portfolio-proof-grid" markdown>
<div class="portfolio-proof" markdown>
### Backend e API

Python, FastAPI, modellazione dati e sistemi modulari. Confini chiari tra logica di business, integrazioni e persistenza.
</div>
<div class="portfolio-proof" markdown>
### Cloud e operatività

AWS, Docker e Infrastructure as Code. Ambienti riproducibili, deployment e osservabilità considerati insieme al codice.
</div>
<div class="portfolio-proof" markdown>
### Decisioni documentate

Contratti espliciti, errori comprensibili e scelte motivate. Un sistema deve poter essere mantenuto anche da chi arriva dopo.
</div>
</div>

[Il mio metodo](methodology.md) · [Profilo tecnico](profile.md) · [Percorso e certificazioni nel CV](cv.md) · [Chi sono](about.md)

<div class="portfolio-contact" markdown>
<p class="portfolio-eyebrow">IL PROSSIMO PROGETTO</p>

## Cerchi una figura backend o software architect?

Mi interessano opportunità in backend engineering, platform engineering e architettura software. Raccontami il prodotto, il team e il problema da affrontare.

[Scrivimi via email](mailto:info@atellaluca.com){ .md-button .md-button--primary }
[Scarica il CV in PDF](assets/cv/Luca-Atella-CV.pdf){ .md-button }

Oppure [contattami su LinkedIn](https://www.linkedin.com/in/luca-atella/).
</div>
</div>
