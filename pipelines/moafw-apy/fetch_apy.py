"""Fetch district-wise crop Area, Production and Yield (APY) for every state, all crops and seasons, 1997-98 to
2022-23, from the DES (MoA&FW) crops APY report (https://data.desagri.gov.in/website/crops-apy-report-web).
One query per state ("All districts", "All crops", all seasons). No login.

Writes _sources/moafw-apy/raw/moafw-apy_district-<statecode>_1997-to-2022.html (the report HTML as returned).
Run from the repo root:  python3 pipelines/moafw-apy/fetch_apy.py
"""
import re
import time
from pathlib import Path

import requests

RAW = Path("_sources/moafw-apy/raw")
PAGE = "https://data.desagri.gov.in/website/crops-apy-report-web"
POST = "https://data.desagri.gov.in/report/crop/horizontal_crop_vertical_year"


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0"
    page = s.get(PAGE, timeout=60).text
    token = (re.search(r'id="hdnrltoken"[^>]*value="([^"]+)"', page) or re.search(r'name="_token" value="([^"]+)"', page)).group(1)
    sel = re.search(r'name="fltrstates\[\]"[^>]*>(.*?)</select>', page, re.S).group(1)
    states = [(v, n.strip()) for v, n in re.findall(r'<option[^>]*value="(\d+)"[^>]*>([^<]*)', sel)]
    years = sorted(re.findall(r'<option value="(\d{4})"', re.search(r'name="fltrstartyear"[^>]*>(.*?)</select>', page, re.S).group(1)))
    (RAW / "moafw-apy_states.tsv").write_text("".join(f"{v}\t{n}\n" for v, n in states))
    print(len(states), "states; years", years[0], "-", years[-1])
    for code, name in states:
        f = RAW / f"moafw-apy_district-{int(code):02d}_{years[0]}-to-{years[-1]}.html"
        if f.exists() and f.stat().st_size > 1000:
            continue
        data = [("reportformat", "horizontal_crop_vertical_year"), ("fltrstates[]", code), ("fltrdistricts[]", ""),
                ("fltrcrops[]", ""), ("fltrseason[]", ""), ("fltrstartyear", years[0]), ("fltrendyear", years[-1]),
                ("fltrrptformat", "scrview"), ("_token", token)]
        r = s.post(POST, data=data, headers={"X-Requested-With": "XMLHttpRequest"}, timeout=1800)
        r.raise_for_status()
        f.write_text(r.text, encoding="utf-8")
        print(code, name, len(r.text))
        time.sleep(2)


if __name__ == "__main__":
    main()
