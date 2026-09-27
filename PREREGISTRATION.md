# Pre-registration, in English

`G0.md` is the pre-registration as it was written, in Italian, with every entry dated. It is
kept unedited because it is a record. This page says, in English, what was fixed **before**
any target was looked at and what was changed **after** looking at data — with the date and
the reason for each change. Times are copied from the dated headers of `G0.md`,
Central European Summer Time, September 2026.

## Terms

- **First Letters**: the Vesuvius Challenge prize category for finding ink on a scroll where
  none has been reported.
- **forward / reverse**: the ink model reads the surface volume in both depth orders; ink
  should appear in one and not the other.
- **surface volume**: the stack of slices rendered around a traced papyrus surface. The
  Challenge publishes these for some segments; for others it publishes only the mesh.
- **candidate**: a connected blob above threshold, large enough and away from the edge.
- **w035, w029, w0 …**: segment names as published on the Challenge's data server.
- **the NUC / the Mac**: the two machines the runs were done on (a Windows mini-PC with an
  RTX 2070 SUPER, and an Apple Silicon Mac).

## What was run

| what | value |
|---|---|
| MANBp render | `vc_render_tifxyz` built from villa `main` at `d285029ab` (the same build as the L1 replication: sha256 `d813ddb1703a0ca569ced24867dcb9b66e50426692ebeb4ed7201af4da70f3f3`, listed in that repository's HASHES.md) |
| MANBp inference | on the Mac's GPU (MPS) rather than the NUC's CUDA, with villa's `vesuvius` package at `78beac819`: `main` `d285029ab` plus the single change of [villa#1865](https://github.com/ScrollPrize/villa/pull/1865), which lets the automatic device choice pick MPS (that PR measured CPU and MPS predictions within one grey level in 255). Same model, same reading criteria, same flags except the batch size, below |
| **deviation, 22 Sep 18:43** | the Mac runs used `--batch-size 8`, not the 32 frozen at 17:50 and restated for MANBp at 18:33. No reason was recorded when the change was made, at w0's inference. On the gate, batch 8 and 32 give AUC 0.997211 and 0.997213 (`G0.md`, 22 Sep 17:50): the batch size changes the run time, not the result at the precision reported here |
| MANBp commands | the ones in `manbp/run.sh`. w1–w8 ran through the original script on 23 Sep, 10:54:20–11:18:57. w0 ran first, by hand, on 22 Sep (inference 18:43–18:44), with the same two commands and the same package |
| PHerc. 0800 inference | on the NUC; each segment's full command is in `pherc0800/*/rapporto.json` |

## Fixed before any target was looked at (22 Sep, from 16:38)

| what | value |
|---|---|
| question | does the public cross-scroll ink model show ink on scrolls with no published ink result? |
| target filter 1 | not one of the four training scrolls (PHerc. 0139, 1667, Paris 4, 0814) |
| target filter 2 | has published segments in the Challenge's bucket |
| target filter 3 | `stages.ink = false` in the Challenge's data browser on 22 Sep |
| target filter 4 | a resolution the model can read (about 9 µm) |
| model | `ink_9um`, `hybrid_3d2d-seed43/step-060000`, sha256 `bf229faf…5525d270` |
| gate | PHerc. 0139 w035, a training segment, must reach AUC ≥ 0.85 against its published labels; if not, no target runs |
| reading | threshold 0.5; both depth orders; a border band excluded; no selection after looking |
| minimum size | the smallest labelled letter on w035, measured before any target; a contingency, written in advance, lowers it to the smallest true-positive blob if predictions are thinner than labels |
| outcome | a null is published |

## Changed after looking at data, and why

| when | change | reason |
|---|---|---|
| 22 Sep 17:50 | gate passed: AUC 0.997213; batch size frozen at 32 | measured on the gate segment, before any target |
| 22 Sep 18:09 | minimum size 15,011 → **12,000 px** | the pre-written contingency fired: the smallest true-positive blob on w035 was 12,083 px, and at 15,011 one real letter vanished |
| 22 Sep 18:09 | target order changed; **PHerc. 0800 first** | the first two targets had no published surface volumes; 0800 was the only target passing all four filters with volumes ready. Filter 3 was kept: five scrolls with volumes ready were excluded because ink had already been reported |
| 22 Sep 18:09 | a second arm on 0800, resampled to 9.362 µm | declared before running: 8.64 µm is not a training scale, so the resampled arm tests whether scale matters |
| 22 Sep 18:33 | MANBp rendered at **level 2 of the 2.399 µm scan** (9.596 µm), not level 3 of the 1.129 µm scan | the mesh's own metadata (`area_vx2` / `area_cm2`) puts it in the 2.399 µm frame; the other scan would have sampled at coordinates off by a factor of 2.1 |
| 22 Sep 18:48 | the forward-vs-reverse count was found to mistake brightness for structure | on MANBp w0 the forward map was brighter: 19 candidates against 0, becoming 19 against 21 at matched lit fraction |
| 22 Sep 19:07 | **no automatic verdict** | four criteria — count, ratio, density, shape — each failed with numbers, and the overlap filter removed a real letter on w035. The pipeline yields candidates; the verdict is visual |
| 22 Sep 19:08 | visual reading protocol | panels shuffled with a control and unlabelled; readers record a verdict before seeing each other's; a fixed sentence for a null |
| 22 Sep 21:14 | duplicate MANBp wraps w6 and w7 chosen by `date_last_modified`, not by the folder name | the name is the creation date; the rule "use the most recent" meant the one last modified. One of the pair also had a truncated `meta.json` |
| 23 Sep 11:07 | density denominator unified | see `ERRATA.md`, entry 4 |
| 23 Sep 11:08 | **PHerc. 0332 excluded** | its segments are in the 2023 frame and the only volume is from 2025. The public `transform.json` rests on six landmarks, median residual 14.6 legacy voxels (about 115 µm, max 16.9), spanning z 1279–4491 while the segments lie at z 5003–7994, and only 247 voxels in y. A render could land on the neighbouring sheet, and no label-free check tells that apart. See [villa#1835](https://github.com/ScrollPrize/villa/issues/1835) and [villa#1843](https://github.com/ScrollPrize/villa/issues/1843), which report a 103.1 µm residual for the same transform |
| 23 Sep 11:21 | MANBp surface reported as **34.0 cm² actually rendered and read**, not the 49.0 cm² the `meta.json` files declare | measured from the published geometry: for five of eleven exports `area_cm2` overstates what the tifxyz contains (w6: 13.1 declared, 2.17 present). The w6/w7 choice stands; measured, it lost nothing on w6 and left about 1 cm² unread on w7 |

Every change above is also in `G0.md`, in Italian, at the time it was made.
