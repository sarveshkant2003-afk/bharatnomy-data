"""Convert all ten tables of Land Use Statistics at a Glance 2024-25 (PDF) to CSV.

Reads  raw/moafw-lus_land-use-statistics-at-a-glance_2024-25.pdf
Writes one CSV per table into the folder above scripts/.

Run from anywhere:  python moafw-lus/scripts/lus_2024-25.py
"""
import csv, os, re, sys
from collections import OrderedDict

import pdfplumber

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lus_pdf as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.normpath(os.path.join(HERE, ".."))
PDF = os.path.join(DIR, "raw", "moafw-lus_land-use-statistics-at-a-glance_2024-25.pdf")

CEREALS = ["rice", "jowar", "bajra", "maize", "ragi", "wheat", "barley",
           "other_cereals_millets", "total_cereals_millets"]

# column number in the publication -> CSV column name (all thousand hectares unless _pct)
COLS = {
    1: dict(enumerate([
        "geographical_area", "reporting_area", "forests", "area_non_agricultural_uses",
        "barren_unculturable_land", "not_available_for_cultivation_total",
        "permanent_pastures_grazing_land", "misc_tree_crops_groves", "culturable_waste_land",
        "other_uncultivated_land_total", "fallow_other_than_current", "current_fallows",
        "fallow_land_total", "net_area_sown", "gross_cropped_area", "area_sown_more_than_once",
        "agricultural_land", "cultivated_land", "cropping_intensity_pct"], start=2)),
    2: dict(enumerate([
        "canals_government", "canals_private", "canals_total", "tanks", "tube_wells",
        "other_wells", "other_sources", "net_irrigated_area", "gross_irrigated_area",
        "area_irrigated_more_than_once", "gross_irrigated_to_gross_cropped_pct"], start=2)),
    3: dict(enumerate(CEREALS + [
        "gram", "tur_arhar", "other_pulses", "total_pulses", "total_foodgrains", "sugarcane",
        "condiments_spices", "fruits_vegetables", "other_food_crops", "total_food_crops",
        "groundnut", "sesamum", "rapeseed_mustard", "linseed", "other_oilseeds",
        "total_oilseeds", "cotton", "tobacco", "fodder_crops", "other_non_food_crops",
        "total_non_food_crops", "total_irrigated_area_all_crops"], start=2)),
    4: dict(enumerate(CEREALS + [
        "gram", "tur_arhar", "other_pulses", "total_pulses", "total_foodgrains", "sugarcane",
        "condiments_spices", "fruits_vegetables", "other_food_crops", "total_food_crops",
        "groundnut", "castorseed", "sesamum", "rapeseed_mustard", "linseed", "coconut",
        "other_oilseeds", "total_oilseeds", "cotton", "jute", "other_fibres", "total_fibres",
        "indigo", "opium", "tobacco", "tea", "coffee", "fodder_crops", "other_non_food_crops",
        "total_non_food_crops", "total_area_under_crops"], start=2)),
}
COLS[5] = dict(COLS[1])
del COLS[5][20]  # cropping intensity is in table 6 for states
COLS[5].update({20: "uncultivable_land", 21: "uncultivated_land"})
COLS[6] = dict(enumerate([
    "net_irrigated_area", "gross_irrigated_area", "area_irrigated_more_than_once",
    "net_unirrigated_area", "gross_unirrigated_area", "gross_irrigated_to_gross_cropped_pct",
    "cropping_intensity_pct"], start=2))
COLS[7] = dict(enumerate([
    "canals_government", "canals_private", "canals_total", "tanks", "tube_wells",
    "other_wells", "other_sources", "net_irrigated_area"], start=2))
COLS[8] = dict(enumerate(CEREALS + [
    "gram", "tur_arhar", "other_pulses", "total_pulses", "total_foodgrains", "sugarcane",
    "condiments_spices", "fruits_vegetables", "other_food_crops", "total_food_crops",
    "groundnut", "sesamum", "rapeseed_mustard", "linseed", "soyabean", "sunflower",
    "other_oilseeds", "total_oilseeds", "cotton", "tobacco", "fodder_crops",
    "other_non_food_crops", "total_non_food_crops", "total_irrigated_area_all_crops"], start=2))
