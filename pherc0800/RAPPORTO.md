# PHerc0800 — sei segmenti, due bracci: nessuna lettera visibile

Rapporto assemblato il 23/09/2026 10:36 dai file grezzi del NUC (`mac-nuc-l2/da-nuc/`), non da riassunti.

## L'esito, nella frase fissa del protocollo

> **No stroke-like structure in the forward panel that is absent from the reverse one;
> judged visually by the authors.**

In questi sei segmenti, a queste due risoluzioni, con il modello pubblico `ink_9um`
(`hybrid_3d2d-seed43/step-060000`), **non si vedono lettere**. Non si scrive che su PHerc0800
non c'è inchiostro: il papiro è stato guardato una volta, in un modo, da noi.

## Chi ha guardato, e con quale indipendenza

- **Un pannello** (`20251028220042`, braccio a 9,362 µm, il più alto della serie) è stato
  giudicato **da due lettori in modo indipendente**, con lo stesso esito: chiazze con la
  grana del fondo, nessuna continuità di tratto, inverso con tessitura equivalente.
- **Gli altri undici** sono stati giudicati **in cieco da un solo lettore** (il NUC), mescolati
  con il controllo positivo w035 e senza etichette. Il lettore ha riconosciuto il controllo
  («lettere») e ha dato «niente» a tutti e dodici i bersagli.
- **Due difetti di procedura, dichiarati**: (1) il ritaglio dei titoli a percentuale fissa ha
  lasciato visibile la riga dei conteggi proprio sul pannello di controllo, quindi lì il cieco
  non ha tenuto — corretto con un taglio calcolato sull'immagine; (2) il secondo lettore ha
  ricevuto l'esito del primo prima di depositare il proprio, quindi per undici pannelli il suo
  giudizio non è indipendente e non viene contato.

## Numeri per segmento, con l'offset in vista

La regola corretta confronta i due versi **a pari frazione di pixel accesi**; la vecchia a
soglia assoluta. Nessuna delle due dà un verdetto: si riportano entrambe.

| segmento | braccio | media av. / inv. | accesi a 0,5 av. / inv. | soglia inv. pareggiata | candidati vecchia | **candidati nuova** |
|---|---|---|---|---|---|---|
| `20251028213516` | 8,64 µm nativo | 82.6 / 88.2 | 5.87 % / 8.64 % | 139 | 2 / 3 | **2 / 0** |
|  | 9,362 µm | 76.3 / 79.8 | 4.80 % / 6.85 % | 139 | 0 / 2 | **0 / 2** |
| `20251028220042` | 8,64 µm nativo | 89.4 / 84.4 | 11.51 % / 6.89 % | 112 | 4 / 2 | **4 / 5** |
|  | 9,362 µm | 82.9 / 78.6 | 10.40 % / 5.19 % | 110 | 8 / 1 | **8 / 4** |
| `20251028220955` | 8,64 µm nativo | 89.2 / 94.3 | 10.66 % / 14.70 % | 137 | 4 / 5 | **4 / 3** |
|  | 9,362 µm | 81.1 / 84.2 | 9.22 % / 11.09 % | 134 | 3 / 4 | **3 / 2** |
| `20251028222030` | 8,64 µm nativo | 81.6 / 81.3 | 5.15 % / 4.32 % | 123 | 1 / 0 | **1 / 0** |
|  | 9,362 µm | 76.1 / 75.1 | 5.30 % / 3.98 % | 121 | 1 / 1 | **1 / 2** |
| `20251028225813` | 8,64 µm nativo | 81.7 / 82.6 | 4.50 % / 4.23 % | 126 | 0 / 0 | **0 / 0** |
|  | 9,362 µm | 78.1 / 78.1 | 5.25 % / 5.17 % | 127 | 1 / 1 | **1 / 1** |
| `20251029010146` | 8,64 µm nativo | 81.9 / 83.6 | 4.67 % / 7.25 % | 140 | 0 / 0 | **0 / 0** |
|  | 9,362 µm | 82.7 / 81.7 | 7.90 % / 6.46 % | 121 | 0 / 0 | **0 / 0** |

**Totali** — braccio nativo: vecchia 11/10, nuova **11/8**;
braccio a 9,362 µm: vecchia 13/9, nuova **13/11**
(avanti / inversi).

Per confronto, il controllo positivo w035 con gli stessi criteri: vecchia 90/39, nuova 89/67.
**Il rapporto avanti/inversi del controllo (1,33) sta dentro l'intervallo dei bersagli**: per
questo il conteggio non è un verdetto, e il verdetto è visivo.

## Densità di candidati, per Mpx occupato

Denominatore unico: l'area che l'inferenza ha trovato non vuota (`nonempty_coverage` nei log),
ricalcolata da `reproduce.py`. Gli altri due denominatori usati in giorni diversi sono
spiegati in `ERRATA.md`, voce 4.

| | densità |
|---|---|
| w035, controllo con inchiostro | 3,55 |
| 0139 w029, controllo con inchiostro | 3,39 |
| **PHerc0800 braccio nativo** | **0,87** |
| **PHerc0800 braccio 9,362 µm** | **1,20** |
| MANBp w0 (nessuna lettera a vista) | 4,59 |

I bersagli senza lettere stanno **da entrambe le parti** dei controlli: 0800 molto sotto,
MANBp w0 sopra. È la prova che la densità non separa.

## Nota di precisione sulla soglia

Il NUC applica la soglia 0,5 come **≥ 128** su mappe uint8; lo script del Mac come **≥ 127**.
Un livello su 255. Tutti i numeri di questa pagina vengono dal NUC, quindi sono a ≥ 128.
Per MANBp e 0332 si usa **≥ 128** ovunque.

## Le immagini

Tutte e dodici, nelle sottocartelle per segmento: `predA-nativo_avanti_inverso.png` e
`predB-9362_avanti_inverso.png`. Anche quelle noiose.

## Tempi

Rete 174 s in tutto (663 MiB); calcolo braccio nativo 260 s, braccio 9,362 µm 231 s; su una
RTX 2070 SUPER partendo dai volumi di superficie già pubblicati, quindi senza render.
