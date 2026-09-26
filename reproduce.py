#!/usr/bin/env python3
"""Recompute every number in README.md from the raw files in data/. No network, no model.

    python3 reproduce.py

Exits 1 if a README claim does not match the raw data. Raw files are published exactly as
they came off the machine that produced them; where one contradicts itself, this script
says so and points to ERRATA.md instead of editing the file.
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
def load(name):
    return json.loads(io.open(os.path.join(D, name), encoding="utf-8-sig").read())

fail, warn = [], []
def check(label, got, want):
    ok = got == want
    print(f"  {'ok ' if ok else 'BAD'} {label}: {got}" + ("" if ok else f"  (README says {want})"))
    if not ok: fail.append(label)

# ---------------------------------------------------------------- positive control, w035
print("Positive control: PHerc0139 w035, published surface volume, public ink_9um seed43")
fw, rv = load("NUC-auc-avanti-b32.json"), load("NUC-auc-inversa.json")
check("AUC forward, supervised pixels", round(fw["auc_supervision"]["auc"], 6), 0.997213)
check("AUC forward, occupancy",        round(fw["auc_occupancy"]["auc"], 6),   0.955024)
check("AUC forward, full frame",       round(fw["auc_full_frame"]["auc"], 6),  0.961406)
check("AUC reverse, supervised pixels", round(rv["auc_supervision"]["auc"], 6), 0.592042)

t = load("NUC-taratura-w035-12000.json")
b = t["contingenza_regola_1"]["definizione_b_blob_abbinato_per_lettera"]
check("annotated letters", t["lettere_annotate"], 13)
check("letters found by a forward candidate (>=50% covered)",
      t["lettere_ritrovate_dai_candidati_avanti(>=50% coperta)"], 12)
check("smallest labelled letter, px", t["aree_lettere"]["min"], 15011)
check("smallest known true positive blob, px", b["area_minima"], 12083)
check("minimum candidate area in use, px", t["area_min_usata"], 12000)

# the file's own verdict string must agree with its own numbers
esito = t["contingenza_regola_1"]["esito"]
if b["area_minima"] < t["aree_lettere"]["min"] and "resta a 15.011" in esito:
    warn.append("NUC-taratura-w035-12000.json: the 'esito' string says the size rule stayed at "
                "15,011 px, but the same file shows the smallest true positive is "
                f"{b['area_minima']} px and the rule in use is {t['area_min_usata']} px. "
                "The numbers are right, the string is stale: see ERRATA.md.")

s = load("NUC-regola2-scartati-w035.json")
n_fwd = s["candidati_avanti"]
old, new = s["vecchia"], s["nuova"]
check("forward candidates before the overlap check", n_fwd, 92)
check("old rule: forward after overlap / reverse", (n_fwd - len(old["scartati"]), old["candidati_inversi"]), (90, 39))
check("new rule: forward after overlap / reverse", (n_fwd - len(new["scartati"]), new["candidati_inversi"]), (89, 67))
check("true letters removed by the overlap check, old rule", old["scartati_che_sono_lettere_vere"], 0)
killed = [x for x in new["scartati"] if x["e_una_lettera_vera"]]
check("true letters removed by the overlap check, new rule", len(killed), 1)
if killed:
    k = killed[0]
    check("  that letter: overlap with a reverse candidate", k["sovrapposizione_con_inverso"], 0.525)
    check("  that letter: labelled-ink pixels inside it", k["pixel_di_inchiostro_dentro"], 6043)

# ---------------------------------------------------------------- targets, PHerc0800
print("\nTargets: PHerc0800, six published segments, two scales")
r = load("NUC-regola2-rianalisi-0800.json")
check("segments", len(r), 6)
tot = {}
for arm in ("A_nativo", "B_9362"):
    o = [0, 0]; n = [0, 0]
    for seg in r.values():
        o[0] += seg[arm]["vecchia"]["finale_avanti"]; o[1] += seg[arm]["vecchia"]["finale_inversi"]
        n[0] += seg[arm]["nuova"]["finale_avanti"];   n[1] += seg[arm]["nuova"]["finale_inversi"]
    tot[arm] = (tuple(o), tuple(n))
check("native 8.64 um: old rule forward/reverse", tot["A_nativo"][0], (11, 10))
check("native 8.64 um: new rule forward/reverse", tot["A_nativo"][1], (11, 8))
check("resampled 9.362 um: old rule forward/reverse", tot["B_9362"][0], (13, 9))
check("resampled 9.362 um: new rule forward/reverse", tot["B_9362"][1], (13, 11))

ctrl_ratio = round(89 / 67, 2)
tgt = [round(a / b, 2) for (a, b) in (tot["A_nativo"][1], tot["B_9362"][1])]
print(f"\n  forward/reverse ratio, new rule: control {ctrl_ratio}, targets {tgt}")
if min(tgt) <= ctrl_ratio <= max(tgt):
    print("  -> the control sits inside the targets' range: the count does not decide. "
          "(This is a finding the README states, not a failure of this script.)")
else:
    fail.append("README says the control ratio sits inside the targets' range; it does not")

# ---------------------------------------------------------------- costs, from the per-segment reports
import glob
net = gpuA = gpuB = 0.0
for f in sorted(glob.glob(os.path.join(HERE, "pherc0800", "*", "rapporto.json"))):
    x = json.loads(io.open(f, encoding="utf-8-sig").read())
    net  += x["rete"]["secondi"]
    gpuA += x["braccio_A_nativo"]["secondi_calcolo"]
    gpuB += x["braccio_B_9362"]["secondi_calcolo"]
print("\nCosts, PHerc0800, summed over the six per-segment reports")
check("network seconds", round(net), 174)
check("GPU seconds, both arms", round(gpuA + gpuB), 491)

# ---------------------------------------------------------------- why no automatic criterion decides
# Recomputed from the prediction maps in data/maps/, at the unified threshold (>= 128 on uint8).
import numpy as np, tifffile
from scipy import ndimage as ndi
T, AREA, BORDER = 128, 12000, 64
def candidates(m, thr):
    lab, k = ndi.label(m >= thr); ar = np.bincount(lab.ravel())[1:] if k else np.array([])
    H, W = m.shape; out = []
    for i in range(1, k + 1):
        if ar[i - 1] < AREA: continue
        ys, xs = np.where(lab == i)
        if ys.min() >= BORDER and xs.min() >= BORDER and ys.max() < H - BORDER and xs.max() < W - BORDER:
            out.append(i)
    return lab, out
def shape(lab, idx):
    fill, slen, ecc = [], [], []
    for i in idx:
        b = lab == i; ys, xs = np.where(b); a = len(ys)
        fill.append(a / ((np.ptp(ys) + 1) * (np.ptp(xs) + 1)))
        per = (b ^ ndi.binary_erosion(b)).sum(); slen.append(per * per / a)
        yc, xc = ys.mean(), xs.mean(); yy = ((ys - yc) ** 2).mean(); xx = ((xs - xc) ** 2).mean()
        xy = ((xs - xc) * (ys - yc)).mean(); tr = yy + xx; d = max(tr * tr / 4 - (yy * xx - xy * xy), 0) ** 0.5
        l1, l2 = tr / 2 + d, max(tr / 2 - d, 1e-9); ecc.append((1 - l2 / l1) ** 0.5)
    return round(float(np.median(fill)), 3), round(float(np.median(slen)), 1), round(float(np.median(ecc)), 3)

occ = load("occupancy.json")
MP = os.path.join(D, "maps")
res = {}
for name in ("manbp_w0", "pherc0139_w029"):
    A = tifffile.imread(os.path.join(MP, name + "_forward.tif"))
    Rv = tifffile.imread(os.path.join(MP, name + "_reverse.tif"))
    valid = (A > 0) | (Rv > 0)
    labA, cA = candidates(A, T); _, cR = candidates(Rv, T)
    fa = (A[valid] >= T).mean(); thr_m = np.percentile(Rv[valid], 100 * (1 - fa)); _, cRm = candidates(Rv, thr_m)
    mpx = A.size / 1e6 * occ[name]["fraction"]
    res[name] = dict(fwd=len(cA), rev_abs=len(cR), rev_matched=len(cRm),
                     density=round(len(cA) / mpx, 2), shape=shape(labA, cA))
w035_density = round(90 / (5820 * 5240 / 1e6 * occ["pherc0139_w035"]["fraction"]), 2)

print("\nWhy no automatic criterion decides (maps in data/maps/, threshold >= 128)")
w0, w29 = res["manbp_w0"], res["pherc0139_w029"]
check("MANBp w0, forward vs reverse at absolute threshold", (w0["fwd"], w0["rev_abs"]), (19, 0))
check("MANBp w0, forward vs reverse at matched lit fraction", (w0["fwd"], w0["rev_matched"]), (19, 21))
check("0139 w029 (ink), forward vs reverse at matched lit fraction", (w29["fwd"], w29["rev_matched"]), (6, 1))
# PHerc0800, same denominator: occupancy and render size read from the inference log tails
import re
d0800 = {}
for arm in ("braccio_A_nativo", "braccio_B_9362"):
    n = mpx = 0.0
    for f in sorted(glob.glob(os.path.join(HERE, "pherc0800", "*", "rapporto.json"))):
        x = json.loads(io.open(f, encoding="utf-8-sig").read())[arm]
        occ = float(re.findall(r"nonempty_coverage=([0-9.]+)%", x["log_coda"])[-1]) / 100
        h, w = map(int, re.findall(r"shape=\(depth=\d+, height=(\d+), width=(\d+)\)", x["log_coda"])[-1])
        n += x["tabella_G0"]["dopo_scarto_inverso"]["avanti"]; mpx += h * w * occ / 1e6
    d0800[arm] = round(n / mpx, 2)
print("  density per occupied Mpx (candidates / area the inference found non-empty):")
print(f"    with letters: w035 {w035_density}, 0139 w029 {w29['density']}")
print(f"    without:      PHerc0800 {d0800['braccio_A_nativo']} and {d0800['braccio_B_9362']}, MANBp w0 {w0['density']}")
if not (min(d0800.values()) < min(w035_density, w29["density"]) < max(w035_density, w29["density"]) < w0["density"]):
    fail.append("README implies blank targets fall on both sides of the lettered controls in density")
if not (w0["density"] >= w035_density and w0["density"] >= w29["density"]):
    fail.append("README says the no-letter target's density is at least as high as both controls")
print(f"  shape (fill, slenderness, eccentricity): 0139 w029 {w29['shape']}, MANBp w0 {w0['shape']}")
if not (w0["shape"][2] >= w29["shape"][2]):
    fail.append("README says the target's blotches are at least as elongated as real letters")

# ---------------------------------------------------------------- PHerc. MANBp, nine wraps
print("\nTargets: PHerc. MANBp, nine wraps rendered from their meshes at 9.596 um")
ar = json.loads(io.open(os.path.join(HERE, "manbp", "areas.json"), encoding="utf-8").read())
wr = ar["wraps"]
check("wraps", len(wr), 9)
check("surface actually published and read, cm2", round(sum(w["measured_cm2"] for w in wr.values()), 2), 34.03)
check("surface the meta.json files declare, cm2", round(sum(w["declared_cm2"] for w in wr.values()), 2), 49.0)
for n in sorted(wr):
    a = json.loads(io.open(os.path.join(HERE, "manbp", f"{n}-analysis.json"), encoding="utf-8").read())
    t = a["tabella_G0"]["dopo_scarto_inverso"]
    print(f"  {n}: {wr[n]['measured_cm2']:.2f} cm2, candidates forward {t['avanti']} / reverse {t['inversi']} "
          f"at matched lit fraction (threshold {a['offset']['soglia_inverso_pareggiata']})")
    if not os.path.exists(os.path.join(HERE, "manbp", f"{n}_forward_reverse.png")):
        fail.append(f"panel for MANBp {n} missing")


tt = sum(json.loads(io.open(os.path.join(HERE, "manbp", f"{n}-timing.json"), encoding="utf-8").read())["render_s"]
         + json.loads(io.open(os.path.join(HERE, "manbp", f"{n}-timing.json"), encoding="utf-8").read())["inferenza_s"] for n in sorted(wr))
check("MANBp render + inference, minutes", round(tt / 60), 34)

# ---------------------------------------------------------------- the blind reading
import hashlib, re as _re
print("\nBlind reading: 11 shuffled panels (9 MANBp wraps + 2 lettered controls), two readers")
BR = os.path.join(HERE, "blind-reading")
key = json.loads(io.open(os.path.join(BR, "key.json"), encoding="utf-8").read())
def verdicts(f):
    d = {}
    for l in io.open(os.path.join(BR, f), encoding="utf-8"):
        m = _re.match(r"\s*(pannello-\d\d)\s*:\s*(lettere|niente)", l, _re.I)
        if m: d[m.group(1) + ".png"] = m.group(2).lower()
    return d
A, Bv = verdicts("reader-A.txt"), verdicts("reader-B.txt")
sha = hashlib.sha256(open(os.path.join(BR, "reader-B.txt"), "rb").read()).hexdigest()
sealed = open(os.path.join(BR, "reader-B.sha256")).read().split()[0]
check("reader B's file is the one sealed before opening reader A's", sha == sealed, True)
check("panels", len(key), 11)
check("readers agree", sum(A[p] == Bv[p] for p in key), 11)
ctrl = [p for p, v in key.items() if v.startswith("CONTROLLO")]
check("controls called 'letters' by both readers", sum(A[p] == "lettere" and Bv[p] == "lettere" for p in ctrl), 2)
check("MANBp wraps called 'nothing' by both readers", sum(A[p] == "niente" and Bv[p] == "niente" for p in key if p not in ctrl), 9)

print()
for w in warn: print("WARNING:", w)
if fail:
    print("MISMATCH:"); [print("  -", f) for f in fail]; sys.exit(1)
print("Every README number matches data/." + (" One known erratum, see above." if warn else ""))
