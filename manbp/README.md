# PHerc. MANBp

`run.sh` renders each of the nine wraps from its published mesh and reads it with the public ink model, with the flags used here: `VILLA_BIN=… CKPT=… bash run.sh w3` for one wrap, no argument for all nine, `DRY=1` to print the commands.
The panels (`w*_forward_reverse.png`), per-wrap analyses and timings, and the measured areas (`areas.json`, `measure_areas.py`) are the outputs of that run; `meshes/` keeps each mesh's `meta.json`.
Which builds were used is in `../PREREGISTRATION.md`, section «What was run».