COLS[9] = dict(enumerate([
    "canals_government", "canals_private", "canals_total", "tanks", "tube_wells",
    "other_wells", "other_sources", "gross_irrigated_area"], start=2))
COLS[10] = dict(enumerate(CEREALS + [
    "gram", "tur_arhar", "other_pulses", "total_pulses", "total_foodgrains",
    "sugarcane", "other_sugar_crops", "total_sugar_crops",
    "black_pepper", "chillies", "ginger", "turmeric", "cardamom", "betelnuts",
    "other_condiments_spices", "total_condiments_spices",
    "mango", "citrus_fruits", "banana", "grapes", "pome_fruits", "papaya", "apple",
    "other_fresh_fruits", "total_fresh_fruits", "cashewnut", "other_dry_fruits",
    "total_dry_fruits", "total_fruits", "potato", "tapioca", "sweet_potato", "onions",
    "other_vegetables", "total_vegetables", "total_fruits_vegetables", "other_food_crops",
    "total_food_crops", "groundnut", "castorseed", "sesamum", "rapeseed_mustard", "linseed",
    "coconut", "nigerseed", "safflower", "soyabean", "sunflower", "other_oilseeds",
    "total_oilseeds", "cotton", "jute", "mesta", "sannhemp", "other_fibres", "total_fibres",
    "indigo", "other_dyes_tanning", "total_dyes_tanning", "opium", "tobacco", "cinchona",
    "indian_hemp", "tea", "coffee", "rubber", "other_drugs_plantation",
    "total_drugs_plantation", "gross_fodder_crops", "green_manure_crops",
    "other_non_food_crops", "total_non_food_crops", "total_area_sown",
    "area_sown_more_than_once", "net_area_sown"], start=2))

OUT = {
    1: "moafw-lus_land-use-classification_india_1950-51-to-2024-25.csv",
    2: "moafw-lus_net-irrigated-area-by-source_india_1950-51-to-2024-25.csv",
    3: "moafw-lus_irrigated-area-by-crop_india_1950-51-to-2024-25.csv",
    4: "moafw-lus_area-under-crops_india_1950-51-to-2024-25.csv",
    5: "moafw-lus_land-use-classification_state_2015-16-to-2024-25.csv",
    6: "moafw-lus_irrigated-area_state_2015-16-to-2024-25.csv",
    7: "moafw-lus_net-irrigated-area-by-source_state_2015-16-to-2024-25.csv",
    8: "moafw-lus_irrigated-area-by-crop_state_2015-16-to-2024-25.csv",
    9: "moafw-lus_gross-irrigated-area-by-source_state_2015-16-to-2024-25.csv",
    10: "moafw-lus_area-under-crops_state_2015-16-to-2024-25.csv",
}

