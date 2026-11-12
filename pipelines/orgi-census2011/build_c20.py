"""Census 2011 C-20: disabled population by type of disability, age and sex, India, states and districts.

Reads  _sources/orgi-census2011/raw/c20/orgi-census2011_c20-<area>_2011.xlsx (fetch_c20.sh; 36 files)
Writes POP_disabled-population_2011_STATES_ORGI_DIST/<same>.csv
State files give the state and its districts; the India file gives the All India rows (its state rows
are compared with the state files as a check). Run from the repo root.
"""
import glob
from pathlib import Path

import pandas as pd

RAW = "_sources/orgi-census2011/raw/c20"
NAME = "POP_disabled-population_2011_STATES_ORGI_DIST"
TYPES = ["total", "seeing", "hearing", "speech", "movement", "mental_retardation", "mental_illness", "any_other", "multiple"]
VALS = [f"disabled_{t}_{s}" for t in TYPES for s in ("persons", "males", "females")]
AGES = ["Total", "0-4", "5-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90+", "Age Not Stated"]


def read(f):
    d = pd.read_excel(f, header=None, dtype=str)
    assert str(d.iat[1, 6]).startswith("Total number of disabled") and str(d.iat[2, 6]) == "Persons", f
    d = d.iloc[5:, :33].dropna(how="all")
    d.columns = ["table", "state_census_code", "district_census_code", "area_name", "area", "age_group"] + VALS
    return d


def main():
    files = sorted(glob.glob(f"{RAW}/*.xlsx")) + sorted(glob.glob(f"{RAW}/*.xls"))
    india = read(next(f for f in files if f.endswith("c20-india_2011.xlsx")))
    parts = [read(f) for f in files if not f.endswith("c20-india_2011.xlsx")]
    st = pd.concat(parts)
    # check: state rows of the India file equal the state rows of the state files
    a = india[india.state_census_code != "00"].set_index(["state_census_code", "area", "age_group"])[VALS]
    b = st[st.district_census_code == "000"].set_index(["state_census_code", "area", "age_group"])[VALS]
    common = a.index.intersection(b.index)
    diff = (a.loc[common].astype(int) - b.loc[common].astype(int)).abs().sum().sum()
    print("India-file state rows vs state files:", len(common), "rows compared, total abs difference", diff)
    df = pd.concat([st, india[india.state_census_code == "00"]])
    geo = pd.read_csv("_reference/geography.csv", dtype=str, keep_default_na=False)
    gs = geo[geo.level == "state"].drop_duplicates("census2011_state_code").set_index("census2011_state_code")
    gd = geo[(geo.level == "district") & (geo.census2011_district_code != "")].drop_duplicates("census2011_district_code").set_index("census2011_district_code")
    old = {"25": "Daman & Diu", "26": "Dadra & Nagar Haveli"}  # separate UTs in 2011
    df["state_ut"] = [("All India" if s == "00" else old.get(s) or gs.at[s, "state_ut"]) for s in df.state_census_code]
    df["lgd_state_code"] = [("" if s in ("00", "25", "26") else gs.at[s, "lgd_state_code"]) for s in df.state_census_code]
    isd = df.district_census_code != "000"
    df["district"] = ["All India" if s == "00" else ("State total" if not d else gd.at[c, "district"])
                      for s, d, c in zip(df.state_census_code, isd, df.district_census_code)]
    df["lgd_district_code"] = [gd.at[c, "lgd_district_code"] if d else "" for d, c in zip(isd, df.district_census_code)]
    df["district_census_code"] = df.district_census_code.where(isd, "")
    df["census2011_name"] = df.area_name.str.replace(r"^(State|District|INDIA)-?", "", regex=True).str.strip()
    df["area"] = df.area.str.lower()
    df["_a"] = df.age_group.map(AGES.index)
    df["_r"] = df.area.map(["total", "rural", "urban"].index)
    df["_t"] = df.district.isin(["State total", "All India"])
    df["_s"] = df.state_ut == "All India"
    df = df.sort_values(["_s", "state_ut", "_t", "district", "_r", "_a"])
    cols = ["state_ut", "lgd_state_code", "state_census_code", "district", "lgd_district_code", "district_census_code",
            "census2011_name", "area", "age_group"] + VALS
    df = df[cols]
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, df.shape)
    return df


if __name__ == "__main__":
    main()
