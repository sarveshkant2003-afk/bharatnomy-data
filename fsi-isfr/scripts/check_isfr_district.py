"""Checks for fsi-isfr_forest-cover_district_2023.csv. Prints results; never changes data."""
import csv, os, random
DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
rows = list(csv.DictReader(open(os.path.join(DIR, "fsi-isfr_forest-cover_district_2023.csv"))))
f = lambda r, c: float(r[c])
keys = [(r["state_ut"], r["district"]) for r in rows]
print(f"{len(rows)} rows x {len(rows[0])} cols; {len({k[0] for k in keys})} states; duplicates {len(keys) - len(set(keys))}")
num = [c for c in rows[0] if c.endswith(("_sq_km", "_pct_of_area"))]
print("negative (other than change):", [(r["district"], c) for r in rows for c in num if c != "change_since_2021_sq_km" and f(r, c) < 0])
bad = [(r["state_ut"], r["district"]) for r in rows
       if abs(f(r, "very_dense_forest_sq_km") + f(r, "moderately_dense_forest_sq_km") + f(r, "open_forest_sq_km") - f(r, "forest_cover_total_sq_km")) > 0.05]
print("VDF+MDF+OF = total:", "ok" if not bad else bad)
bad = [(r["state_ut"], r["district"], r["forest_cover_pct_of_area"]) for r in rows
       if abs(100 * f(r, "forest_cover_total_sq_km") / f(r, "geographical_area_sq_km") - f(r, "forest_cover_pct_of_area")) > 0.05]
print("pct = total / area (within 0.05):", "ok" if not bad else bad)
print("pct within 0-100:", all(0 <= f(r, "forest_cover_pct_of_area") <= 100 for r in rows))
for s in sorted({k[0] for k in keys}):
    d = [r for r in rows if r["state_ut"] == s and r["district"] != "State total"]
    t = next(r for r in rows if r["state_ut"] == s and r["district"] == "State total")
    diffs = {c: round(sum(f(r, c) for r in d) - f(t, c), 2) for c in num if c != "forest_cover_pct_of_area"}
    diffs = {c: v for c, v in diffs.items() if abs(v) > 0.1}
    if diffs:
        print(f"districts vs State total, {s}: {diffs}")
random.seed(3)
for r in random.sample(rows, 5):
    print("spot:", r["state_ut"], "|", r["district"], "|", " ".join(r[c] for c in num))
