"""Build _reference/variables.csv (and a minimal variables.xlsx) from the climate variable sheets' log.

Variables are the ones in the four climate variable sheets, named exactly as in the sheets
(_reference/variables-draft.csv, one row per sheet row). This script
  1. writes each sheet variable's lens and sub-theme (from SUB_THEMES below) into variables-draft.csv;
  2. writes variables.csv with the sheet variables that have data (status found or partial), one row per
     variable name (a name used in two sheets appears once).

Run from the repo root:  python3 pipelines/reference/build_variables.py
Then:                     python3 tools/build_catalog.py   (validates and writes registry.json)
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / "_reference/variables-draft.csv"
OUT = ROOT / "_reference/variables.csv"
FIELDS = ["variable_id", "name", "lens_id", "sub_theme_id", "dataset", "column", "unit", "geo_level",
          "frequency", "earliest_period", "latest_period", "type"]

# Sub-theme of every sheet row: {sheet: {sub-theme: [serial numbers]}}
SUB_THEMES = {
    "air_quality": {
        "CAR-AIR": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 22, 23, 24],
        "EPM-DEMAND": [18], "EPM-ACCESS": [20, 21], "CAR-HEALTH": [25, 26],
        "CAR-GOV": [27, 28, 29], "CAR-LAND": [30],
    },
    "heat_climate_resilience": {
        "CAR-HEAT": [1, 2, 3, 4, 5, 6, 7, 10], "CAR-RAIN": [8, 9], "CAR-AIR": [11],
        "CAR-EXPOSURE": [12, 13, 18, 19, 20, 27, 28], "MAC-LABOUR": [14, 15, 16, 44], "MAC-AGRI": [17, 46, 47],
        "CAR-HOUSING": [21], "CAR-WATER": [22, 30, 49], "EPM-ACCESS": [23, 24],
        "CAR-HEALTH": [25, 31, 32, 36, 38], "MAC-WELFARE": [26, 37, 39, 50], "CAR-LAND": [29],
        "CAR-GOV": [33, 34, 35], "CAR-MORTALITY": [40, 41, 42], "EPM-DEMAND": [43], "COM-CROPS": [45],
        "MAC-INDUSTRY": [48],
    },
    "rainfall": {
        "CAR-RAIN": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 24, 25, 26, 27, 36],
        "CAR-WATER": [20, 21, 22, 23, 37, 38, 39], "CAR-WIND": [28], "CAR-MORTALITY": [29, 30, 31],
        "COM-WEATHER": [32], "CAR-EXPOSURE": [33], "CAR-HOUSING": [34], "CAR-LAND": [35, 41],
        "MAC-AGRI": [40], "CAR-GOV": [42, 43],
    },
    "wind": {
        "CAR-WIND": [1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14], "EPM-RENEW": [6, 7, 8], "CAR-AIR": [15],
        "CAR-EXPOSURE": [16, 17], "CAR-HOUSING": [18, 19], "CAR-LAND": [20, 21], "CAR-GOV": [22, 23],
        "CAR-MORTALITY": [24, 25, 27], "EPM-DEMAND": [26],
    },
}
HAS_DATA = {"found": 0, "partial": 1}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    lenses = {r["sub_theme_id"]: r["lens_id"] for r in csv.DictReader(open(ROOT / "_reference/lenses.csv", encoding="utf-8"))}
    where = {(sh, str(n)): st for sh, m in SUB_THEMES.items() for st, ns in m.items() for n in ns}
    with open(DRAFT, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        fields, rows = list(r.fieldnames), list(r)
    for c in ("lens_id", "sub_theme_id"):
        if c not in fields:
            fields.insert(fields.index("variable_name") + 1, c) if c == "lens_id" else fields.insert(fields.index("lens_id") + 1, c)
    missing = []
    for row in rows:
        st = where.get((row["sheet"], row["sno"]))
        if not st:
            missing.append((row["sheet"], row["sno"], row["variable_name"]))
        row["sub_theme_id"], row["lens_id"] = st or "", lenses.get(st, "")
    if missing:
        raise SystemExit(f"sheet rows without a sub-theme in SUB_THEMES: {missing}")
    with open(DRAFT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    best = {}
    for row in rows:
        if row["status"] not in HAS_DATA or not row["dataset"]:
            continue
        name = row["variable_name"]
        if name not in best or HAS_DATA[row["status"]] < HAS_DATA[best[name]["status"]]:
            best[name] = row
    out = []
    for name, row in best.items():
        source = row["dataset"].split("_")[4] if row["dataset"].count("_") >= 4 else ""
        out.append({
            "variable_id": slug(name), "name": name, "lens_id": row["lens_id"], "sub_theme_id": row["sub_theme_id"],
            "dataset": row["dataset"], "column": row["column"], "unit": row["unit"], "geo_level": row["geo_level"],
            "frequency": row["frequency"], "earliest_period": row["earliest_period"], "latest_period": row["latest_period"],
            "type": "derived" if source == "BNY" else "raw",
        })
    out.sort(key=lambda r: (r["lens_id"], r["sub_theme_id"], r["name"]))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "variables"
    ws.append(FIELDS)
    for r in out:
        ws.append([r[f] for f in FIELDS])
    wb.save(OUT.with_suffix(".xlsx"))
    print(f"{len(out)} sheet variables with data -> {OUT.relative_to(ROOT)} and variables.xlsx "
          f"({len(rows)} sheet rows, {len({r['variable_name'] for r in rows})} distinct names)")


if __name__ == "__main__":
    main()
