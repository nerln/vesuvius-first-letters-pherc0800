#!/bin/bash
# PHerc. MANBp: render a wrap from its published mesh, then read it with the public ink model.
# Same flags as the run published here (w1-w8 on 23 Sep 2026; w0 on 22 Sep). No analysis step:
# the numbers in the README are recomputed from data/ by ../reproduce.py.
#
#   VILLA_BIN=/path/to/vc_render_tifxyz CKPT=/path/to/step-060000.pth bash run.sh w3
#   (no wrap name = all nine; DRY=1 prints the commands without running them)
set -eu

VILLA_BIN=${VILLA_BIN:?vc_render_tifxyz, built from villa main at d285029ab for this run}
CKPT=${CKPT:?ink_9um/hybrid_3d2d-seed43/step-060000.pth}
OUT=${OUT:-./manbp-out}
PY=${PY:-python3}
# villa/vesuvius/src. This run used 78beac819 (main d285029ab plus #1865), whose automatic
# device choice picks MPS on Apple Silicon; on main at d285029ab the same command runs on CPU.
VESUVIUS_SRC=${VESUVIUS_SRC:-}
DRY=${DRY:-0}

B=https://vesuvius-challenge-open-data.s3.amazonaws.com
VOL=s3://vesuvius-challenge-open-data/PHercMANBp/volumes/20251216152116-2.399um-0.2m-78keV-masked.zarr/
# w6 and w7 each have two exports; the one last modified is used (PREREGISTRATION.md, 22 Sep 21:14).
WRAPS="w0:20251218010446-w0_20251218010446110
w1:20251217233843-w1_20251217233843496
w2:20251217234605-w2_20251217234605189
w3:20251218211706-w3_20251218211706689
w4:20251218212128-w4_20251218212128406
w5:20251218212713-w5_20251218212713988
w6:20251220015639-w6_20251220015639809
w7:20251222223312-w7_20251222223312675
w8:20251219211451-w8_20251219211451561"

run() { if [ "$DRY" = 1 ]; then echo "$*"; else "$@"; fi; }

for e in $WRAPS; do
  n=${e%%:*}; s=${e#*:}
  [ $# -gt 0 ] && [ "$1" != "$n" ] && continue
  run mkdir -p "$OUT/mesh/$n"
  for f in meta.json x.tif y.tif z.tif; do
    run curl -sfL -o "$OUT/mesh/$n/$f" "$B/PHercMANBp/segments/$s/mesh/intermediate/tifxyz_original/$f"
  done
  run "$VILLA_BIN" --volume "$OUT/cache/manbp-2399.zarr" --remote-url "$VOL" \
      --segmentation "$OUT/mesh/$n" --zarr-output "$OUT/$n.zarr" \
      --scale 1 --group-idx 2 --num-slices 31 --slice-step 1 --flip-normals --cache-gb 2
  # --batch-size 8 is what ran; the value frozen on the NUC was 32 (PREREGISTRATION.md,
  # «What was run», deviation of 22 Sep 18:43; on the gate the two give the same AUC to 5 decimals).
  run env PYTHONPATH="$VESUVIUS_SRC" "$PY" -m vesuvius.ink_detection.inference.infer \
      "$OUT/$n.zarr" "$CKPT" "$OUT/$n-pred.tif" \
      --overlap 0.5 --blend-mode hann --direction both --batch-size 8 --no-compile
  # The render (about 150 MB) is not needed once the prediction exists.
  run rm -rf "$OUT/$n.zarr"
done
