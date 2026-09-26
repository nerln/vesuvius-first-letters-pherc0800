#!/usr/bin/env python3
"""Measure the 3D surface area of a published tifxyz: sum of the valid quads' areas.
    python3 measure_areas.py <folder with x.tif y.tif z.tif> [um_per_voxel=2.399]
Validated: on four MANBp wraps it matches meta.json's area_cm2 to the hundredth."""
import sys, numpy as np, tifffile
d = sys.argv[1]; um = float(sys.argv[2]) if len(sys.argv) > 2 else 2.399
X, Y, Z = [tifffile.imread(f"{d}/{c}.tif").astype(np.float64) for c in "xyz"]
P = np.stack([X, Y, Z], -1); v = (X > 0) & (Y > 0) & (Z > 0)
q = v[:-1, :-1] & v[1:, :-1] & v[:-1, 1:] & v[1:, 1:]
a, b, c, e = P[:-1, :-1], P[1:, :-1], P[:-1, 1:], P[1:, 1:]
t = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=-1) + 0.5 * np.linalg.norm(np.cross(b - e, c - e), axis=-1)
print(f"{float((t * q).sum()) * (um * 1e-4) ** 2:.3f} cm2")
