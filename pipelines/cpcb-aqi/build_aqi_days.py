"""Yearly AQI summary per city from the CPCB daily AQI bulletins already in the repo.

Input:  ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY/ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY.csv
        (itself parsed from the bulletin PDFs in _sources/cpcb-aqi-bulletin/raw/)
Output: ENV_aqi-days-by-category_2015-to-2026_STATES_BNY_CITY/ENV_aqi-days-by-category_2015-to-2026_STATES_BNY_CITY.csv

Run from the repo root:  python3 pipelines/cpcb-aqi/build_aqi_days.py
"""
from pathlib import Path

import pandas as pd

SRC = "ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY"
NAME = "ENV_aqi-days-by-category_2015-to-2026_STATES_BNY_CITY"
CATS = {"Good": "days_good", "Satisfactory": "days_satisfactory", "Moderate": "days_moderate",
        "Poor": "days_poor", "Very Poor": "days_very_poor", "Severe": "days_severe"}


def main():
    d = pd.read_csv(Path(SRC) / f"{SRC}.csv", dtype={"aqi": float})
    d["year"] = d.date.str[:4].astype(int)
    g = d.groupby(["city", "year"])
    out = pd.DataFrame({"days_reported": g.size()})
    cat = pd.crosstab([d.city, d.year], d.air_quality).rename(columns=CATS)
    for c in CATS.values():
        out[c] = cat[c] if c in cat else 0
    out["days_very_poor_or_severe"] = out.days_very_poor + out.days_severe
    out["days_aqi_above_100"] = g.aqi.apply(lambda s: int((s > 100).sum()))
    out["aqi_mean"] = g.aqi.mean().round(1)
    out["aqi_highest"] = g.aqi.max()
    pm = d.prominent_pollutants.fillna("")
    for p, col in (("PM2.5", "days_pm25_prominent"), ("PM10", "days_pm10_prominent"), ("O3", "days_o3_prominent")):
        out[col] = d.assign(x=pm.str.contains(p, regex=False)).groupby(["city", "year"]).x.sum()
    out["stations_reporting_max"] = g.stations_reporting.max()
    out = out.reset_index()
    ints = [c for c in out if c.startswith("days_") or c in ("aqi_highest", "stations_reporting_max")]
    out[ints] = out[ints].astype("Int64")
    Path(NAME).mkdir(exist_ok=True)
    out.sort_values(["city", "year"]).to_csv(Path(NAME) / f"{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, out.shape)
    # checks
    s = out[list(CATS.values())].sum(axis=1)
    print("category days != days reported:", int((s != out.days_reported).sum()))
    print("days_aqi_above_100 != moderate+poor+very poor+severe:",
          int((out.days_aqi_above_100 != out[["days_moderate", "days_poor", "days_very_poor", "days_severe"]].sum(axis=1)).sum()))


if __name__ == "__main__":
    main()
