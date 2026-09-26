# NUC → MAC, L2 — **PHerc0800, tutti e sei i segmenti, due bracci: nullo**

22/09/2026, ore del NUC. Sei segmenti su sei, braccio primario (nativo 8,64 µm) e braccio secondario
(ricampionato a 9,362 µm, fattore 0,9229, `scipy.ndimage.zoom` order=1), criteri di lettura identici nei
due: soglia 0,5, area ≥ 12.000 px, esclusioni di bordo 64 px, scarto dei candidati avanti coperti ≥ 50 %
da un candidato inverso. Nessun filtro cambiato dopo aver visto un'immagine.

## L'esito, in una riga
**Nullo.** Su 26,1 Mpx di superficie, il braccio nativo lascia **11 candidati avanti contro 10 inversi**;
il ricampionato **13 contro 9**. Sul controllo positivo, a parità di criteri, erano **90 contro 39** con
le lettere riconoscibili a occhio. Non c'è asimmetria fra i versi, e le macchie che restano hanno la
stessa forma e la stessa granulometria del rumore che compare anche leggendo dalla faccia sbagliata.

## Conteggi a ogni filtro (avanti / inversi)

| segmento | Mpx | **A** soglia | A area | A bordo | **A finale** | **B** soglia | B area | B bordo | **B finale** |
|---|---:|---|---|---|---|---|---|---|---|
| 20251028213516 | 4,8 | 285/348 | 2/3 | 2/3 | **2/3** | 259/285 | 0/2 | 0/2 | **0/2** |
| 20251028220042 | 4,1 | 323/261 | 4/2 | 4/2 | **4/2** | 228/228 | 8/1 | 8/1 | **8/1** |
| 20251028220955 | 4,4 | 351/383 | 5/7 | 4/5 | **4/5** | 297/315 | 3/5 | 3/4 | **3/4** |
| 20251028222030 | 6,7 | 361/446 | 1/1 | 1/0 | **1/0** | 331/357 | 1/1 | 1/1 | **1/1** |
| 20251028225813 | 5,2 | 350/356 | 0/0 | 0/0 | **0/0** | 349/304 | 1/1 | 1/1 | **1/1** |
| 20251029010146 | 1,0 | 44/35 | 0/0 | 0/0 | **0/0** | 75/85 | 1/0 | 0/0 | **0/0** |
| **totale** | **26,1** | | | | **11/10** | | | | **13/9** |

Densità, per confronto diretto con il controllo positivo:

| | candidati avanti per Mpx | inversi per Mpx | rapporto avanti/inversi |
|---|---:|---:|---:|
| w035 (controllo, 9,362 µm) | **2,95** | 1,28 | **2,3** |
| PHerc0800 braccio A (nativo 8,64 µm) | 0,42 | 0,38 | 1,1 |
| PHerc0800 braccio B (9,362 µm) | 0,50 | 0,34 | 1,4 |

## Tempi, separati come chiesto

| | totale sui sei |
|---|---|
| rete (scaricamento dei volumi nativi, 663 MiB) | **174 s** |
| calcolo, braccio A | **260 s** |
| calcolo, braccio B | **231 s** |
| ricampionamento (CPU) | 2–10 s a segmento |
| analisi dei candidati | ~1 s a braccio sui segmenti piccoli |

Per segmento: rete 7,8–44,7 s; calcolo A 19,4–59,5 s; calcolo B 16,1–53,9 s. Tutto a lotti da 32, un
solo processo, `nvidia-smi` prima di ogni corsa (nessun job altrui presente in nessuna delle dodici).

## Che cosa si vede, oltre ai numeri
Nelle dodici immagini affiancate (`*_avanti_inverso.png`) i due versi hanno lo stesso aspetto: una
tessitura a chiazze, la stessa a destra e a sinistra. Il caso meno simmetrico è
**20251028220042 braccio B, 8 candidati avanti contro 1 inverso**: guardando l'immagine, le otto macchie
riquadrate sono chiazze della stessa granulometria del fondo, non tratti; e nello stesso segmento il
braccio nativo dà 4 contro 2. Non lo chiamo un segnale: lo riporto perché è il numero più alto della
serie e perché il G0 chiede di riportare tutto, non i migliori.

## Che cosa dice il braccio secondario sulla domanda «la scala conta?»
Conta sul conteggio grezzo, non sull'esito. Il ricampionamento a 9,362 µm cambia il numero di macchie
sopra soglia in modo sistematico (per esempio 44 → 75 sul segmento piccolo, 285 → 259 sul primo) e
sposta qualche candidato dentro o fuori dal filtro d'area, ma il verdetto resta lo stesso in tutti e sei
i segmenti: nessuna asimmetria fra i versi. Quindi la cautela sulla scala era giusta come domanda, e la
risposta è che a questa risoluzione **non è la scala a nascondere l'inchiostro**: non c'è inchiostro da
nascondere in questi sei render.

## Cosa non ho fatto
Non ho spostato la soglia, non ho cambiato l'area minima (12.000 px, tarata su w035 e congelata), non ho
scelto i segmenti (sono tutti e sei quelli pubblicati), non ho guardato i bersagli prima di fissare i
criteri. MANBp e 0332 restano intoccati: per quelli serve il render, e la decisione su dove farlo è
vostra.

## Materiale
`bersagli/PHerc0800/<segmento>/`: `rapporto.json` (tempi, comandi verbatim, tabella dei filtri),
`candidatiA.json` e `candidatiB.json` (ogni candidato con area, bbox, sovrapposizione con l'inverso),
`predA-nativo*.tif`, `predB-9362*.tif`, e le due figure affiancate. I volumi scaricati sono stati
cancellati dopo l'uso: lo spazio occupato ora è quello dei soli TIFF.
