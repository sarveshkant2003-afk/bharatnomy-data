"""Coastal districts and their population, India, Census 2011 (BNY).

Input:  _sources/natural-earth/raw/ne_10m_coastline.zip                     (Natural Earth 1:10m coastline)
        _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011  (district boundaries, 2011)
        POP_census-pca_2011_STATES_ORGI_DIST                               (population)
Output: POP_coastal-districts_2011_STATES_BNY_DIST/<same>.csv

A district is coastal if its 2011 boundary comes within 0.01 degree (about 1 km) of the coastline; the tolerance
absorbs the mismatch between the two maps. Run from the repo root.
"""
import tempfile
import zipfile
from pathlib import Path

import math

import pandas as pd
import shapefile
from shapely.geometry import box, shape
from shapely.ops import unary_union

NE = "_sources/natural-earth/raw/ne_10m_coastline.zip"
SHP = "_sources/datameet-maps/raw/datameet-maps_census2011-districts_2011"
PCA = "POP_census-pca_2011_STATES_ORGI_DIST/POP_census-pca_2011_STATES_ORGI_DIST.csv"
NAME = "POP_coastal-districts_2011_STATES_BNY_DIST"
TOL = 0.01


def length_km(geom):
    """Length of a (multi)line in km, using a local equirectangular approximation per segment."""
    parts = getattr(geom, "geoms", [geom])
    total = 0.0
    for g in parts:
        if g.is_empty or g.geom_type not in ("LineString", "LinearRing"):
            continue
        c = list(g.coords)
        for (x1, y1), (x2, y2) in zip(c, c[1:]):
            k = math.cos(math.radians((y1 + y2) / 2))
            total += math.hypot((x2 - x1) * 111.32 * k, (y2 - y1) * 110.57)
    return total


def main():
    with tempfile.TemporaryDirectory() as t:
        zipfile.ZipFile(NE).extractall(t)
        lines = [shape(s.__geo_interface__) for s in shapefile.Reader(f"{t}/ne_10m_coastline").shapes()]
    bb = box(66, 5, 99, 38)
    coast = unary_union([l.intersection(bb) for l in lines if l.intersects(bb)])
    coastal, clen = {}, {}
    for sr in shapefile.Reader(SHP).shapeRecords():
        c = sr.record.as_dict()["censuscode"]
        if c:
            g = shape(sr.shape.__geo_interface__).buffer(0)
            coastal[f"{c:03d}"] = g.distance(coast) <= TOL
            clen[f"{c:03d}"] = round(length_km(coast.intersection(g.buffer(TOL))), 1) if coastal[f"{c:03d}"] else 0.0
    pca = pd.read_csv(PCA, dtype=str, keep_default_na=False)
    pca = pca[pca.area == "total"]
    d = pca[pca.district_census_code.isin(coastal)].copy()
    d["district"] = d.district.str.strip()
    d["is_coastal"] = d.district_census_code.map(lambda c: "yes" if coastal[c] else "no")
    d["coastline_within_1km_km"] = d.district_census_code.map(lambda c: f"{clen[c]:.1f}")
    out = d[["state_ut", "lgd_state_code", "district", "lgd_district_code", "district_census_code", "is_coastal", "coastline_within_1km_km",
             "population_persons", "population_males", "population_females", "households"]].copy()
    # state and All India totals of coastal population
    pop = out.assign(p=out.population_persons.astype(int))
    tot = []
    for s, g in pop.groupby("state_ut"):
        if (g.is_coastal == "yes").any():
            tot.append([s, g.lgd_state_code.iloc[0], "State total (coastal districts)", "", "", "yes", "", str(g[g.is_coastal == "yes"].p.sum()), "", "", ""])
    tot.append(["All India", "", "All India (coastal districts)", "", "", "yes", "", str(pop[pop.is_coastal == "yes"].p.sum()), "", "", ""])
    out = pd.concat([out.sort_values(["state_ut", "district"]), pd.DataFrame(tot, columns=out.columns)])
    out.insert(out.columns.get_loc("population_persons"), "year", "2011")
    Path(NAME).mkdir(exist_ok=True)
    out.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, out.shape, "coastal districts:", sum(coastal.values()), "coastal population:", pop[pop.is_coastal == "yes"].p.sum())


if __name__ == "__main__":
    main()
