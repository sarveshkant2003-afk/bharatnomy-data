"""CEA monthly installed capacity report (Excel), as on 30.09.2026: state/UT and region tables.

Reads  _sources/cea-installed-capacity/raw/cea-installed-capacity_monthly-report_2026-09.xlsx (sheet "IC Value")
Writes ENG_installed-capacity_2026-09_STATES_CEA/<same>.csv
Run from the repo root.
"""
import re
from pathlib import Path

import pandas as pd

SRC = "_sources/cea-installed-capacity/raw/cea-installed-capacity_monthly-report_2026-09.xlsx"
NAME = "ENG_installed-capacity_2026-09_STATES_CEA"
COLS = ["coal_mw", "lignite_mw", "gas_mw", "diesel_mw", "thermal_total_mw", "nuclear_mw", "hydro_mw",
        "res_mnre_mw", "renewable_total_mw", "grand_total_mw"]
STATES = {"Jammu & Kashmir and Ladakh": "", "Andaman & Nicobar": "Andaman & Nicobar Islands",
          "Dadra and Nagar Haveli and Daman and Diu": "Dadra & Nagar Haveli and Daman & Diu"}
VALID = set("""Andaman & Nicobar Islands,Andhra Pradesh,Arunachal Pradesh,Assam,Bihar,Chandigarh,Chhattisgarh,
Dadra & Nagar Haveli and Daman & Diu,Delhi,Goa,Gujarat,Haryana,Himachal Pradesh,Jammu & Kashmir,Jharkhand,Karnataka,
Kerala,Ladakh,Lakshadweep,Madhya Pradesh,Maharashtra,Manipur,Meghalaya,Mizoram,Nagaland,Odisha,Puducherry,Punjab,
Rajasthan,Sikkim,Tamil Nadu,Telangana,Tripura,Uttar Pradesh,Uttarakhand,West Bengal""".replace("\n", "").split(","))


def clean(v):
    return re.sub(r"\s+", " ", str(v)).strip() if pd.notna(v) else ""


def main():
    d = pd.read_excel(SRC, "IC Value", header=None, dtype=object)
    out, region, area = [], "", ""
    start = d.index[d[1].astype(str).str.startswith("INSTALLED CAPACITY (IN MW) OF POWER UTILITIES")][0]
    for i in range(start, len(d)):
        a, b = clean(d.at[i, 1]), clean(d.at[i, 2])
        if a.startswith("List of Projects"):
            break
        m = re.search(r"(NORTHERN|WESTERN|SOUTHERN|EASTERN|NORTH[- ]?EASTERN|ISLANDS)", a.upper()) if a.startswith("INSTALLED") else None
        if m:
            region = {"NORTH-EASTERN": "North-Eastern", "NORTH EASTERN": "North-Eastern"}.get(m.group(1), m.group(1).title())
        if not isinstance(d.at[i, 3], (int, float)) or pd.isna(d.at[i, 3]):
            continue  # titles, headers, blank rows
        if a:
            area = a
        out.append([region, area, b or "Total"] + [d.at[i, c] for c in range(3, 13)])
    # All India rows of the first (region) table
    area = ""
    for i in range(0, start):
        a, b = clean(d.at[i, 1]), clean(d.at[i, 2])
        if a:
            area = a
        if area == "ALL INDIA" and isinstance(d.at[i, 3], (int, float)) and pd.notna(d.at[i, 3]):
            out.append(["All India", "All India", "Grand Total" if b == "Total" else b] + [d.at[i, c] for c in range(3, 13)])
    df = pd.DataFrame(out, columns=["region", "utility_area", "sector"] + COLS)
    st = df.utility_area.map(lambda s: STATES.get(s, s))
    df.insert(0, "state_ut", [s if s in VALID or s == "All India" else "" for s in st])
    for c in COLS:
        df[c] = pd.to_numeric(df[c]).map(lambda v: f"{v:.4f}".rstrip("0").rstrip("."))  # float noise beyond 4 decimals dropped
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, df.shape)
    return df


if __name__ == "__main__":
    print(main().to_string())