STATES = {
    "ANDAMAN & NICOBAR ISLANDS": "Andaman & Nicobar Islands",
    # p146: the first line "ANDAMAN &" of this heading has no extractable text
    "NICOBAR ISLANDS": "Andaman & Nicobar Islands",
    # p147: same for the first and last lines of "DADRA AND / NAGAR HAVELI AND DAMAN AND / DIU"
    "NAGAR HAVELI AND DAMAN AND": "Dadra & Nagar Haveli and Daman & Diu", "ANDHRA PRADESH": "Andhra Pradesh",
    "ARUNACHAL PRADESH": "Arunachal Pradesh", "ASSAM": "Assam", "BIHAR": "Bihar",
    "CHANDIGARH": "Chandigarh", "CHHATTISGARH": "Chhattisgarh",
    "DADAR AND NAGAR HAVELI AND DAMAN AND DIU": "Dadra & Nagar Haveli and Daman & Diu",
    "DADRA AND NAGAR HAVELI AND DAMAN AND DIU": "Dadra & Nagar Haveli and Daman & Diu",
    "DADAR & NAGAR HAVELI": "Dadra & Nagar Haveli", "DADRA & NAGAR HAVELI": "Dadra & Nagar Haveli",
    "DAMAN & DIU": "Daman & Diu", "DELHI": "Delhi", "GOA": "Goa", "GUJARAT": "Gujarat",
    "HARYANA": "Haryana", "HIMACHAL PRADESH": "Himachal Pradesh",
    "JAMMU & KASHMIR": "Jammu & Kashmir", "JHARKHAND": "Jharkhand", "KARNATAKA": "Karnataka",
    "KERALA": "Kerala", "LADAKH": "Ladakh", "LAKSHADWEEP": "Lakshadweep",
    "MADHYA PRADESH": "Madhya Pradesh", "MAHARASHTRA": "Maharashtra", "MANIPUR": "Manipur",
    "MEGHALAYA": "Meghalaya", "MEGHALYA": "Meghalaya", "MIZORAM": "Mizoram",
    "NAGALAND": "Nagaland", "ODISHA": "Odisha", "PUDUCHERRY": "Puducherry", "PUNJAB": "Punjab",
    "RAJASTHAN": "Rajasthan", "SIKKIM": "Sikkim", "TAMIL NADU": "Tamil Nadu",
    "TELANGANA": "Telangana", "TRIPURA": "Tripura", "UTTAR PRADESH": "Uttar Pradesh",
    "UTTARAKHAND": "Uttarakhand", "UTTRAKHAND": "Uttarakhand", "WEST BENGAL": "West Bengal",
    "ALL INDIA": "All India",
}
ORDER = list(OrderedDict.fromkeys(STATES.values()))

NUM = re.compile(r"^(\(?)(-?\d+(?:\.\d+)?)(\)?)([*$#@^]*)$")
PAREN = re.compile(r"\((\d+)\)")
# Tables 3 and 4: "Figures in parenthesis give area ... for which crop-wise details are
# not available but has been included in Total". Kept in source_marks as "<column>:(n)".
MARKER_ONLY = re.compile(r"^(\(a\)|NAS|N\.A\.S\.|NA|N\.A\.|-|\.|[*$#@^]+)$")
NAME = re.compile(r"^[A-Za-z&.*$@# -]+$")


def unit(col):
    return col if col.endswith("_pct") else col + "_000_ha"


def parse_cell(text):
    """Return (value, mark). mark keeps any symbol printed with the number."""
    text = text.replace(" ", "")
    m = NUM.match(text)
    if m:
        paren = m.group(1) == "(" and m.group(3) == ")"
        mark = ("()" if paren else "") + m.group(4)
        return m.group(2), mark
    if MARKER_ONLY.match(text):
        return "", text
    raise ValueError(f"unparsed cell {text!r}")


def state_key(name):
    base = re.sub(r"[*$#@^]+", "", name).strip()
    base = re.sub(r"\s+", " ", base).upper()
    if base not in STATES and base.count(" AND ") == 1:
        base = base.replace(" AND ", " & ")  # "Andaman and Nicobar Islands", "Jammu and Kashmir"
    if base not in STATES:
        raise KeyError(f"unknown state heading {name!r}")
    return STATES[base], name[len(name.rstrip("*$#@^")):]


