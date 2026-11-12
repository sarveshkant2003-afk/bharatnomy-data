"""Built-up surface per district, all India, 1975 to 2030 (BNY from JRC GHSL GHS-BUILT-S R2023A).

Input:  _sources/jrc-ghsl/raw/GHS_BUILT_S[_NRES]_E<year>_GLOBE_R2023A_4326_30ss_V1_0.tif  (fetch_ghsl.sh)
        _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011
        _reference/geography.csv
Output: ENV_built-up-surface_1975-to-2030_STATES_BNY_DIST/<same>.csv

Each grid cell (30 arc-seconds, about 0.9 x 0.9 km) holds square metres of built-up surface. A cell belongs to the
district that contains its centre. District built-up = sum of its cells; district land area = sum of the cells'
areas on the WGS84 ellipsoid (cells are not equal-area). Run from the repo root.
"""
import glob
import re
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
import shapefile
from rasterio.features import rasterize
from rasterio.windows import from_bounds
from shapely.geometry import shape

RAW = "_sources/jrc-ghsl/raw"
SHP = "_sources/datameet-maps/raw/datameet-maps_census2011-districts_2011"
GEO = "_reference/geography.csv"
NAME = "ENV_built-up-surface_1975-to-2030_STATES_BNY_DIST"
BOUNDS = (68.0, 6.0, 98.0, 37.5)  # lon/lat box around India


def districts():
    r = shapefile.Reader(SHP)
    out = []
    for sr in r.shapeRecords():
        c = sr.record.as_dict()["censuscode"]
        if c:
            out.append((int(c), shape(sr.shape.__geo_interface__).buffer(0)))
    return out


def cell_area_m2(transform, h, w):
    """Area of each row's cells on the WGS84 ellipsoid (authalic-latitude formula)."""
    a, e2 = 6378137.0, 0.00669437999014
    e = np.sqrt(e2)
    top = transform.f
    dy, dx = -transform.e, transform.a
    lat1 = np.deg2rad(top - np.arange(h) * dy)
    lat2 = np.deg2rad(top - (np.arange(h) + 1) * dy)

    def q(phi):
        s = np.sin(phi)
        return (1 - e2) * (s / (1 - e2 * s * s) - (1 / (2 * e)) * np.log((1 - e * s) / (1 + e * s)))
    return (a * a / 2) * np.abs(q(lat1) - q(lat2)) * np.deg2rad(dx)


def keys():
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    d = geo[(geo.level == "district") & (geo.census2011_district_code != "")]
    d = d.drop_duplicates("census2011_district_code").set_index("census2011_district_code")
    return d


def main():
    files = sorted(glob.glob(f"{RAW}/GHS_BUILT_S_E*_4326_30ss_V1_0.tif"))
    dists = districts()
    with rasterio.open(files[0]) as src:
        win = from_bounds(*BOUNDS, transform=src.transform).round_offsets().round_lengths()
        tr = src.window_transform(win)
        h, w = int(win.height), int(win.width)
    ids = rasterize(((g, c) for c, g in dists), out_shape=(h, w), transform=tr, fill=0, dtype="int32")
    area = np.repeat(cell_area_m2(tr, h, w)[:, None], w, axis=1)
    flat = ids.ravel()
    inside = flat > 0
    codes = np.unique(flat[inside])
    land = pd.Series(np.bincount(flat[inside], weights=area.ravel()[inside]))[codes]
    rows = []
    for kind, pat in (("total", "GHS_BUILT_S_E"), ("non_residential", "GHS_BUILT_S_NRES_E")):
        for f in sorted(glob.glob(f"{RAW}/{pat}*_4326_30ss_V1_0.tif")):
            year = int(re.search(r"_E(\d{4})_", f).group(1))
            with rasterio.open(f) as src:
                v = src.read(1, window=win).astype("float64")
                if src.nodata is not None:
                    v[v == src.nodata] = 0
            s = pd.Series(np.bincount(flat[inside], weights=v.ravel()[inside]))[codes]
            rows.append(pd.DataFrame({"census": codes, "year": year, "kind": kind, "m2": s.values}))
            print(Path(f).name, "India total built-up km2:", round(s.sum() / 1e6))
    r = pd.concat(rows).pivot_table(index=["census", "year"], columns="kind", values="m2").reset_index()
    r["area"] = r.census.map(land)
    k = keys()
    out = pd.DataFrame({
        "state_ut": [k.at[f"{c:03d}", "state_ut"] for c in r.census],
        "lgd_state_code": [k.at[f"{c:03d}", "lgd_state_code"] for c in r.census],
        "district": [k.at[f"{c:03d}", "district"] for c in r.census],
        "lgd_district_code": [k.at[f"{c:03d}", "lgd_district_code"] for c in r.census],
        "district_census_code": [f"{c:03d}" for c in r.census],
        "year": r.year,
        "built_up_sq_km": (r["total"] / 1e6).round(3),
        "built_up_non_residential_sq_km": (r["non_residential"] / 1e6).round(3),
        "grid_land_area_sq_km": (r.area / 1e6).round(1),
        "built_up_pct_of_area": (100 * r["total"] / r.area).round(3),
        "source_flag": np.where(r.year > 2020, "estimated", ""),
    })
    out = out.sort_values(["state_ut", "district", "year"])
    Path(NAME).mkdir(exist_ok=True)
    out.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, out.shape, "districts:", out.district_census_code.nunique())


if __name__ == "__main__":
    main()
