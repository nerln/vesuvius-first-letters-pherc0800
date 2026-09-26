# Quali papiri si possono davvero sondare — misurato il 22/09/2026 16:26

Fonte: elenco del bucket pubblico `vesuvius-challenge-open-data` letto via HTTP
(`?list-type=2&delimiter=/`), contando i prefissi sotto `<papiro>/segments/`.
Dati grezzi in `segmenti-per-papiro.csv`. **45 papiri, 29 senza nessun segmento.**

## I quattro bersagli proposti non sono sondabili
PHerc0125, PHerc0211, PHerc0257, PHerc0813 **non hanno affatto una cartella
`segments/`**: hanno solo `photos/`, `representations/` (predizioni lasagna) e
`volumes/`. Senza mesh pubblicate non c'è niente da rendere: bisognerebbe prima
tracciare i segmenti, che è un lavoro di settimane, non di cinque giorni.

## I modelli condivisi sono addestrati su quattro papiri
PHerc0139, PHerc1667, PHercParis4, PHerc0814 (`07_tutorial5.md:483`). Un risultato su
questi **non è First Letters**: sono il set di addestramento.

## Quindi i bersagli veri sono questi, e sono 168 segmenti su 12 papiri

| papiro | segmenti | note |
|---|---|---|
| PHerc0172 | 53 | il più ricco fra i non addestrati |
| PHerc0500P2 | 46 | |
| PHerc0009B | 20 | |
| PHerc1447 | 16 | |
| PHercMANBp | 11 | |
| PHerc0343P | 8 | |
| PHerc0800 | 6 | |
| PHerc0841 | 3 | |
| PHerc0332 | 2 | |
| PHercMAN5 | 1 | già sondato da noi (protocollo recto, nullo pulito) |
| PHerc1451 | 1 | |
| PHerc1203 | 1 | già sondato da kadenpool (`reports/pherc1203-first-letters`) |

## Il controllo positivo invece è documentato e pronto
**w035 di PHerc0139**, che la challenge stessa indica come esempio guidato proprio perché
sta nel set di addestramento: «so you know what a good result looks like before trying an
unread scroll» (`07_tutorial5.md:503`). Il suo volume di superficie **è già pubblicato**
sotto `surface-volumes/`, quindi il render si può saltare.

## Cosa resta da verificare prima di scegliere
Quali di questi 168 segmenti sono già stati sondati da altri. «Mai sondato» è un criterio
che va misurato, non assunto: due dei dodici papiri lo sono già.
