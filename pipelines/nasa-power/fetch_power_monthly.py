"""Download NASA POWER monthly aerosol, soil, evaporation and boundary-layer data for every MERRA-2 cell over Maharashtra.

Same cells as fetch_power.py. Writes _sources/nasa-power/raw/monthly/power_monthly_<lat>_<lon>.json.gz
(the API's JSON response, gzipped). Skips cells already downloaded.

Run from the repo root:  python3 pipelines/nasa-power/fetch_power_monthly.py
"""
import gzip
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_power import cells  # noqa: E402

OUT = Path("_sources/nasa-power/raw/monthly")
PARAMS = "AOD_55,GWETTOP,GWETROOT,GWETPROF,EVLAND,PBLTOP,PS,T2M,WS10M"
URL = ("https://power.larc.nasa.gov/api/temporal/monthly/point?parameters={p}&community=AG"
       "&longitude={lon}&latitude={lat}&start=1981&end=2025&format=JSON")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    todo = cells()
    for k, (lat, lon) in enumerate(todo, 1):
        f = OUT / f"power_monthly_{lat:.3f}_{lon:.3f}.json.gz"
        if f.exists():
            continue
        for attempt in range(6):
            r = subprocess.run(["curl", "-s", "-m", "300", URL.format(p=PARAMS, lat=lat, lon=lon)], capture_output=True)
            try:
                if "properties" in json.loads(r.stdout):
                    break
            except Exception:
                pass
            time.sleep(15 * (attempt + 1))
        else:
            raise SystemExit(f"failed: {lat} {lon}")
        f.write_bytes(gzip.compress(r.stdout))
        if k % 20 == 0:
            print(k, "of", len(todo))
        time.sleep(0.5)


if __name__ == "__main__":
    main()
