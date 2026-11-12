"""Mean wind power density and wind speed at 100 m per district, India (BNY from Global Wind Atlas v3).

Input:  _sources/global-wind-atlas/raw/gwa_IND_power-density_100m.tif, gwa_IND_wind-speed_100m.tif (fetch_gwa.sh)
        _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011
        _reference/geography.csv
Output: CLM_wind-resource-100m_2008-to-2017_STATES_BNY_DIST/<same>.csv

District value = mean of the 250 m cells whose centre lies inside the district's 2011 boundary (plain mean over
cells; cells are near-equal in area at a given latitude). Also the 90th percentile of power density, since wind
farms are sited on the windiest spots. Run from the repo root.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
import rasterio.mask
import shapefile
from shapely.geometry import mapping, shape

RAW = "_sources/global-wind-atlas/raw"
SHP = "_sources/datameet-maps/raw/datameet-maps_census2011-districts_2011"
GEO = "_reference/geography.csv"
NAME = "CLM_wind-resource-100m_2008-to-2017_STATES_BNY_DIST"


def stats(src, geom):
    try:
        a, _ = rasterio.mask.mask(src, [mapping(geom)], crop=True, filled=False)
    except ValueError:  # district outside the GWA India raster
        return np.array([])
    v = a[0].compressed().astype("float64")
    v = v[np.isfinite(v) & (v >= 0)]
    return v


def main():
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    k = geo[(geo.level == "district") & (geo.census2011_district_code != "")].drop_duplicates("census2011_district_code").set_index("census2011_district_code")
    rows = []
    with rasterio.open(f"{RAW}/gwa_IND_power-density_100m.tif") as pd_src, rasterio.open(f"{RAW}/gwa_IND_wind-speed_100m.tif") as ws_src:
        for sr in shapefile.Reader(SHP).shapeRecords():
            c = sr.record.as_dict()["censuscode"]
            if not c:
                continue
            g = shape(sr.shape.__geo_interface__).buffer(0)
            p = stats(pd_src, g)
            w = stats(ws_src, g)
            cc = f"{c:03d}"
            expected = g.area / (pd_src.res[0] * pd_src.res[1])  # cells the district would have if fully covered
            rows.append(dict(state_ut=k.at[cc, "state_ut"], lgd_state_code=k.at[cc, "lgd_state_code"], district=k.at[cc, "district"],
                             lgd_district_code=k.at[cc, "lgd_district_code"], district_census_code=cc,
                             power_density_100m_mean_w_m2=round(p.mean(), 1) if len(p) else "",
                             power_density_100m_p90_w_m2=round(float(np.percentile(p, 90)), 1) if len(p) else "",
                             wind_speed_100m_mean_ms=round(w.mean(), 2) if len(w) else "",
                             wind_speed_100m_p90_ms=round(float(np.percentile(w, 90)), 2) if len(w) else "",
                             raster_coverage_pct=round(min(100.0, 100 * len(p) / expected), 1), source_flag="" if len(p) else "not_available"))
    df = pd.DataFrame(rows).sort_values(["state_ut", "district"])
    low = df.raster_coverage_pct < 50  # values from a sliver of the district would mislead: leave blank
    vcols = ["power_density_100m_mean_w_m2", "power_density_100m_p90_w_m2", "wind_speed_100m_mean_ms", "wind_speed_100m_p90_ms"]
    df.loc[low, vcols] = ""
    df.loc[low, "source_flag"] = "not_available"
    print("districts with coverage below 90%:", df[df.raster_coverage_pct < 90][["district", "raster_coverage_pct"]].values.tolist())
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, df.shape)
    return df


if __name__ == "__main__":
    main()