def main():
    pdf = pdfplumber.open(PDF)
    data = {t: OrderedDict() for t in OUT}     # table -> (state, year) -> {col: value}
    marks = {t: {} for t in OUT}               # table -> (state, year) -> [marks]
    flags = {t: {} for t in OUT}
    current = {}                               # (table, first column) -> state carried across pages
    seen = {}
    for page in pdf.pages:
        text = re.sub(r"\n\d+\s*$", "", (page.extract_text() or "").strip())
        if text and text in seen:
            # Printed page 137 (PDF p150) repeats printed page 130: the Table 5 page with
            # columns 12-21 for Goa to Kerala is missing from the publication.
            print(f"  p{page.page_number} duplicates p{seen[text]}: skipped", file=sys.stderr)
            continue
        seen[text] = page.page_number
        got = L.page_table(page)
        if not got:
            continue
        title, mk, head, body = got
        tm = re.match(r"TABLE\s*(\d+)", title)
        if not tm:
            continue
        t = int(tm.group(1))
        nums = [int(L.MARK.fullmatch(m["text"]).group(1)) for m in mk]
        group = (t, nums[1])
        state = current.get(group, "All India" if t <= 4 else None)
        pending = current.pop((group, "pending"), [])  # heading split across pages
        for row in body:
            text = " ".join(w["text"] for w in row)
            first = row[0]["text"]
            ym = L.YEAR.match(first) or re.match(r"^(\d{4}-\d{2})(\(p\))?([*$#@^]*)$", first)
            if ym:
                if pending:
                    try:
                        state, smark = state_key(" ".join(pending))
                    except KeyError:
                        print(page.page_number, [[(w["text"], round(w["top"])) for w in r] for r in body[:4]]); raise
                    pending = []
                    if smark:
                        current[(group, "smark")] = smark
                if state is None:
                    raise ValueError(f"p{page.page_number}: year row before any state: {text}")
                year = ym.group(1)
                key = (state, year)
                rowmarks = marks[t].setdefault(key, [])
                if ym.group(2):
                    flags[t][key] = "provisional"
                if ym.group(3):
                    rowmarks.append(f"year:{ym.group(3)}")
                cells = L.assign(row[1:], mk)
                rec = data[t].setdefault(key, {})
                for n, cell in cells.items():
                    if n == 1:
                        continue
                    if n not in COLS[t]:
                        raise KeyError(f"p{page.page_number} T{t}: column {n} not mapped ({cell})")
                    # a lone '(p)' printed in its own word after the year
                    for part in re.sub(r"(\d)\(", r"\1 (", cell).split():
                        pm = PAREN.fullmatch(part)
                        if pm and t in (3, 4):
                            rowmarks.append(f"{unit(COLS[t][n])}:({pm.group(1)})")
                            continue
                        v, m = parse_cell(part)
                        col = unit(COLS[t][n])
                        if v != "":
                            if col in rec and rec[col] != v:
                                raise ValueError(f"p{page.page_number} T{t} {key} {col}: {rec[col]} vs {v}")
                            rec[col] = v
                        if m:
                            rowmarks.append(f"{col}:{m}")
                smark = current.get((group, "smark"))
                if smark and f"state_ut:{smark}" not in rowmarks:
                    rowmarks.append(f"state_ut:{smark}")
            elif NAME.match(text) and not text.startswith("(P"):
                if not pending:
                    current.pop((group, "smark"), None)
                pending.append(text)
            elif re.match(r"^\(p\)", text, re.I) or text.startswith(("Note", "NAS", "*Gross", "$", "#", "@", "(a)", "but has")):
                continue
            elif re.fullmatch(r"\d+", text):
                continue  # page number
            else:
                # wrapped footnote text or similar: keep going, but show it
                print(f"  skip p{page.page_number} T{t}: {text[:90]}", file=sys.stderr)
        current[group] = state
        if pending:
            current[(group, "pending")] = pending

    # Table 5: the page with columns 12-21 for Goa (2024-25) to Kerala is missing (see above)
    for key, rec in data[5].items():
        if not any(unit(COLS[5][n]) in rec for n in range(12, 22)):
            marks[5].setdefault(key, []).append("columns_12_to_21:page_missing_in_publication")

    for t, rows in data.items():
        cols = [unit(c) for c in COLS[t].values()]
        has_marks = any(marks[t].get(k) for k in rows)
        has_flag = any(flags[t].get(k) for k in rows)
        header = ["state_ut", "year"] + cols + (["source_flag"] if has_flag else []) + (["source_marks"] if has_marks else [])
        keys = sorted(rows, key=lambda k: (k[0] == "All India", ORDER.index(k[0]) if k[0] != "All India" else 0, k[0], k[1]))
        if t > 4:
            keys = sorted(rows, key=lambda k: (k[0] == "All India", k[0], k[1]))
        path = os.path.join(DIR, OUT[t])
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(header)
            for k in keys:
                r = rows[k]
                line = [k[0], k[1]] + [r.get(c, "") for c in cols]
                if has_flag:
                    line.append(flags[t].get(k, ""))
                if has_marks:
                    line.append("; ".join(OrderedDict.fromkeys(marks[t].get(k, []))))
                w.writerow(line)
        print(f"T{t}: {len(keys)} rows x {len(header)} cols -> {OUT[t]}")


if __name__ == "__main__":
    main()
