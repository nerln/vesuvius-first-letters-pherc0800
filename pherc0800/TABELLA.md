# PHerc0800 — sei segmenti, due bracci, conteggi dopo ogni filtro

Criteri congelati nel G0 prima di vedere qualunque bersaglio: soglia 0,5, area >= 12.000 px,
bordo 64 px, scarto di un candidato avanti se un candidato inverso lo copre per >= 50 %.

| segmento | braccio | sopra soglia | dopo area | dopo bordo | **dopo scarto** |
|---|---|---|---|---|---|
| `20251028213516` | A nativo 8,64 µm | 285/348 | 2/3 | 2/3 | **2/3** |
|  | B a 9,362 µm | 259/285 | 0/2 | 0/2 | **0/2** |
| `20251028220042` | A nativo 8,64 µm | 323/261 | 4/2 | 4/2 | **4/2** |
|  | B a 9,362 µm | 228/228 | 8/1 | 8/1 | **8/1** |
| `20251028220955` | A nativo 8,64 µm | 351/383 | 5/7 | 4/5 | **4/5** |
|  | B a 9,362 µm | 297/315 | 3/5 | 3/4 | **3/4** |
| `20251028222030` | A nativo 8,64 µm | 361/446 | 1/1 | 1/0 | **1/0** |
|  | B a 9,362 µm | 331/357 | 1/1 | 1/1 | **1/1** |
| `20251028225813` | A nativo 8,64 µm | 350/356 | 0/0 | 0/0 | **0/0** |
|  | B a 9,362 µm | 349/304 | 1/1 | 1/1 | **1/1** |
| `20251029010146` | A nativo 8,64 µm | 44/35 | 0/0 | 0/0 | **0/0** |
|  | B a 9,362 µm | 75/85 | 1/0 | 0/0 | **0/0** |

**Totali** — A: **11 avanti / 10 inversi**; B: **13 avanti / 9 inversi**.

Per confronto, il controllo positivo w035 con gli stessi criteri: **90 avanti / 39 inversi**, rapporto 2,31. Qui: 1.10 e 1.44.
