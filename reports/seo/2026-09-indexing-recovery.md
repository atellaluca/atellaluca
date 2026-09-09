# Indicizzazione e restyling — 9 settembre 2026

## Diagnosi verificata

La homepage pubblica `https://profile.atellaluca.com/` risponde HTTP 200, con canonical autoreferenziale e `index,follow`. Non risultano blocchi globali in robots.txt né X-Robots-Tag nella risposta esaminata. Il server è GitHub Pages; il documento pubblico risultava modificato il 2 giugno 2026. Questi riscontri dimostrano accessibilità tecnica, non inclusione nell’indice Google.

Problemi osservati sul sito pubblico o riprodotti nella build:

1. **Hreflang HTML relativi** (`/` e `/it/`). Google richiede URL assoluti. La sitemap aveva già alternates assoluti: il difetto HTML non dimostra da solo una perdita completa di indicizzazione.
2. **Redirect JavaScript basato sulla lingua del browser**. Poteva impedire a un visitatore italiano di aprire volontariamente la versione inglese in una nuova sessione. Rimosso: ogni URL ora serve stabilmente la propria lingua.
3. **Vecchi URL `/overview/` senza migrazione**. Verificato HTTP 404 su `/case-studies/importspy/overview/`. Generati redirect per i sei casi studio in entrambe le lingue.
4. **Sitemap con duplicato `/cv/`**: la modifica del canonical della pagina stampa alterava anche il `loc` usato dal generatore. Il canonical viene ora corretto solo nell’HTML finale; la sitemap elimina le pagine stampa e mantiene le due vere pagine CV con alternates completi.
5. **Pagina stampa bloccata da robots.txt e contemporaneamente noindex**: il blocco impediva la lettura della direttiva noindex. Ora è scansionabile, esclusa dalla sitemap e canonicalizzata al CV della stessa lingua.
6. **Titoli ridondanti**: nome e qualifica ripetuti dal titolo globale. Titoli semplificati e nome presente una sola volta.

Non sono disponibili i report privati di Google Search Console. Non è quindi dimostrabile se il motivo decisivo sia “Scansionata, ma attualmente non indicizzata”, un canonical scelto da Google, una rimozione o altro. L’assenza per una keyword non equivale necessariamente ad assenza dall’indice. Non è stata attribuita una penalizzazione al multilingua.

## Interventi

- URL lingua stabili e selettore esplicito; hreflang EN/IT assoluti, reciproci e `x-default` inglese.
- Sitemap XML e gzip sincronizzate; nessuna pagina stampa o redirect tra gli URL da indicizzare.
- Dodici pagine di migrazione con meta refresh immediato, canonical e link accessibile. GitHub Pages non supporta una configurazione di redirect HTTP 301: il meta refresh è il ripiego statico documentato da Google. Su hosting con redirect server, preferire 301/308.
- Identità Person e WebSite stabile nei dati strutturati, `inLanguage`, immagine social condivisa dal percorso assoluto e noindex sulla 404.
- Homepage EN/IT ridisegnate: gerarchia tipografica, palette verde/petrolio, identità visiva esistente, progetti a schede, competenze collegate alle evidenze, pulsanti contatto e CV visibili all’inizio e alla fine.
- Testi dei contatti orientati anche a selezione del personale, ruoli backend/platform/architecture e informazioni utili per iniziare il colloquio.
- Nessuna metrica, esperienza o disponibilità contrattuale inventata. Distinti progetti in produzione, open source, pipeline non pubblicata e architetture di riferimento.
- Workflow: build strict e controllo SEO obbligatori; pubblicazione dello stesso artefatto verificato con ghp-import.

## Validazione

Ambiente temporaneo in `/tmp/portfolio-venv`, con versioni di `poetry.lock` (il vecchio ambiente locale non aveva un interprete funzionante).

```sh
poetry run mkdocs build --strict
poetry run python scripts/check_seo.py site
```

Eseguiti equivalenti con l’ambiente temporaneo e output `/tmp/portfolio-audit`:

