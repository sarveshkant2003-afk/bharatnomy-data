"""IMD RSMC New Delhi cyclone climatology tables.

Reads  _sources/imd-rsmc/raw/imd-rsmc_severe-cyclonic-storms-climatology.xls (6 sheets, monthly counts by intensity)
       _sources/imd-rsmc/raw/imd-rsmc_tc-intensity-climatology.xls (TC DATA, TC RAINFALL: one row per cyclone, text)
Writes CLM_severe-cyclone-frequency_1965-to-2025_IN_IMD
       CLM_cyclone-intensity-landfall_1990-to-2025_IN_IMD
       CLM_cyclone-rainfall-damage_1990-to-2025_IN_IMD

Merged cells are read as the sheet shows them (every cell of the range gets its value). A row with
text only in later columns continues the cyclone above it and is appended to it. The sheets' Total and
Mean rows are left out (they are sums and averages of the rows kept). Run from the repo root.
"""
import re
from pathlib import Path

import pandas as pd
import xlrd

RAW = Path("_sources/imd-rsmc/raw")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
FREQ = {"SCS": "scs_48_63kt_count", "VSCS": "vscs_64_89kt_count", "ESCS": "escs_90_119kt_count",
        "SuCS": "sucs_120kt_plus_count", "VSCS above": "vscs_and_above_64kt_plus_count",
        "SCS above": "scs_and_above_48kt_plus_count"}


def grid(sheet):
    g = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    for r0, r1, c0, c1 in sheet.merged_cells:
        for r in range(r0, r1):
            for c in range(c0, c1):
                g[r][c] = g[r0][c0]
    return [[clean(v) for v in row] for row in g]


def clean(v):
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else repr(v)
    v = str(v).replace("\r", "\n")
    v = "\n".join(re.sub(r"[ \t\xa0]+", " ", line).strip() for line in v.split("\n"))
    return re.sub(r"\n{2,}", "\n", v).strip()


def write(df, name):
    Path(name).mkdir(exist_ok=True)
    df.to_csv(f"{name}/{name}.csv", index=False, lineterminator="\n")
    print(name, df.shape)


def frequency():
    book = xlrd.open_workbook(RAW / "imd-rsmc_severe-cyclonic-storms-climatology.xls", formatting_info=True)
    rows, annual_bad = {}, []
    for sh in book.sheets():
        col = FREQ[sh.name]
        g = grid(sh)
        h = next(i for i, r in enumerate(g) if r[0] == "Year")
        assert g[h][1:14] == MONTHS + ["Annual"], (sh.name, g[h])
        for r in g[h + 1:]:
            if not re.fullmatch(r"\d{4}", r[0]):
                continue
            vals = [int(float(x)) for x in r[1:13]]
            if sum(vals) != int(float(r[13])):
                annual_bad.append((sh.name, r[0]))
            for m, v in zip(range(1, 13), vals):
                rows.setdefault(f"{r[0]}-{m:02d}", {})[col] = v
    df = pd.DataFrame.from_dict(rows, orient="index")[list(FREQ.values())].sort_index()
    df.insert(0, "month", df.index)
    df.insert(0, "year", df.month.str[:4])
    print("annual column != sum of months:", annual_bad or "none")
    write(df.reset_index(drop=True), "CLM_severe-cyclone-frequency_1965-to-2025_IN_IMD")


def per_cyclone(sheet_name, cols, name):
    book = xlrd.open_workbook(RAW / "imd-rsmc_tc-intensity-climatology.xls", formatting_info=True)
    g = grid(book.sheet_by_name(sheet_name))
    h = next(i for i, r in enumerate(g) if "Basin" in r[1:4])
    out = []
    for r in g[h + 1:]:
        body = r[2:2 + len(cols) - 1]
        if not any(body):
            continue
        if not r[3] and out:  # continuation of the cyclone above
            for k, v in zip(cols[1:], body):
                if v and v not in out[-1][k]:
                    out[-1][k] = (out[-1][k] + "\n" + v).strip()
            continue
        out.append(dict(zip(cols, [r[1]] + body)))
    df = pd.DataFrame(out)
    df["year"] = df.year.str.strip()
    df = df.drop(columns=[c for c in df.columns if c.endswith("_2") and not df[c].any()])
    return df


def main():
    frequency()
    tc = per_cyclone("TC DATA", ["year", "basin", "cyclone", "max_wind_intensity", "max_wind_duration",
                            "lowest_central_pressure_and_time", "max_pressure_drop_hpa",
                            "landfall_max_sustained_wind", "landfall_central_pressure", "landfall_pressure_drop_hpa",
                            "landfall_place", "landfall_point_lat_lon", "landfall_time", "storm_surge"],
                "CLM_cyclone-intensity-landfall_1990-to-2025_IN_IMD")
    write(tc, "CLM_cyclone-intensity-landfall_1990-to-2025_IN_IMD")
    rf = per_cyclone("TC RAINFALL", ["year", "basin", "cyclone", "heavy_rainfall", "deaths", "deaths_2", "damage"],
                "CLM_cyclone-rainfall-damage_1990-to-2025_IN_IMD")
    # two rows have no year in this sheet: take it from the same cyclone's row in TC DATA
    rf.insert(1, "year_from_tc_data", "")
    for i in rf.index[rf.year == ""]:
        storm = re.search(r"([A-Z]{4,})", rf.at[i, "cyclone"]).group(1)
        hit = tc[tc.cyclone.str.upper().str.contains(storm)]
        assert len(hit) == 1, storm
        rf.at[i, "year"], rf.at[i, "year_from_tc_data"] = hit.year.iloc[0], "yes"
    write(rf, "CLM_cyclone-rainfall-damage_1990-to-2025_IN_IMD")


if __name__ == "__main__":
    main()
