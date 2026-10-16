---
title: "Architettura ImportSpy | Evidenze, Policy e Ammissione Python"
description: "Come ImportSpy di Luca Atella separa ispezione del sorgente, identità delle dipendenze, raccolta delle evidenze, valutazione delle policy ed esecuzione Python esplicita."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "Luca Atella, autore dell’architettura di ammissione Python di ImportSpy"
schema_type: "TechArticle"
---

# ImportSpy — Architettura

ImportSpy separa **la raccolta di informazioni sul modulo**, **la decisione sulla conformità alle policy** e **l’esecuzione**. Ogni passaggio ha un diverso confine di fiducia. Questa separazione permette a sviluppatori, pipeline CI e sistemi di plugin di usare il risultato senza rendere l’esecuzione una conseguenza implicita della validazione.

Il [case study](index.md) presenta il contesto; questa pagina approfondisce i compromessi architetturali di **ImportSpy 0.5.0**.

## Snapshot del sorgente e confine di esecuzione

L’ispettore legge i byte del sorgente, ne calcola l’hash, analizza l’AST e lo compila per verificarne la sintassi senza eseguire il codice risultante. I fatti descrivono dichiarazioni e import, non tutti i possibili oggetti runtime. Decoratori, metaclassi e valori calcolati possono lasciare proprietà richieste sconosciute; l’ispezione non li esegue per eliminare l’incertezza.

`check` restituisce una decisione anche quando l’ammissione riesce. Per eseguire serve un `load` esplicito, che aggiorna i metadati delle dipendenze e ripete il controllo di ammissione. Dopo l’approvazione, esegue i byte acquisiti senza riaprire il percorso. Un test modifica il file durante la raccolta delle evidenze e verifica l’esecuzione dello snapshot ispezionato.

Questo limita il divario tra controllo e uso del **sorgente selezionato**. Non congela dipendenze installate, import hook, file esterni o processo circostante. I validatori runtime intervengono dopo l’inizializzazione del modulo; rimuovere da `sys.modules` un modulo che ha fallito non ne annulla gli effetti. Il loader non è un import hook né una sandbox.

Le API di compatibilità mantenute, `Spy.importspy` e `SpyModel.from_module`, ispezionano moduli già eseguiti. Appartengono alla precedente architettura dei contratti runtime e non acquisiscono il confine prima dell’esecuzione della pipeline di ammissione. Si vedano il [flusso della libreria e le indicazioni di migrazione](https://github.com/atellaluca/ImportSpy/blob/main/docs/modes/embedded.md).

## Identità delle dipendenze senza false certezze

Il nome di importazione e quello della distribuzione rispondono a domande diverse. Un import può corrispondere a più distribuzioni installate, mentre una distribuzione può fornire più import. ImportSpy conserva queste relazioni senza scegliere arbitrariamente un solo contributore. Per i namespace adotta quindi un criterio conservativo: la policy valuta tutti i contributori identificati.

Il resolver distingue dipendenze della libreria standard, interne, esterne, namespace, con origine diretta e non risolte. Legge percorsi del sorgente e metadati installati senza importare le dipendenze candidate. Le corrispondenze mancanti restano non risolte; se un fatto richiesto non può essere accertato, l’ammissione viene negata.

Questa prudenza può includere contributori del namespace inutilizzati da uno specifico import figlio. L’inventario comprende gli import osservati nel file selezionato, inclusi quelli condizionali e nei corpi delle funzioni. Non ricostruisce ricorsivamente il grafo delle dipendenze transitive e non intercetta gli import dinamici.

## Evidenze separate dalle policy

I record normalizzati `Evidence` contengono soggetto, osservazione, provider, fase e stato. Quattro stati conservano distinzioni che un booleano perderebbe:

| Stato | Significato |
| --- | --- |
| `verified` | Il produttore ha accertato lo specifico fatto dichiarato. |
| `observed` | Il dato è disponibile senza una verifica più forte. |
| `unknown` | Il metodo non permette di accertare il fatto. |
| `unavailable` | La raccolta è fallita o è stata disabilitata. |

I metadati sull’origine installata sono un’osservazione, non una prova crittografica di provenienza. Analogamente, una sintassi verificata non dimostra che il comportamento arbitrario del codice Python sia sicuro. La policy stabilisce quali fatti e stati siano sufficienti; un’evidenza richiesta sconosciuta o indisponibile non può diventare implicitamente un’approvazione.

Separare raccolta e valutazione rende la policy deterministica **a parità di policy e fatti**. I controlli di base funzionano offline, senza account o telemetria. Controlli distinti possono comunque differire perché cambiano sorgente, metadati installati, stato dell’host e timestamp. Le cache delle dipendenze appartengono a un’istanza del motore; il caricamento esplicito le aggiorna.

## Estensioni e fasi di esecuzione

| Estensione | Responsabilità e fase di esecuzione |
| --- | --- |
| `EvidenceProvider` | Raccoglie fatti locali o esterni selezionati durante l’ammissione. |
| `PolicyValidator` | Valuta i fatti raccolti senza I/O nella fase di policy. |
| `RuntimeValidator` | Ispeziona oggetti runtime dopo l’esecuzione esplicita del modulo. |
| `Reporter` | Formatta una decisione esistente senza ripetere l’ammissione. |

Sono estensioni Python considerate attendibili. I provider vengono selezionati esplicitamente; il motore non carica tutti i plugin installati. La raccolta via rete richiede un’abilitazione esplicita: un accordo di cooperazione, non un firewall attorno all’inizializzazione o al codice dei plugin.

I protocolli sono implementati; l’[esempio di estensione offline](https://github.com/atellaluca/ImportSpy/blob/main/docs/extensions.md) ne dimostra l’uso senza verifiche esterne. Gli adattatori per OSV/pip-audit, Sigstore, attestazioni PyPI, CycloneDX, SPDX e metadati GitHub restano [integrazioni proposte](https://github.com/atellaluca/ImportSpy/blob/main/docs/community-roadmap.md), non funzionalità native.

## Una decisione, più destinatari

`AdmissionDecision` riunisce identità e hash di sorgente e policy, versione del motore, fatti sull’host, dipendenze, evidenze, violazioni ed esito. Le fasi e il flag `target_executed` distinguono l’ispezione dell’host dall’esecuzione del modulo. Una `Violation` contiene codice stabile, severità, spiegazione e posizione nel sorgente quando nota.

I reporter leggibili da persone, JSON e SARIF usano la stessa decisione. JSON conserva inventario ed evidenze; SARIF presenta le violazioni per i flussi di code scanning. La formattazione non ripete la raccolta e non esegue il modulo. L’automazione ottiene così diagnostica strutturata, mantenendo le evidenze necessarie a spiegare un rifiuto.

Implementazione e limiti della **0.5.0**: [architettura ufficiale](https://github.com/atellaluca/ImportSpy/blob/main/docs/architecture.md), [modello di sicurezza](https://github.com/atellaluca/ImportSpy/blob/main/docs/security-model.md) e [codice sorgente](https://github.com/atellaluca/ImportSpy).
