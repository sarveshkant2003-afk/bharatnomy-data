"""District crop Area, Production and Yield, all states, 1997-98 to 2022-23 (DES, MoA&FW crops APY report).

Reads  _sources/moafw-apy/raw/moafw-apy_district-<code>_1997-to-2022.html (fetch_apy.py)
Writes AGR_crop-area-production-yield_1997-98-to-2009-10_STATES_MOAFW_DIST and ..._2010-11-to-2022-23_... (long: one row per
       district, year, crop and season that has any value). Cells are kept as printed (text), commas removed.
Run from the repo root.
"""
import glob
import re
import sys
from pathlib import Path

import lxml.html
import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1] / "lgd"))
from build_geography import match_district  # noqa: E402

RAW = "_sources/moafw-apy/raw"
# split in two by year range to keep each CSV under 25 MB
PARTS = {"AGR_crop-area-production-yield_1997-98-to-2009-10_STATES_MOAFW_DIST": ("1997-98", "2009-10"),
         "AGR_crop-area-production-yield_2010-11-to-2022-23_STATES_MOAFW_DIST": ("2010-11", "2022-23")}
STATE_FIX = {"Andaman and Nicobar Islands": "Andaman & Nicobar Islands", "Jammu and Kashmir": "Jammu & Kashmir",
             "Dadra and Nagar Haveli": "Dadra & Nagar Haveli", "Daman and Diu": "Daman & Diu",
             "The Dadra & Nagar Haveli and Daman and Diu": "Dadra & Nagar Haveli and Daman & Diu"}


def text(el):
    return re.sub(r"\s+", " ", el.text_content()).strip()


def expand(row):
    out = []
    for th in row:
        out += [text(th)] * int(th.get("colspan", 1))
    return out


def parse(f):
    s = Path(f).read_text(encoding="utf-8")
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<pre>.*?</pre>", "", s, flags=re.S)
    doc = lxml.html.fromstring(s)
    tbl = doc.get_element_by_id("apyreport")
    head = tbl.xpath("./thead/tr")
    if len(head) < 3:
        return []
    crops = expand(head[0].xpath("./th"))[3:]
    seasons = expand(head[1].xpath("./th"))
    measures = expand(head[2].xpath("./th"))
    assert len(crops) == len(seasons) == len(measures), f
    rows, st, di = [], "", ""
    for tr in tbl.xpath("./tbody/tr"):
        cells = [text(td) for td in tr.xpath("./td")]
        k = len(cells) - len(crops)  # state and district cells span many rows (rowspan)
        if k not in (1, 2, 3):
            continue
        keys = [re.sub(r"^\d+\.\s*", "", c) for c in cells[:k]]
        if k == 3:
            st, di = keys[0], keys[1]
        elif k == 2:
            di = keys[0]
        yr = keys[-1]
        cells = cells[k - 3:] if k == 3 else ["", ""][: 3 - k] + cells
        vals = [v.replace(",", "") for v in cells[3:]]
        for i in range(0, len(crops), 3):  # each crop-season block is Area, Production, Yield
            assert measures[i].startswith("Area") and measures[i + 1].startswith("Production") and measures[i + 2].startswith("Yield"), measures[i:i + 3]
            a, p, y = vals[i:i + 3]
            if a or p or y:
                pu = re.search(r"\((.+)\)", measures[i + 1]).group(1)
                yu = re.search(r"\((.+)\)", measures[i + 2]).group(1)
                rows.append((st, di, yr, crops[i], seasons[i], a, p, y, pu, yu))
    return rows


def main():
    rows = []
    for f in sorted(glob.glob(f"{RAW}/moafw-apy_district-*.html")):
        r = parse(f)
        rows += r
        print(Path(f).name, len(r))
    df = pd.DataFrame(rows, columns=["state_ut", "district", "year", "crop", "season", "area_ha", "production", "yield",
                                     "production_unit", "yield_unit"])
    df["state_ut"] = df.state_ut.map(lambda s: STATE_FIX.get(s.replace("&amp;", "&"), s.replace("&amp;", "&")))
    df["year"] = df.year.str.replace(r"^(\d{4}) - \d{2}(\d{2})$", r"\1-\2", regex=True)
    geo = pd.read_csv("_reference/geography.csv", dtype=str, keep_default_na=False)
    gs = geo[geo.level == "state"].set_index("state_ut").lgd_state_code.to_dict()
    gd = geo[geo.level == "district"]
    codes = {}
    for s_, d in df[["state_ut", "district"]].drop_duplicates().itertuples(index=False):
        idx = match_district(gd, s_, d, None)
        codes[(s_, d)] = "" if idx is None else gd.at[idx, "lgd_district_code"]
    df.insert(1, "lgd_state_code", df.state_ut.map(lambda s: gs.get(s, "")))
    df.insert(3, "lgd_district_code", [codes[(s_, d)] for s_, d in zip(df.state_ut, df.district)])
    df = df.sort_values(["state_ut", "district", "year", "crop", "season"])
    for name, (a, b) in PARTS.items():
        part = df[(df.year >= a) & (df.year <= b)]
        Path(name).mkdir(exist_ok=True)
        part.to_csv(f"{name}/{name}.csv", index=False, lineterminator="\n")
        print(name, part.shape)
    un = sorted({k for k, v in codes.items() if not v})
    print("districts without LGD code:", len(un), "of", len(codes))
    return df


if __name__ == "__main__":
    main()
