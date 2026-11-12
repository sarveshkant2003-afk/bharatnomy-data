"""Count IMD best-track systems crossing each district per year, all India, 1982-2025 (BNY).

Input:  CLM_cyclone-best-tracks_1982-to-2026_IN_IMD/<same>.csv                 (build_best_tracks.py)
        _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011     (district boundaries, 2011)
        _reference/geography.csv                                               (names, LGD codes)
Output: CLM_cyclone-crossings_1982-to-2025_STATES_BNY_DIST/<same>.csv

Each system's consecutive track points (same year and serial, in time order) are joined by straight
lines. A system "crosses" a district if its track line touches the district polygon. The strength of
a line segment is the higher maximum sustained wind of its two ends. 2026 is left out (tentative).
Run from the repo root.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import shapefile
from shapely import STRtree
from shapely.geometry import LineString, Point, shape

TRACKS = "CLM_cyclone-best-tracks_1982-to-2026_IN_IMD/CLM_cyclone-best-tracks_1982-to-2026_IN_IMD.csv"
SHP = "_sources/datameet-maps/raw/datameet-maps_census2011-districts_2011"
GEO = "_reference/geography.csv"
NAME = "CLM_cyclone-crossings_1982-to-2025_STATES_BNY_DIST"
FIRST, LAST = 1982, 2025


def districts():
    r = shapefile.Reader(SHP)
    codes, geoms = [], []
    for sr in r.shapeRecords():
        c = sr.record.as_dict()["censuscode"]
        if c == 0:
            continue
        codes.append(f"{c:03d}")
        geoms.append(shape(sr.shape.__geo_interface__).buffer(0))
    return codes, geoms


def keys(codes):
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    d = geo[(geo.level == "district") & (geo.census2011_district_code != "")]
    d = d.drop_duplicates("census2011_district_code").set_index("census2011_district_code")
    return pd.DataFrame([dict(census=c, state_ut=d.at[c, "state_ut"], lgd_state_code=d.at[c, "lgd_state_code"],
                              district=d.at[c, "district"], lgd_district_code=d.at[c, "lgd_district_code"],
                              district_census_code=c) for c in sorted(set(codes))])


def main():
    codes, geoms = districts()
    tree = STRtree(geoms)
    t = pd.read_csv(TRACKS, dtype=str, keep_default_na=False)
    t = t[t.year.astype(int).between(FIRST, LAST)].copy()
    for c in ("latitude_deg_n", "longitude_deg_e", "max_sustained_wind_kt"):
        t[c] = pd.to_numeric(t[c], errors="coerce")
    hits = {}  # (census, year, system) -> max segment wind
    for (year, serial), s in t.groupby(["year", "serial"], sort=False):
        s = s.sort_values(["date", "time_utc"], kind="stable")
        xy = list(zip(s.longitude_deg_e, s.latitude_deg_n))
        w = s.max_sustained_wind_kt.tolist()
        segs = [(LineString([xy[i], xy[i + 1]]) if xy[i] != xy[i + 1] else Point(xy[i]), np.nanmax([w[i], w[i + 1]]) if not (np.isnan(w[i]) and np.isnan(w[i + 1])) else np.nan)
                for i in range(len(xy) - 1)] or [(Point(xy[0]), w[0])]
        for geom, wind in segs:
            for gi in tree.query(geom, predicate="intersects"):
                k = (codes[gi], int(year), serial)
                prev = hits.get(k, np.nan)
                hits[k] = wind if np.isnan(prev) else (prev if np.isnan(wind) else max(prev, wind))
    h = pd.DataFrame([(c, y, s, w) for (c, y, s), w in hits.items()], columns=["census", "year", "system", "wind"])
    g = h.groupby(["census", "year"])
    out = pd.DataFrame({
        "systems_crossing": g.size(),
        "cyclonic_storms_crossing_34kt": g.wind.apply(lambda x: int((x >= 34).sum())),
        "severe_cyclonic_storms_crossing_48kt": g.wind.apply(lambda x: int((x >= 48).sum())),
        "very_severe_cyclonic_storms_crossing_64kt": g.wind.apply(lambda x: int((x >= 64).sum())),
        "max_wind_over_district_kt": g.wind.max(),
    })
    full = pd.MultiIndex.from_product([sorted(set(codes)), range(FIRST, LAST + 1)], names=["census", "year"])
    out = out.reindex(full)
    cnt = [c for c in out.columns if c != "max_wind_over_district_kt"]
    out[cnt] = out[cnt].fillna(0).astype(int)
    out["max_wind_over_district_kt"] = out.max_wind_over_district_kt.map(lambda v: "" if np.isnan(v) else f"{v:g}")
    out = keys(codes).merge(out.reset_index(), on="census").drop(columns="census")
    out = out.sort_values(["state_ut", "district", "year"])
    Path(NAME).mkdir(exist_ok=True)
    out.to_csv(Path(NAME) / f"{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, out.shape, "district-years with a crossing:", int((out.systems_crossing > 0).sum()))


if __name__ == "__main__":
    main()
