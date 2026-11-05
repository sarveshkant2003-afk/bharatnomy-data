"""Count NASA FIRMS MODIS vegetation fire detections per district per year, all India, 2001-2025.

Input:  _sources/nasa-firms/raw/firms_modis-india_YYYY.csv.gz           (fetch_firms.sh)
        _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011 (district boundaries, 2011)
        _reference/geography.csv                                          (names, LGD codes)
Output: ENV_active-fires_2001-to-2025_STATES_BNY_DIST/ENV_active-fires_2001-to-2025_STATES_BNY_DIST.csv

Run from the repo root:  python3 pipelines/nasa-firms/build_district_fires.py
"""
import glob
import re
from pathlib import Path

import numpy as np
import pandas as pd
import shapefile
from shapely import STRtree, points
from shapely.geometry import shape

RAW = "_sources/nasa-firms/raw"
SHP = "_sources/datameet-maps/raw/datameet-maps_census2011-districts_2011"
GEO = "_reference/geography.csv"
NAME = "ENV_active-fires_2001-to-2025_STATES_BNY_DIST"
FIRST, LAST = 2001, 2025  # 2000 starts in November (MODIS Terra began mid-2000)
SEASONS = {"jan_feb": (1, 2), "mar_may": (3, 5), "jun_sep": (6, 9), "oct_dec": (10, 12)}


def districts():
    r = shapefile.Reader(SHP)
    codes, geoms = [], []
    for sr in r.shapeRecords():
        if sr.record.as_dict()["censuscode"] == 0:
            continue  # one polygon has no Census code (area outside any 2011 district); its fires count as outside
        codes.append(f"{sr.record.as_dict()['censuscode']:03d}")
        geoms.append(shape(sr.shape.__geo_interface__).buffer(0))
    return codes, geoms


def keys(codes):
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    d = geo[(geo.level == "district") & (geo.census2011_district_code != "")]
    d = d.drop_duplicates("census2011_district_code").set_index("census2011_district_code")
    rows = []
    for c in sorted(set(codes)):
        if c not in d.index:
            raise SystemExit(f"Census 2011 district {c} not in geography.csv")
        r = d.loc[c]
        rows.append(dict(census=c, state_ut=r.state_ut, lgd_state_code=r.lgd_state_code, district=r.district,
                         lgd_district_code=r.lgd_district_code, district_census_code=c))
    return pd.DataFrame(rows)


def main():
    codes, geoms = districts()
    tree = STRtree(geoms)
    parts, outside = [], {}
    for f in sorted(glob.glob(f"{RAW}/firms_modis-india_*.csv.gz")):
        y = int(re.search(r"_(\d{4})\.csv\.gz$", f).group(1))
        if not FIRST <= y <= LAST:
            continue
        d = pd.read_csv(f, usecols=["latitude", "longitude", "acq_date", "confidence", "type"])
        d = d[d["type"] == 0]
        pts = points(d.longitude.values, d.latitude.values)
        pi, gi = tree.query(pts, predicate="within")
        # a point on a shared border can fall in two polygons: keep the first
        first = pd.Series(gi, index=pi).groupby(level=0).first()
        d = d.iloc[first.index].assign(census=[codes[g] for g in first.values])
        outside[y] = len(pts) - len(first)
        parts.append(d.assign(year=y, month=pd.to_datetime(d.acq_date).dt.month))
    p = pd.concat(parts)
    g = p.groupby(["census", "year"])
    out = pd.DataFrame({
        "fire_detections": g.size(),
        "fire_detections_confidence_30_plus": g.confidence.apply(lambda s: int((s >= 30).sum())),
    })
    for name, (a, b) in SEASONS.items():
        out[f"fire_detections_{name}"] = p[p.month.between(a, b)].groupby(["census", "year"]).size()
    # every district x year, zero where no fire was detected
    full = pd.MultiIndex.from_product([sorted(set(codes)), range(FIRST, LAST + 1)], names=["census", "year"])
    out = out.reindex(full).fillna(0).astype(int).reset_index()
    out = keys(codes).merge(out, on="census").drop(columns="census")
    out = out.sort_values(["state_ut", "district", "year"])
    Path(NAME).mkdir(exist_ok=True)
    out.to_csv(Path(NAME) / f"{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, out.shape)
    print("detections outside every district polygon, by year:", outside)
    s = out[[f"fire_detections_{n}" for n in SEASONS]].sum(axis=1)
    print("seasons != total:", int((s != out.fire_detections).sum()))


if __name__ == "__main__":
    main()