- Build strict superata.
- 44 pagine indicizzabili: canonical, lingua HTML, descrizione, singolo H1, JSON-LD, risorse e collegamenti interni presenti.
- Alternates HTML e sitemap corrispondenti e reciproci su tutte le pagine.
- XML e gzip identici dopo decompressione; due pagine stampa noindex e 12 redirect corretti.
- Chromium: home EN/IT desktop 1440 px; italiano a 820/390 px; inglese a 320 px con browser italiano; caso studio e contatti su mobile. Nessun overflow orizzontale, immagine mancante o errore JavaScript.
- Cambio lingua IT → EN → IT verificato; home italiana e contatto utilizzabili senza JavaScript.
- Screenshot desktop e mobile controllati visivamente in `/tmp/portfolio-desktop-it.png` e `/tmp/portfolio-mobile-it.png`.

## Pubblicazione e verifica Google

Stato al termine della diagnosi: modifiche preparate e verificate localmente. La pubblicazione viene avviata dal push su `main`; il workflow compila il sito, verifica i segnali SEO e pubblica solo l’artefatto validato. L’esito effettivo va verificato in GitHub Actions e sugli URL pubblici.

Dopo il deploy:

1. Verificare che le due home pubbliche abbiano i nuovi contenuti, hreflang assoluti e nessun redirect di lingua; verificare un vecchio URL `/overview/`.
2. In Search Console, proprietà del dominio o del prefisso corretto, inviare `https://profile.atellaluca.com/sitemap.xml`.
3. Ispezionare `/` e `/it/`: registrare motivo di esclusione, ultima scansione, canonical dichiarato e canonical scelto da Google. Usare anche il test live.
4. Richiedere indicizzazione delle due home e delle principali pagine CV/casi studio. Se compare un problema specifico, risolverlo in base al responso effettivo.
5. Monitorare impressioni e clic delle query “Luca Atella”, “Luca Atella backend”, “Luca Atella software architect” e delle pagine IT/EN. Una richiesta di indicizzazione non garantisce inclusione, tempi o posizionamento.
6. Controllare che LinkedIn e GitHub rimandino al dominio canonico del portfolio. Non sono stati modificati account esterni.

## Fonti ufficiali

### Riscontro sugli URL indicati dall’utente

Verifica HTTP diretta successiva alla segnalazione:

| URL | Risposta pubblica |
| --- | --- |
| `/case-studies/unified-backend/overview/` | 404 |
| `/case-studies/importspy/` | 200 |
| `/it/case-studies/importspy/` | 200 |

Il primo collegamento inviato aveva testo ImportSpy ma destinazione Unified Backend `/overview/`. Il redirect generato copre quest’ultima destinazione e conduce a `/case-studies/unified-backend/`, non a ImportSpy.

La pagina italiana ImportSpy pubblica ha canonical autoreferenziale e `index,follow`; gli hreflang HTML sono ancora relativi. L’utente segnala che Google l’ha trovata ma non indicizzata: manca la dicitura esatta per distinguere “Rilevata, ma attualmente non indicizzata” (scoperta senza scansione) da “Scansionata, ma attualmente non indicizzata” (scansione avvenuta). Non si deduce un blocco robots o una penalizzazione dal solo stato di esclusione.

Aggiunta alla pagina italiana una sezione sul contributo personale, già documentato nella versione inglese, e collegamenti agli approfondimenti, al profilo e al CV. Il miglioramento aiuta lettura e navigazione, senza costituire garanzia di indicizzazione.

Al momento del riscontro le correzioni erano locali e il vecchio URL pubblico restituiva ancora 404. Dopo la pubblicazione, controllare il vecchio URL e ispezionare in Search Console l’URL italiano ImportSpy, annotando dicitura esatta, ultima scansione ed eventuale canonical scelto da Google.

### Riferimenti

- [Google: gestione di siti multilingua e redirect automatici](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)
- [Google: URL assoluti e reciprocità hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Google: redirect e meta refresh immediato](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
