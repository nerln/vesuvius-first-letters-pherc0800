# Errata

Raw files in `data/` are published as the machine that produced them wrote them. When one is
wrong, the record of it stays here even after it is fixed.

## 1. A stale verdict string in the calibration file — fixed at the source

`data/NUC-taratura-w035-12000.json`, field `contingenza_regola_1.esito`, first said the size
rule "stays at 15,011", while the numbers in the same file showed the smallest true positive
at 12,083 px and the rule in use at 12,000 px.

**Cause**, found by the machine that produced it: its script compared the contingency against
the area used in the run instead of against the original 15,011-px rule, so a run at 12,000
wrote "stays at 15,011". The script was fixed and both calibration files regenerated; all
other numbers were identical. **The published file is the corrected one.**

## 2. Two defects in the first blind reading (the PHerc. 0800 panels, 22 Sep)

- The panel titles were cropped at a fixed 8.5 % of the height. On the positive-control panel
  that left the candidate counts visible, so **on that one panel the reading was not blind**.
  The crop is now computed from the image.
- The second reader received the first reader's verdict before recording their own. So only
  **one** target panel (`20251028220042`, 9.362 µm arm) has two independent concordant
  readings; the other eleven have one blind reader each.

The MANBp reading in `blind-reading/` (23 Sep) was set up after both were found: titles
cropped from the image content, a first reader with no context at all, and the second
reader's verdicts hashed before it read the first's.

## 3. Threshold convention

The 0.5 threshold on uint8 maps was applied as ≥ 128 on one machine and ≥ 127 on the other.
Everything published here is at **≥ 128**. For the two pairs of maps in `data/maps/`, recounting at ≥ 127 changes nothing; the other machine's counts were not recomputed at ≥ 127.

## 4. Candidate density was computed with three different denominators on different days

"Candidates per Mpx" appears in this repository with three denominators:

| file | denominator | w035 (letters) | MANBp w0 (no letters) |
|---|---|---|---|
| `pherc0800/RAPPORTO-NUC.md` | whole render, including empty canvas | 2.95 | — |
| `G0.md`, entry of 22 Sep | map pixels that are non-zero | 3.55 ¹ | 3.72 |
| `README.md`, `reproduce.py` | area the inference scanned as non-empty | **3.55** | **4.59** |

¹ `G0.md` used the inference occupancy for w035 and the non-zero map pixels for w0: two
denominators in one table. That mix is corrected here, not in `G0.md`, which is kept as it
was written on that day.

**The README uses the last one, and only that.** It counts area where there is a surface.
The whole-render denominator does not: MANBp w0's render is about 69 % empty canvas, and
dividing by it puts w0 at 1.44 per Mpx, *below* both lettered segments — a reversal that
comes from the empty canvas, not from the papyrus. Under both surface-area denominators the
no-letter segment is at least as dense as the lettered ones, and PHerc. 0800 (0.87, 1.20) is
well below them: the blank segments fall on **both** sides of the lettered ones, which is
the point.
