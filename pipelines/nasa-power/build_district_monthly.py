"""Monthly aerosol, soil wetness, land evaporation and boundary-layer values per Maharashtra district (NASA POWER, MERRA-2).

Input:  _sources/nasa-power/raw/monthly/power_monthly_<lat>_<lon>.json.gz  (fetch_power_monthly.py)
        _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011
        _reference/geography.csv
Output: CLM_aerosol-soil-evaporation-boundary-layer_1981-to-2025_MH_BNY_DIST/<same>.csv

District value = area-weighted mean of the POWER cells (0.5 x 0.625 deg) overlapping the 2011 boundary.
Mixing height (approx.) = (Rd * T / g) * ln(surface pressure / PBL-top pressure), with T the 2 m temperature;
ventilation coefficient (approx.) = mixing height x 10 m wind speed. Both from monthly means.

Run from the repo root:  python3 pipelines/nasa-power/build_district_monthly.py
"""
import glob
import gzip
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from shapely.geometry import box

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "imd-gridded"))
from build_district_indices import districts, keys, assemble  # noqa: E402

RAW = "_sources/nasa-power/raw/monthly"
NAME = "CLM_aerosol-soil-evaporation-boundary-layer_1981-to-2025_MH_BNY_DIST"
DLAT, DLON = 0.5, 0.625
RD, G = 287.05, 9.80665
COLS = {"AOD_55": ("aod_550nm", 3), "GWETTOP": ("soil_wetness_surface_frac", 2),
        "GWETROOT": ("soil_wetness_root_zone_frac", 2), "GWETPROF": ("soil_wetness_profile_frac", 2),
        "EVLAND": ("evaporation_land_mm_day", 2), "PBLTOP": ("pbl_top_pressure_kpa", 2),
        "PS": ("surface_pressure_kpa", 2), "T2M": ("temperature_2m_c", 2), "WS10M": ("wind_speed_10m_ms", 2)}


def load_cells():
    cells = {}
    for f in glob.glob(f"{RAW}/power_monthly_*.json.gz"):
        lat, lon = map(float, re.search(r"_(-?[\d.]+)_(-?[\d.]+)\.json\.gz$", f).groups())
        df = pd.DataFrame(json.loads(gzip.decompress(Path(f).read_bytes()))["properties"]["parameter"])
        df = df[~df.index.str.endswith("13")]  # month 13 = POWER's annual value
        df.index = df.index.str[:4] + "-" + df.index.str[4:]
        cells[(lat, lon)] = df.replace(-999.0, np.nan)
    return cells


def district_monthly(geom, cells):
    w = {}
    for (lat, lon) in cells:
        a = box(lon - DLON / 2, lat - DLAT / 2, lon + DLON / 2, lat + DLAT / 2)
        share = a.intersection(geom).area / a.area
        if share > 0:
            w[(lat, lon)] = share
    cols = list(COLS)
    num = sum(cells[k][cols].fillna(0) * v for k, v in w.items())
    den = sum(cells[k][cols].notna() * v for k, v in w.items())
    out = (num / den.replace(0, np.nan))
    h = RD * (out.T2M + 273.15) / G * np.log(out.PS / out.PBLTOP)
    out = out.rename(columns={k: v[0] for k, v in COLS.items()})
    for k, (c, nd) in COLS.items():
        out[c] = out[c].round(nd)
    out["mixing_height_approx_m"] = h.round(0)
    out["ventilation_coefficient_approx_m2s"] = (h * out.wind_speed_10m_ms).round(0)
    out.index.name = "month"
    out.insert(0, "year", out.index.str[:4])
    return out, len(w)


def main():
    cells = load_cells()
    dists = districts()
    K = keys(dists)
    R, ncell = {}, {}
    for code, _, geom in dists:
        R[code], ncell[code] = district_monthly(geom, cells)
    df = assemble(R, K).sort_values(["district", "month"])
    df["source_flag"] = np.where(df.aod_550nm.isna(), "not_available", "")
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(Path(NAME) / f"{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, df.shape, "cells per district:", min(ncell.values()), "-", max(ncell.values()))
    print("blank cells per column:", df.isna().sum()[df.isna().sum() > 0].to_dict())
    print("AOD available from:", df.loc[df.aod_550nm.notna(), "month"].min())


if __name__ == "__main__":
    main()
