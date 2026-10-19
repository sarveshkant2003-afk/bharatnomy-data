"""Checks for the Land Use Statistics CSVs (see CLAUDE.md, "Checks").

Prints every check with its result. Never changes data.
Run:  python moafw-lus/scripts/check_lus.py
"""
import csv, glob, os, random

DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STATES = """Andaman & Nicobar Islands, Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chandigarh,
Chhattisgarh, Dadra & Nagar Haveli and Daman & Diu, Delhi, Goa, Gujarat, Haryana, Himachal Pradesh,
Jammu & Kashmir, Jharkhand, Karnataka, Kerala, Ladakh, Lakshadweep, Madhya Pradesh, Maharashtra,
Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Puducherry, Punjab, Rajasthan, Sikkim, Tamil Nadu,
Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal, All India, Dadra & Nagar Haveli,
Daman & Diu"""
STATE_LIST = {s.strip() for s in STATES.replace("\n", " ").split(",")}

CEREALS = ["rice", "jowar", "bajra", "maize", "ragi", "wheat", "barley", "other_cereals_millets"]
LAND = [
    ("not_available_for_cultivation_total", ["area_non_agricultural_uses", "barren_unculturable_land"], []),
    ("other_uncultivated_land_total", ["permanent_pastures_grazing_land", "misc_tree_crops_groves", "culturable_waste_land"], []),
    ("fallow_land_total", ["fallow_other_than_current", "current_fallows"], []),
    ("reporting_area", ["forests", "not_available_for_cultivation_total", "other_uncultivated_land_total", "fallow_land_total", "net_area_sown"], []),
    ("area_sown_more_than_once", ["gross_cropped_area"], ["net_area_sown"]),
    ("agricultural_land", ["misc_tree_crops_groves", "culturable_waste_land", "fallow_land_total", "net_area_sown"], []),
    ("cultivated_land", ["current_fallows", "net_area_sown"], []),
    ("uncultivable_land", ["reporting_area"], ["agricultural_land"]),
    ("uncultivated_land", ["reporting_area"], ["cultivated_land"]),
]
SOURCES = [
    ("canals_total", ["canals_government", "canals_private"], []),
    ("net_irrigated_area", ["canals_total", "tanks", "tube_wells", "other_wells", "other_sources"], []),
    ("gross_irrigated_area_9", ["canals_total", "tanks", "tube_wells", "other_wells", "other_sources"], []),
    ("area_irrigated_more_than_once", ["gross_irrigated_area"], ["net_irrigated_area"]),
]
CROPS = [
    ("total_cereals_millets", CEREALS, []),
    ("total_pulses", ["gram", "tur_arhar", "other_pulses"], []),
    ("total_foodgrains", ["total_cereals_millets", "total_pulses"], []),
    ("total_sugar_crops", ["sugarcane", "other_sugar_crops"], []),
    ("total_condiments_spices", ["black_pepper", "chillies", "ginger", "turmeric", "cardamom", "betelnuts", "other_condiments_spices"], []),
    ("total_fresh_fruits", ["mango", "citrus_fruits", "banana", "grapes", "pome_fruits", "papaya", "apple", "other_fresh_fruits"], []),
    ("total_dry_fruits", ["cashewnut", "other_dry_fruits"], []),
    ("total_fruits", ["total_fresh_fruits", "total_dry_fruits"], []),
    ("total_vegetables", ["potato", "tapioca", "sweet_potato", "onions", "other_vegetables"], []),
    ("total_fruits_vegetables", ["total_fruits", "total_vegetables"], []),
    ("total_fibres", ["cotton", "jute", "mesta", "sannhemp", "other_fibres"], []),
    ("total_dyes_tanning", ["indigo", "other_dyes_tanning"], []),
    ("total_drugs_plantation", ["opium", "tobacco", "cinchona", "indian_hemp", "tea", "coffee", "rubber", "other_drugs_plantation"], []),
    ("total_area_sown", ["total_food_crops", "total_non_food_crops"], []),
    ("total_irrigated_area_all_crops", ["total_food_crops", "total_non_food_crops"], []),
    ("total_area_under_crops", ["total_food_crops", "total_non_food_crops"], []),
    ("area_sown_more_than_once_10", ["total_area_sown"], ["net_area_sown"]),
]
OILSEEDS = ["groundnut", "castorseed", "sesamum", "rapeseed_mustard", "linseed", "coconut", "nigerseed",
            "safflower", "soyabean", "sunflower", "other_oilseeds"]


def num(v):
    return float(v) if v not in ("", None) else None


