"""District-wise mangrove cover, ISFR 2023 Volume I, Table 3.4 (2021 and 2023 assessments).

Reads  _sources/fsi-isfr/raw/fsi-isfr_india-state-of-forest-report-vol-1_2023.pdf (pages 130-133)
Writes ENV_mangrove-cover_2021-to-2023_STATES_FSI_DIST/<same>.csv

District names wrap over several lines around the number row; each name fragment is joined to
the number row nearest to it vertically. Run from the repo root.
"""
import re
import sys
from pathlib import Path

import pandas as pd
import pdfplumber

sys.path.insert(0, str(Path(__file__).parents[1] / "lgd"))
from build_geography import match_district  # noqa: E402

PDF = Path("_sources/fsi-isfr/raw/fsi-isfr_india-state-of-forest-report-vol-1_2023.pdf")
NAME = "ENV_mangrove-cover_2021-to-2023_STATES_FSI_DIST"
PAGES = [129, 130, 131, 132]  # 0-based: report pages 130-133
NUM = re.compile(r"^-?[\d,]+\.\d\d$")
STATES = {"Andhra Pradesh": "Andhra Pradesh", "Goa": "Goa", "Gujarat": "Gujarat", "Karnataka": "Karnataka",
          "Kerala": "Kerala", "Maharashtra": "Maharashtra", "Odisha": "Odisha", "Tamil Nadu": "Tamil Nadu",
          "West Bengal": "West Bengal", "Andaman & Nicobar": "Andaman & Nicobar Islands",
          "D&NH and Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu", "Puducherry": "Puducherry"}
# spellings in this table that differ from _reference/geography.csv (same district)
ALIAS = {"Nicobar": "Nicobars", "Dakshin Kannada": "Dakshina Kannada", "Uttar Kannada": "Uttara Kannada",
         "Ernakulum": "Ernakulam", "Mumbai city": "Mumbai", "Villupuram": "Viluppuram"}
COLS = ["very_dense_mangrove_sq_km", "moderately_dense_mangrove_sq_km", "open_mangrove_sq_km", "mangrove_cover_total_sq_km"]


def page_rows(page):
    """Return (kind, top, text, numbers) per printed line of Table 3.4 on this page."""
    words = page.extract_words(keep_blank_chars=False, use_text_flow=False)
    start = max(w["bottom"] for w in words if w["text"] == "3.4" or (w["text"] == "Districts"))
    lines = []  # words whose tops are within 3 pt form one printed line
    for w in sorted((w for w in words if w["top"] > start + 30), key=lambda w: w["top"]):
        if lines and w["top"] - lines[-1][0] <= 3:
            lines[-1][1].append(w)
        else:
            lines.append((w["top"], [w]))
    rows = []
    for top, ws in lines:
        ws = sorted(ws, key=lambda w: w["x0"])
        nums = [w["text"] for w in ws if NUM.match(w["text"])]
        text = " ".join(w["text"] for w in ws if not NUM.match(w["text"])).strip()
        if text.startswith(("3.7.1", "Forest Survey", "India State of Forest")):
            break
        if text.isdigit() and not nums:
            continue  # page number
        rows.append((top, text, nums))
    return rows


def main():
    pdf = pdfplumber.open(PDF)
    out, state = [], None
    for pi in PAGES:
        rows = [r for r in page_rows(pdf.pages[pi])]
        # find the table body on page 130 (after the state table): start at "1 Andhra Pradesh"
        if pi == 129:
            rows = rows[next(i for i, r in enumerate(rows) if r[1] == "1 Andhra Pradesh"):]
        numrows = [i for i, r in enumerate(rows) if len(r[2]) == 9]
        frags = {i: [] for i in numrows}
        for i, (top, text, nums) in enumerate(rows):
            if nums or not text:
                continue
            m = re.match(r"^(\d+) (.+)$", text)
            if (m and m.group(2) in STATES) or text in STATES:
                continue
            j = min(numrows, key=lambda k: abs(rows[k][0] - top))
            frags[j].append((top, text))
        for i, (top, text, nums) in enumerate(rows):
            m = re.match(r"^(\d+) (.+)$", text)
            if m and m.group(2) in STATES and not nums:
                state = STATES[m.group(2)]
                continue
            if i not in frags:
                continue
            parts = sorted(frags[i] + [(top, text)])
            name = ""
            for _, p in parts:
                if not p:
                    continue
                name = name[:-1] + p if name.endswith("-") and p[:1].islower() else (name + " " + p).strip()
            name = re.sub(r"\s+", " ", name)
            name = re.sub(r"^\d+ (?=Total$)", "", name)  # page number printed on the Total line
            v = [n.replace(",", "") for n in nums]
            district = "State total" if name == "Total" else name
            out.append([state, district, "2021"] + v[0:4] + [""])
            out.append([state, district, "2023"] + v[4:8] + [v[8]])
    df = pd.DataFrame(out, columns=["state_ut", "district", "year"] + COLS + ["change_since_2021_sq_km"])
    geo = pd.read_csv("_reference/geography.csv", dtype=str, keep_default_na=False)
    gs = geo[geo.level == "state"].set_index("state_ut").lgd_state_code.to_dict()
    gd = geo[geo.level == "district"]
    df.insert(1, "lgd_state_code", df.state_ut.map(gs))
    codes = []
    for s, d in zip(df.state_ut, df.district):
        idx = None if d == "State total" else match_district(gd, s, ALIAS.get(d, d), None)
        codes.append("" if idx is None else gd.at[idx, "lgd_district_code"])
    df.insert(3, "lgd_district_code", codes)
    df["source_flag"] = ["not_applicable" if (y == "2021") else "" for y in df.year]
    df["_t"] = df.district == "State total"
    order = list(dict.fromkeys(df.state_ut))
    df["_s"] = df.state_ut.map(order.index)
    df = df.sort_values(["_s", "_t", "district", "year"]).drop(columns=["_s", "_t"])
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(len(df), "rows;", df.district.ne("State total").sum() // 2, "districts")
    print("unmatched:", sorted({(s, d) for s, d, c in zip(df.state_ut, df.district, df.lgd_district_code) if d != "State total" and not c}))


if __name__ == "__main__":
    main()
