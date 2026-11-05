"""Build _reference/variables.csv (and a minimal variables.xlsx) from the datasets in the repo.

One row per value column of every dataset folder: key columns (places, codes, time, flags) are left out.
Names come from the dataset README's Columns table where a column is described there; lens and
sub-theme come from the rules below (dataset, then column pattern); unit, geography level, frequency
and coverage are read from the folder name and the CSV.

Run from the repo root:  python3 pipelines/reference/build_variables.py
Then:                     python3 tools/build_catalog.py   (validates and writes registry.json)
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from build_catalog import NAME, parse_readme  # noqa: E402

OUT = ROOT / "_reference" / "variables.csv"
csv.field_size_limit(sys.maxsize)

KEYS = {
    "state_ut", "lgd_state_code", "district", "lgd_district_code", "city", "state_census_code",
    "district_census_code", "district_census_name", "subdistrict", "subdistrict_census_code",
    "town_census_code", "area", "residence", "area_level", "year", "date", "month", "period",
    "source_flag", "source_marks", "sector", "nic_code", "nic_description", "cause", "age",
}
TIME = ("year", "date", "month")

# (dataset prefix, column regex or None, sub_theme_id); first match wins
RULES = [
    ("CLM_heat-indicators", r"^rainfall_", "CAR-RAIN"),
    ("CLM_heat-indicators", None, "CAR-HEAT"),
    ("CLM_rainfall", None, "CAR-RAIN"),
    ("CLM_temperature", None, "CAR-HEAT"),
    ("CLM_wind-humidity", r"^(relative_humidity|wet_bulb)", "CAR-HEAT"),
    ("CLM_wind-humidity", None, "CAR-WIND"),
    ("ENV_aqi", None, "CAR-AIR"),
    ("ENV_active-fires", None, "CAR-AIR"),
    ("ENV_forest", None, "CAR-LAND"),
    ("HLT_deaths-forces-of-nature", None, "CAR-MORTALITY"),
    ("HOU_household-amenities", r"^(drinking_water|latrine|bathing|waste_water)", "CAR-WATER"),
    ("HOU_household-amenities", r"^(cooking_fuel|lighting|kitchen)", "EPM-ACCESS"),
    ("HOU_household-amenities", None, "CAR-HOUSING"),
    ("HOU_slum", None, "CAR-EXPOSURE"),
    ("POP_", None, "CAR-EXPOSURE"),
    ("WAT_", None, "CAR-WATER"),
    ("AGR_area-under-crops", None, "COM-CROPS"),
    ("AGR_irrigated-area-by-crop", None, "COM-CROPS"),
    ("AGR_", None, "MAC-AGRI"),
    ("IND_asi", r"(electricity|coal|fuel|petroleum)", "EPM-DEMAND"),
    ("IND_", None, "MAC-INDUSTRY"),
    ("LAB_", None, "MAC-LABOUR"),
]

UNITS = [
    (r"_000_ha$", "thousand ha"), (r"_ha$", "ha"), (r"_sq_km$", "sq km"), (r"_pct(_of_area)?$|_pct_", "%"),
    (r"_mm$", "mm"), (r"_c$", "°C"), (r"_ms$", "m/s"), (r"_tpd$", "tonnes per day"),
    (r"_inr_lakh$", "₹ lakh"), (r"_inr_000$", "₹ thousand"), (r"_inr_crore$", "₹ crore"),
    (r"_000_tonne$", "thousand tonnes"), (r"_000_kwh$", "thousand kWh"), (r"_000$", "thousand"),
    (r"^spi_", "index"), (r"^(days|nights|heatwave|severe_heatwave|warm_nights|rainy_days|heavy|very_heavy|extremely_heavy|calm_days|strong_wind_days|consecutive_dry|monsoon_longest)", "days"),
    (r"^fire_detections", "count"), (r"^aqi", "index (0-500)"), (r"^deaths_", "deaths"),
]


def sub_theme(dataset, column):
    for prefix, pattern, st in RULES:
        if dataset.startswith(prefix) and (pattern is None or re.search(pattern, column)):
            return st
    return ""


def unit_of(column):
    for pattern, u in UNITS:
        if re.search(pattern, column):
            return u
    return ""


def geo_level(geo, level):
    if level:
        return level
    return "IN" if geo == "IN" else "STATE"


def coverage(path, header):
    t = next((c for c in TIME if c in header), None)
    if not t:
        return None, [], header
    i = header.index(t)
    vals, numeric = set(), {c: False for c in header}
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            if row[i]:
                vals.add(row[i])
    return t, sorted(vals), header


def numeric_columns(path, header, limit=2000):
    """Columns with at least one value, judged on the first rows: numbers, or short text categories."""
    seen = {c: set() for c in header}
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        next(r)
        for k, row in enumerate(r):
            if k >= limit:
                break
            for c, v in zip(header, row):
                if v != "" and len(seen[c]) < 50:
                    seen[c].add(v)
    return {c for c, v in seen.items() if v}


UNIT_SUFFIX = r"_(000_ha|ha|sq_km|pct|pct_of_area|mm|c|ms|tpd|inr_lakh|inr_000|inr_crore|000_tonne|000_kwh|000)$"
SPECIAL_UNITS = {"wind_direction_prevailing": "compass sector", "air_quality": "category",
                 "prominent_pollutants": "pollutant names"}


def humanise(column):
    return re.sub(UNIT_SUFFIX, "", column).replace("_", " ").strip().capitalize()


def unit_default(dataset, column):
    """Unit for columns without a unit suffix: survey codes in PLFS records, otherwise a count."""
    if column in SPECIAL_UNITS:
        return SPECIAL_UNITS[column]
    if dataset.startswith("LAB_plfs"):
        return "code or value (see README)"
    return "count"


def main():
    lenses = {r["sub_theme_id"]: r["lens_id"] for r in csv.DictReader(open(ROOT / "_reference/lenses.csv", encoding="utf-8"))}
    rows = []
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))):
        m = NAME.match(d.name)
        f = d / f"{d.name}.csv"
        if not m or not f.exists():
            continue
        cat, subject, period, geo, source, level = m.groups()
        header = next(csv.reader(open(f, newline="", encoding="utf-8")))
        t, vals, _ = coverage(f, header)
        filled = numeric_columns(f, header)
        meanings = {}
        if (d / "README.md").exists():
            meanings = parse_readme((d / "README.md").read_text(encoding="utf-8"))[3]
        freq = {"year": "annual", "date": "daily", "month": "monthly"}.get(t, "one-off")
        if t is None:
            years = re.findall(r"\d{4}(?:-\d{2})?", period)
            first, last = (years[0], years[-1]) if years else ("", "")
        else:
            first, last = vals[0], vals[-1]
        shared = {}
        for c in header:
            if c in meanings:
                shared[meanings[c]] = shared.get(meanings[c], 0) + 1
        for c in header:
            if c in KEYS or c not in filled:
                continue
            st = sub_theme(d.name, c)
            name = meanings.get(c) or humanise(c)
            if c in meanings and shared[meanings[c]] > 1:  # one README row describes several columns
                name = f"{humanise(c)}: {meanings[c]}"
            rows.append({
                "variable_id": f"{d.name}:{c}",
                "name": name,
                "lens_id": lenses.get(st, ""),
                "sub_theme_id": st,
                "dataset": d.name,
                "column": c,
                "unit": unit_of(c) or unit_default(d.name, c),
                "geo_level": geo_level(geo, level),
                "frequency": freq,
                "earliest_period": first,
                "latest_period": last,
                "type": "derived" if source == "BNY" else "raw",
            })
    fields = list(rows[0])
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    write_xlsx(rows, fields)
    missing = [r["variable_id"] for r in rows if not r["sub_theme_id"]]
    print(f"{len(rows)} variables -> {OUT.relative_to(ROOT)} and variables.xlsx; without sub-theme: {len(missing)}")


def write_xlsx(rows, fields):
    """Minimal workbook: one sheet, header row, values only."""
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "variables"
    ws.append(fields)
    for r in rows:
        ws.append([r[f] for f in fields])
    wb.save(OUT.with_suffix(".xlsx"))


if __name__ == "__main__":
    main()
