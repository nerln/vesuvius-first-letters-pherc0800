# A First Letters null on PHerc. 0800, a null on PHerc. MANBp, and why no automatic count decides it

The public cross-scroll ink model (`ink_9um`, `hybrid_3d2d-seed43/step-060000`) was run on
every published segment of PHerc. 0800 — six segments, at the native 8.64 µm and resampled
to 9.362 µm — and on the nine published wraps of PHerc. MANBp, rendered from their meshes at
9.596 µm (34.0 cm² of surface). In none of them does stroke-like structure appear in the
forward panel (the model reading the surface volume in its usual depth order) that is absent
from the reverse one (the same volume read back to front, where ink should not show). All panels are in `pherc0800/` and `manbp/`.

That is about these segments, scales and model, not a claim that either scroll has no ink.
PHerc. 0800 is in the First Letters set, with volume `20250521135224`, the one read here; PHerc.
MANBp is not in that set ([eligibility list](https://github.com/ScrollPrize/villa/blob/75c79ac5f506d4b9a89bcfbef8e8c0f2f0c3acb3/scrollprize.org/src/data/prizeEligibility.json), as updated on 24 September in
[villa#1887](https://github.com/ScrollPrize/villa/pull/1887)).

This null is for the public `ink_9um` checkpoint only. On 24 September the Challenge announced,
in its Discord #announcements channel, a new 9 µm ink-detection recipe that finds letters on
PHerc. 1447, which villa#1887 took off the First Letters list the same day; its model was not released at the time of writing, and this run says nothing about what it
would find on PHerc. 0800 or PHerc. MANBp.

## The control, first

On PHerc. 0139 w035, a training segment, the same pipeline brings out the Greek letters its
labels mark (`control/`): AUC 0.997 on labelled pixels, 0.592 in reverse. That shows the
pipeline works, not how well it reads an unread scroll.

## Who judged, and how blind

The MANBp panels, shuffled with two lettered controls and unlabelled, went to two AI readers:
one with no context, and the agent that made them, which published a hash of its verdicts
(`blind-reading/reader-B.sha256`) before reading the other's. Both called both controls "letters" and all nine wraps "nothing" (`blind-reading/`).

## What we learned that others will hit

We tried to make the verdict automatic, and **four criteria failed, each with numbers**:

| criterion | why it fails |
|---|---|
| forward vs reverse candidate count | a brightness offset between the two maps turns into "N vs 0" |
| forward/reverse ratio | control 1.33 sits inside the targets' 1.18–1.38 |
| candidate density | blank segments fall on both sides of the lettered ones |
| blob shape | a blank segment's blotches are at least as elongated as real letters |

One fix even removed a real letter of the control (overlap 0.525), so that check is now only a
diagnostic. The pipeline yields **candidates, not verdicts**; the verdict is visual.

## Files

`PREREGISTRATION.md`: what was fixed before looking and what changed after, dated, in English
(`G0.md` is the Italian original). `ERRATA.md`: what was wrong. `python3 reproduce.py`
recomputes every number here from the raw output and exits 1 on a mismatch.

Costs: PHerc. 0800, 174 s network and 491 s GPU on an RTX 2070 SUPER; PHerc. MANBp, 34 minutes
on an Apple Silicon Mac, render included.
