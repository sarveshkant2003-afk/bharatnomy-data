"""Download NASA POWER daily wind, humidity and temperature for every MERRA-2 grid cell over Maharashtra.

POWER's meteorology comes from the MERRA-2 reanalysis on a 0.5 deg (lat) x 0.625 deg (lon) grid. A point
request returns the values of the cell containing the point, so we request each cell centre once.

Writes _sources/nasa-power/raw/power_daily_<lat>_<lon>.json.gz (the API's JSON response, gzipped).
Skips cells already downloaded, so it can be re-run to resume.

Run from the repo root:  python3 pipelines/nasa-power/fetch_power.py
"""
import gzip
import json
import subprocess
import time
from pathlib import Path

import shapefile
from shapely.geometry import box, shape
from shapely.ops import unary_union

OUT = Path("_sources/nasa-power/raw")
SHP = "_sources/datameet-maps/raw/datameet-maps_census2011-districts_2011"
STATE_CENSUS = 27  # Maharashtra
PARAMS = "WS10M,WS10M_MAX,WS10M_MIN,WD10M,WS50M,WS50M_MAX,RH2M,T2M,T2M_MAX,T2MWET"
START, END = "19810101", "20251231"
URL = ("https://power.larc.nasa.gov/api/temporal/daily/point?parameters={p}&community=RE"
       "&longitude={lon}&latitude={lat}&start={s}&end={e}&format=JSON&time-standard=LST")
DLAT, DLON = 0.5, 0.625


def cells():
    r = shapefile.Reader(SHP)
    mh = unary_union([shape(s.shape.__geo_interface__).buffer(0) for s in r.shapeRecords()
                      if s.record.as_dict()["ST_CEN_CD"] == STATE_CENSUS])
    minx, miny, maxx, maxy = mh.bounds
    out = []
    i0, i1 = int((miny + 90) / DLAT) - 1, int((maxy + 90) / DLAT) + 2
    j0, j1 = int((minx + 180) / DLON) - 1, int((maxx + 180) / DLON) + 2
    for i in range(i0, i1):
        lat = -90 + i * DLAT
        for j in range(j0, j1):
            lon = -180 + j * DLON
            if box(lon - DLON / 2, lat - DLAT / 2, lon + DLON / 2, lat + DLAT / 2).intersects(mh):
                out.append((round(lat, 3), round(lon, 3)))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    todo = cells()
    print(len(todo), "cells")
    for k, (lat, lon) in enumerate(todo, 1):
        f = OUT / f"power_daily_{lat:.3f}_{lon:.3f}.json.gz"
        if f.exists():
            continue
        url = URL.format(p=PARAMS, lat=lat, lon=lon, s=START, e=END)
        for attempt in range(6):
            r = subprocess.run(["curl", "-s", "-m", "300", url], capture_output=True)
            try:
                d = json.loads(r.stdout)
                if "properties" in d:
                    break
            except Exception:
                pass
            time.sleep(15 * (attempt + 1))
        else:
            raise SystemExit(f"failed: {lat} {lon}")
        f.write_bytes(gzip.compress(r.stdout))
        if k % 20 == 0:
            print(k, "done")
        time.sleep(1)


if __name__ == "__main__":
    main()
