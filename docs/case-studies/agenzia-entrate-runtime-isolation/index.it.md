---
title: "Compatibilità runtime Agenzia delle Entrate | Caso Studio"
description: "Intervento di Luca Atella su compatibilità e isolamento dei runtime Java per applicativi Agenzia delle Entrate in uno studio commercialista."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "Caso studio su isolamento runtime e compatibilità applicativi legacy"
schema_type: "TechArticle"
---

# Compatibilità e isolamento dei runtime per gli applicativi Agenzia delle Entrate

- **Tipo:** intervento professionale su ambiente operativo legacy
- **Contesto:** studio commercialista, adempimenti fiscali e strumenti di compliance
- **Ruolo:** diagnosi tecnica, isolamento runtime, verifica di coesistenza
- **Tecnologie:** Windows · Java runtime · JNLP · LaunchAnywhere · Desktop Telematico / Entratel

---

## Sintesi

- **Contesto:** uno studio commercialista doveva mantenere utilizzabili applicativi Agenzia delle Entrate di diverse annualità nello stesso ambiente Windows.
- **Mio ruolo:** ho analizzato le incompatibilità, isolato i runtime Java per applicazione e verificato la coesistenza degli strumenti.
- **Problema:** una configurazione Java globale non soddisfaceva tutti gli applicativi; sistemare un programma poteva compromettere gli altri.
- **Intervento:** ho separato runtime, modalità di avvio e requisiti specifici di Desktop Telematico / Entratel, incluse esigenze TLS e truststore.
- **Risultato osservato:** gli applicativi nuovi e storici hanno potuto coesistere nello stesso ambiente di lavoro senza dipendere da una singola configurazione Java globale.

---

## Contesto Operativo

L’ambiente era Windows e includeva applicativi di annualità e famiglie diverse, fra cui:

- IRAP 2019-2021;
- ISA;
- Desktop Telematico / Entratel;
- altri applicativi con dipendenze Java differenti.

La necessità non era progettare un nuovo sistema, ma garantire continuità operativa a strumenti già usati nello studio.

---

## Problema

Gli applicativi non condividevano gli stessi requisiti di runtime. Una configurazione Java globale poteva far funzionare un programma e bloccarne un altro.

Il problema coinvolgeva:

- versioni Java diverse;
- modalità di avvio differenti;
- applicazioni avviate via JNLP;
- applicazioni impacchettate con LaunchAnywhere;
- requisiti specifici di comunicazione, TLS e truststore per Desktop Telematico / Entratel.

---

## Intervento Personale

Ho lavorato su diagnosi, isolamento e verifica:

- isolamento dei runtime Java per applicazione;
- gestione delle specificità di avvio legate a JNLP e LaunchAnywhere;
- trattamento separato delle esigenze di Desktop Telematico / Entratel;
- rimozione della dipendenza da un’unica configurazione Java globale;
- verifiche incrociate di funzionamento e coesistenza degli applicativi.

---

## Competenze Dimostrate

Questo intervento mostra un metodo applicabile anche a sistemi software più ampi:

- diagnosi delle incompatibilità in ambienti legacy;
- gestione e isolamento delle dipendenze;
- integrazione di software di terze parti;
- attenzione alle regressioni;
- supporto alla continuità operativa;
- scelta di interventi proporzionati alle necessità del cliente.

---

## Perimetro

Il lavoro riguarda infrastruttura, compatibilità e coesistenza degli strumenti utilizzati per gli adempimenti fiscali.

Non riguarda consulenza fiscale, certificazione di conformità normativa, attività da auditor o responsabilità da compliance officer. L’isolamento dei runtime non è presentato come garanzia di sicurezza, conformità normativa o supporto ufficiale degli applicativi legacy.

---

## Collegamento al Metodo

Questo caso è diverso dai progetti backend, ma segue lo stesso principio: governare le relazioni fra componenti, dipendenze e ambiente di esecuzione considerando gli effetti delle modifiche sull’intero sistema.

Lo stesso filo conduttore appare in [ImportSpy](../importspy/index.md), dove i contratti rendono esplicite le incompatibilità fra moduli, e nella [Piattaforma Fleet Cloud-Portable](../cloud-portable-fleet-platform/index.md), dove la logica applicativa è separata dai servizi infrastrutturali.