def identities(cols):
    rules = []
    for target, plus, minus in LAND + SOURCES + CROPS:
        t = target.rsplit("_", 1)[0] if target.endswith(("_9", "_10")) else target
        if target == "gross_irrigated_area_9" and "net_irrigated_area" in cols:
            continue  # only Table 9 sums sources to gross irrigated area
        if t in cols and all(c in cols for c in plus + minus):
            rules.append((t, plus, minus))
    present = [c for c in OILSEEDS if c in cols]
    if "total_oilseeds" in cols:
        rules.append(("total_oilseeds", present, []))
    food = [c for c in ["total_foodgrains", "sugarcane" if "total_sugar_crops" not in cols else "total_sugar_crops",
                        "condiments_spices" if "condiments_spices" in cols else "total_condiments_spices",
                        "fruits_vegetables" if "fruits_vegetables" in cols else "total_fruits_vegetables",
                        "other_food_crops"] if c in cols]
    if "total_food_crops" in cols:
        rules.append(("total_food_crops", food, []))
    if "total_non_food_crops" in cols:
        nf = [c for c in ["total_oilseeds", "total_fibres", "cotton" if "total_fibres" not in cols else None,
                          "total_dyes_tanning", "indigo" if "total_dyes_tanning" not in cols else None,
                          "opium" if "total_drugs_plantation" not in cols else None,
                          "tobacco" if "total_drugs_plantation" not in cols else None,
                          "tea" if "total_drugs_plantation" not in cols else None,
                          "coffee" if "total_drugs_plantation" not in cols else None,
                          "total_drugs_plantation", "fodder_crops", "gross_fodder_crops", "green_manure_crops",
                          "other_non_food_crops"] if c and c in cols]
        rules.append(("total_non_food_crops", nf, []))
    return rules


def main():
    random.seed(7)
    for path in sorted(glob.glob(os.path.join(DIR, "*.csv"))):
        name = os.path.basename(path)
        rows = list(csv.DictReader(open(path, encoding="utf-8")))
        cols = {c[:-7] if c.endswith("_000_ha") else c: c for c in rows[0] if c not in ("state_ut", "year", "source_flag", "source_marks")}
        print(f"\n## {name}: {len(rows)} rows x {len(rows[0])} cols")
        keys = [(r["state_ut"], r["year"]) for r in rows]
        places = {k[0] for k in keys}
        years = {k[1] for k in keys}
        print(f"- keys: {len(places)} places x {len(years)} years; duplicates {len(keys) - len(set(keys))}; "
              f"empty keys {sum(1 for k in keys if not all(k))}")
        print(f"- state_ut not in list: {sorted(places - STATE_LIST) or 'none'}")
        bad, neg = [], []
        for r in rows:
            for short, c in cols.items():
                v = r[c]
                if v == "":
                    continue
                try:
                    x = float(v)
                except ValueError:
                    bad.append((r["state_ut"], r["year"], c, v))
                    continue
                if x < 0:
                    neg.append((r["state_ut"], r["year"], c, v))
        print(f"- non-numeric cells: {len(bad)} {bad[:3]}; negative values: {len(neg)} {neg[:3]}")
        blanks = sum(1 for r in rows for c in cols.values() if r[c] == "")
        print(f"- blank cells: {blanks} of {len(rows) * len(cols)}")
        for short, c in cols.items():
            if short.endswith("_pct") and "cropping_intensity" not in short:
                out = [(r["state_ut"], r["year"], r[c]) for r in rows if r[c] and not 0 <= float(r[c]) <= 100]
                print(f"- {c} within 0-100: {'yes' if not out else out}")
        # printed totals
        for target, plus, minus in identities(cols):
            diffs = []
            for r in rows:
                t = num(r[cols[target]])
                parts = [num(r[cols[c]]) for c in plus + minus]
                if t is None or all(p is None for p in parts):
                    continue
                calc = sum(p or 0 for p in [num(r[cols[c]]) for c in plus]) - sum(p or 0 for p in [num(r[cols[c]]) for c in minus])
                if abs(calc - t) > 1:
                    diffs.append((r["state_ut"], r["year"], t, round(calc, 1)))
            print(f"- {target} = {'+'.join(plus)}{''.join('-' + m for m in minus)}: "
                  f"{'ok (within 1 for rounding)' if not diffs else f'{len(diffs)} rows differ by >1, e.g. {diffs[:3]}'}")
        # All India vs sum of states
        if len(places) > 1 and "All India" in places:
            worst = []
            for y in sorted(years):
                ai = next((r for r in rows if r["state_ut"] == "All India" and r["year"] == y), None)
                if not ai:
                    continue
                for short, c in cols.items():
                    if short.endswith("_pct") or ai[c] == "":
                        continue
                    s = sum(float(r[c]) for r in rows if r["year"] == y and r["state_ut"] != "All India" and r[c])
                    d = float(ai[c]) - s
                    if abs(d) > max(2, 0.005 * float(ai[c])):
                        worst.append((y, short, ai[c], round(s)))
            print(f"- All India vs sum of states (tolerance max(2, 0.5%)): "
                  f"{'ok' if not worst else f'{len(worst)} cells differ, e.g. {worst[:4]}'}")
        # part <= whole
        for part, whole in [("net_irrigated_area", "gross_irrigated_area"), ("net_area_sown", "gross_cropped_area"),
                            ("net_area_sown", "reporting_area"), ("reporting_area", "geographical_area")]:
            if part in cols and whole in cols:
                out = [(r["state_ut"], r["year"], r[cols[part]], r[cols[whole]]) for r in rows
                       if r[cols[part]] and r[cols[whole]] and float(r[cols[part]]) > float(r[cols[whole]])]
                print(f"- {part} <= {whole}: {'yes' if not out else f'{len(out)} rows not, e.g. {out[:3]}'}")
        sample = random.sample(rows, min(5, len(rows)))
        print("- spot check rows: " + " | ".join(f"{r['state_ut']} {r['year']}: " + ", ".join(
            f"{k}={r[c]}" for k, c in list(cols.items())[:4]) for r in sample))


if __name__ == "__main__":
    main()
