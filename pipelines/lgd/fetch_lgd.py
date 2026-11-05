"""Fetch states, districts and sub-districts from the Local Government Directory (LGD) web service.

Writes the raw JSON responses to _sources/lgd/raw/:
  lgd_states.json, lgd_districts.json (list per state), lgd_subdistricts.json (list per district)

Run from the repo root:  python3 pipelines/lgd/fetch_lgd.py [--fresh]
(--fresh re-downloads states and districts; otherwise the saved lists are reused and only sub-districts are fetched/resumed)
"""
import json, subprocess, sys, time, urllib.parse
from pathlib import Path

BASE = "https://lgdirectory.gov.in/webservices/lgdws/"
OUT = Path("_sources/lgd/raw")


def post(endpoint, **params):
    # curl, not urllib: the macOS system Python's SSL library fails the handshake with lgdirectory.gov.in
    cmd = ["curl", "-s", "-m", "60", "-X", "POST", "-A", "Mozilla/5.0 (bharatnomy-data)",
           "-H", "Content-Type: application/x-www-form-urlencoded",
           "--data", urllib.parse.urlencode(params), BASE + endpoint]
    for attempt in range(8):
        try:
            return json.loads(subprocess.run(cmd, capture_output=True, check=True).stdout)
        except Exception:
            if attempt == 7:
                raise
            time.sleep(10 * (attempt + 1))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # stateList ignores stateCode and returns every state; a parameter is required
    sf, df = OUT / "lgd_states.json", OUT / "lgd_districts.json"
    if sf.exists() and df.exists() and "--fresh" not in sys.argv:
        states, districts = json.loads(sf.read_text()), json.loads(df.read_text())
    else:
        # stateList ignores stateCode and returns every state; a parameter is required
        states = post("stateList", stateCode=0)
        sf.write_text(json.dumps(states, ensure_ascii=False, indent=1))
        districts = {}
        for s in sorted(states, key=lambda x: x["stateCode"]):
            districts[str(s["stateCode"])] = post("districtList", stateCode=s["stateCode"])
            time.sleep(0.3)
        df.write_text(json.dumps(districts, ensure_ascii=False, indent=1))
    # sub-districts: resumable, progress kept in a partial file until complete
    part = OUT / "lgd_subdistricts.partial.json"
    subd = json.loads(part.read_text()) if part.exists() else {}
    todo = [d["districtCode"] for ds in districts.values() for d in ds if str(d["districtCode"]) not in subd]
    for i, dc in enumerate(todo, 1):
        subd[str(dc)] = post("subdistrictList", districtCode=dc)
        time.sleep(0.3)
        if i % 10 == 0:
            part.write_text(json.dumps(subd, ensure_ascii=False))
    (OUT / "lgd_subdistricts.json").write_text(json.dumps(subd, ensure_ascii=False, indent=1))
    part.unlink(missing_ok=True)
    print(len(states), "states;", sum(map(len, districts.values())), "districts;",
          sum(map(len, subd.values())), "sub-districts")


if __name__ == "__main__":
    main()
