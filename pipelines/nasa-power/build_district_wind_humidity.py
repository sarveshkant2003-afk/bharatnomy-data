"""Yearly wind and humidity indicators per Maharashtra district from NASA POWER daily data (MERRA-2).

Input:  _sources/nasa-power/raw/power_daily_<lat>_<lon>.json.gz  (fetch_power.py)
        _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011
        _reference/geography.csv
Output: CLM_wind-humidity_1981-to-2025_MH_BNY_DIST/CLM_wind-humidity_1981-to-2025_MH_BNY_DIST.csv

District daily value = area-weighted mean of the POWER cells (0.5 x 0.625 deg) overlapping the 2011 boundary.

Run from the repo root:  python3 pipelines/nasa-power/build_district_wind_humidity.py
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

RAW = "_sources/nasa-power/raw"
NAME = "CLM_wind-humidity_1981-to-2025_MH_BNY_DIST"
DLAT, DLON = 0.5, 0.625
SECTORS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
CALM_MS = 1.0      # our definition: daily mean 10 m wind below 1 m/s
STRONG_MS = 10.8   # our definition: daily maximum 10 m wind at least 10.8 m/s (Beaufort 6, strong breeze)


def load_cells():
    cells = {}
    for f in glob.glob(f"{RAW}/power_daily_*.json.gz"):
        lat, lon = map(float, re.search(r"_(-?[\d.]+)_(-?[\d.]+)\.json\.gz$", f).groups())
        p = json.loads(gzip.decompress(Path(f).read_bytes()))["properties"]["parameter"]
        df = pd.DataFrame(p)
        df.index = pd.to_datetime(df.index, format="%Y%m%d")
        cells[(lat, lon)] = df.replace(-999.0, np.nan)
    return cells


def district_daily(geom, cells):
    w = {}
    for (lat, lon) in cells:
        a = box(lon - DLON / 2, lat - DLAT / 2, lon + DLON / 2, lat + DLAT / 2)
        share = a.intersection(geom).area / a.area
        if share > 0:
            w[(lat, lon)] = share
    cols = ["WS10M", "WS10M_MAX", "WS50M", "RH2M", "T2MWET"]
    num = sum(cells[k][cols] * v for k, v in w.items())
    den = sum(cells[k][cols].notna() * v for k, v in w.items())
    out = num / den
    # wind direction: average the wind vectors (unit vectors weighted by speed), not the angles
    rad = {k: np.deg2rad(cells[k]["WD10M"]) for k in w}
    u = sum(np.sin(rad[k]) * cells[k]["WS10M"] * v for k, v in w.items())
    vv = sum(np.cos(rad[k]) * cells[k]["WS10M"] * v for k, v in w.items())
    out["WD10M"] = (np.rad2deg(np.arctan2(u, vv)) + 360) % 360
    return out, len(w)


def indices(d):
    rows = []
    for y, x in d.groupby(d.index.year):
        if x.WS10M.notna().sum() < 360:
            continue
        sector = pd.Series(np.array(SECTORS)[((x.WD10M + 22.5) % 360 // 45).astype(int)], index=x.index)
        top = sector.value_counts()
        jjas = x[x.index.month.isin([6, 7, 8, 9])]
        mam = x[x.index.month.isin([3, 4, 5])]
        rows.append(dict(
            year=y,
            wind_speed_10m_mean_ms=x.WS10M.mean(),
            wind_speed_50m_mean_ms=x.WS50M.mean(),
            wind_speed_10m_max_highest_ms=x.WS10M_MAX.max(),
            wind_direction_prevailing=top.index[0],
            wind_direction_prevailing_days=int(top.iloc[0]),
            calm_days_below_1ms=int((x.WS10M < CALM_MS).sum()),
            strong_wind_days_10_8ms=int((x.WS10M_MAX >= STRONG_MS).sum()),
            relative_humidity_mean_pct=x.RH2M.mean(),
            relative_humidity_mean_mar_may_pct=mam.RH2M.mean(),
            relative_humidity_mean_jun_sep_pct=jjas.RH2M.mean(),
            wet_bulb_temp_highest_c=x.T2MWET.max(),
            wet_bulb_temp_mean_mar_may_c=mam.T2MWET.mean(),
        ))
    r = pd.DataFrame(rows).set_index("year")
    return r


def main():
    cells = load_cells()
    dists = districts()
    K = keys(dists)
    R, ncell = {}, {}
    for code, _, geom in dists:
        d, ncell[code] = district_daily(geom, cells)
        R[code] = indices(d)
    df = assemble(R, K)
    for c in df.columns:
        if c.endswith(("_ms", "_c")):
            df[c] = df[c].round(2)
        elif c.endswith("_pct"):
            df[c] = df[c].round(1)
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(Path(NAME) / f"{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, df.shape, "cells per district:", min(ncell.values()), "-", max(ncell.values()))


if __name__ == "__main__":
    main()
