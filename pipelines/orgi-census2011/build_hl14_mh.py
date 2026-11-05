"""Census 2011 table HH-14 (percentage of households by amenities and assets) for Maharashtra,
district and sub-district rows, all 135 indicators.

Input:  _sources/orgi-census2011/raw/hl14-mh/orgi-census2011_hl14-district-<code>_2011.xlsx  (fetch_hl14_mh.sh)
Output: HOU_household-amenities-hh14_2011_MH_ORGI_SDT/HOU_household-amenities-hh14_2011_MH_ORGI_SDT.csv

Town, ward and village rows of the same files are not converted yet.

Run from the repo root:  python3 pipelines/orgi-census2011/build_hl14_mh.py
"""
import glob
import re
from pathlib import Path

import pandas as pd

RAW = "_sources/orgi-census2011/raw/hl14-mh"
NAME = "HOU_household-amenities-hh14_2011_MH_ORGI_SDT"
GEO = "_reference/geography.csv"

# Column-number ranges of the printed table (0-based in the sheet) -> name prefix
GROUPS = [
    (10, 21, "house_condition"), (22, 30, "roof"), (31, 40, "wall"), (41, 47, "floor"),
    (48, 54, "dwelling_rooms"), (55, 61, "household_size"), (62, 64, "ownership"),
    (65, 70, "married_couples"), (71, 80, "drinking_water_source"), (81, 83, "drinking_water_location"),
    (84, 89, "lighting"), (90, 101, "latrine"), (102, 104, "bathing"), (105, 107, "waste_water"),
    (108, 117, "cooking_fuel"), (118, 125, "kitchen"), (126, 126, "banking"), (127, 138, "assets"),
    (139, 144, "house_structure"),
]
# Labels that need a clearer name than a slug of the printed text
FIXED = {
    90: "latrine_within_premises_total", 91: "latrine_flush_piped_sewer", 92: "latrine_flush_septic_tank",
    93: "latrine_flush_other_system", 94: "latrine_pit_with_slab", 95: "latrine_pit_without_slab",
    96: "latrine_night_soil_to_open_drain", 97: "latrine_service_removed_by_human",
    98: "latrine_service_serviced_by_animal", 99: "latrine_none_within_premises_total",
    100: "latrine_none_public_latrine", 101: "latrine_none_open",
    102: "bathing_within_premises_bathroom", 103: "bathing_within_premises_enclosure_without_roof",
    104: "bathing_none_within_premises",
    118: "kitchen_total", 119: "kitchen_cooking_inside_total", 120: "kitchen_cooking_inside_has_kitchen",
    121: "kitchen_cooking_inside_no_kitchen", 122: "kitchen_cooking_outside_total",
    123: "kitchen_cooking_outside_has_kitchen", 124: "kitchen_cooking_outside_no_kitchen",
    125: "kitchen_no_cooking", 126: "banking_services_availed",
    129: "assets_computer_with_internet", 130: "assets_computer_without_internet",
    131: "assets_phone_landline_only", 132: "assets_phone_mobile_only", 133: "assets_phone_both",
    137: "assets_tv_computer_phone_and_scooter_or_car", 138: "assets_none_of_listed",
}


def slug(s):
    s = str(s).lower().replace("&", "and").replace("+", "_plus").replace("-", "_to_")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def column_names(sheet):
    h = sheet.iloc[3:6]
    names = {}
    for a, b, prefix in GROUPS:
        l2 = None
        for c in range(a, b + 1):
            if c in FIXED:
                names[c] = FIXED[c]
                continue
            if isinstance(h.iat[1, c], str):
                l2 = h.iat[1, c]
            l3 = h.iat[2, c]
            parts = [prefix] if prefix == "house_structure" else [prefix, slug(l2)]  # structure header has no level 2
            if isinstance(l3, str):
                parts.append(slug(l3))
            names[c] = "_".join(p for p in parts if p)
    names = {c: n.replace("_to_", "_") if not re.search(r"\d_to_\d", n) else n for c, n in names.items()}
    out = {c: f"{n}_pct" for c, n in names.items()}
    assert len(set(out.values())) == len(out), "duplicate column names"
    return out


def main():
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    geo = geo[geo.level == "district"].set_index("census2011_district_code")
    parts, names = [], None
    for f in sorted(glob.glob(f"{RAW}/*.xlsx")):
        s = pd.read_excel(f, header=None, dtype=str)
        n = column_names(s)
        if names is None:
            names = n
        assert n == names, f"{f}: header differs"
        body = s.iloc[7:]
        body = body[body[0].notna() & body[0].str.strip().str.isdigit()]
        area = body[8].str.strip()
        keep = area.str.startswith(("District - ", "Sub-Dist - ")) & (body[6].str.strip().str.strip("0") == "")
        body = body[keep]
        df = pd.DataFrame({
            "state_ut": "Maharashtra",
            "lgd_state_code": "27",
            "district": [geo.at[c, "district"] for c in body[2].str.strip()],
            "lgd_district_code": [geo.at[c, "lgd_district_code"] for c in body[2].str.strip()],
            "district_census_code": body[2].str.strip(),
            "district_census_name": body[3].str.strip(),
            "area_level": ["district" if a.startswith("District") else "sub-district" for a in area[keep]],
            "subdistrict": [a.split(" - ", 1)[1].strip() if a.startswith("Sub-Dist") else "" for a in area[keep]],
            "subdistrict_census_code": [t.strip() if t.strip().strip("0") else "" for t in body[4]],
            "residence": body[9].str.strip(),
        })
        vals = pd.DataFrame({name: pd.to_numeric(body[c].str.strip(), errors="raise").values
                             for c, name in names.items()})
        parts.append(pd.concat([df.reset_index(drop=True), vals], axis=1))
    out = pd.concat(parts)
    order = {"Total": 0, "Rural": 1, "Urban": 2}
    out["_o"] = out.residence.map(order)
    out["_l"] = (out.area_level == "sub-district").astype(int)
    out = out.sort_values(["district", "_l", "subdistrict_census_code", "_o"]).drop(columns=["_o", "_l"])
    Path(NAME).mkdir(exist_ok=True)
    out.to_csv(Path(NAME) / f"{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, out.shape)
    print(list(names.values()))


if __name__ == "__main__":
    main()
