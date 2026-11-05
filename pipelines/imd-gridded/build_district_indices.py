"""District rainfall and temperature indices for Maharashtra from IMD Pune daily gridded data.

Writes three datasets (BNY = computed by Bharatnomy from IMD data):
  CLM_rainfall-indices_1951-to-2025_MH_BNY_DIST        one row per district per year
  CLM_rainfall-variability_1971-to-2020_MH_BNY_DIST    one row per district (variability over the base period)
  CLM_temperature-indices_1951-to-2024_MH_BNY_DIST     one row per district per year

Inputs
  _sources/imd-gridded/raw/imd-gridded_{rain-025deg,tmax-1deg,tmin-1deg}_YYYY.grd   (not committed; see its README)
  _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011.shp             (district boundaries, 2011)
  _reference/geography.csv                                                            (LGD codes)

Method
  * District daily value = area-weighted mean of the grid cells overlapping the district's 2011 boundary
    (weight = share of the cell's area inside the district; cells IMD marks as missing are skipped that day).
  * Indices are computed on that district-average daily series.

Run from the repo root:  python3 pipelines/imd-gridded/build_district_indices.py
"""
import calendar
import glob
import re
from pathlib import Path

import numpy as np
import pandas as pd
import shapefile
from scipy import stats
from shapely.geometry import box, shape

RAW = Path("_sources/imd-gridded/raw")
SHP = Path("_sources/datameet-maps/raw/datameet-maps_census2011-districts_2011")
GEO = Path("_reference/geography.csv")
STATE_CENSUS = 27  # Maharashtra
LPA = (1971, 2020)      # IMD's long period average for rainfall
NORMAL = (1991, 2020)   # IMD's current climatological normal for temperature

RAIN_GRID = dict(shape=(129, 135), lat0=6.5, lon0=66.5, step=0.25, missing=lambda a: a < -1)
TEMP_GRID = dict(shape=(31, 31), lat0=7.5, lon0=67.5, step=1.0, missing=lambda a: a > 90)

NAMES = {
    "rain": "CLM_rainfall-indices_1951-to-2025_MH_BNY_DIST",
    "var": "CLM_rainfall-variability_1971-to-2020_MH_BNY_DIST",
    "temp": "CLM_temperature-indices_1951-to-2024_MH_BNY_DIST",
}


def ndays(y):
    return 366 if calendar.isleap(y) else 365


# ---------------------------------------------------------------- districts and weights

def districts():
    r = shapefile.Reader(str(SHP))
    out = []
    for sr in r.shapeRecords():
        rec = sr.record.as_dict()
        if rec["ST_CEN_CD"] == STATE_CENSUS:
            out.append((f"{rec['censuscode']:03d}", rec["DISTRICT"], shape(sr.shape.__geo_interface__).buffer(0)))
    return sorted(out)


def weights(geom, g):
    """{(i, j): share of cell (i, j) inside geom}, i = lat index, j = lon index."""
    h = g["step"] / 2
    minx, miny, maxx, maxy = geom.bounds
    w = {}
    for i in range(g["shape"][0]):
        lat = g["lat0"] + i * g["step"]
        if lat + h < miny or lat - h > maxy:
            continue
        for j in range(g["shape"][1]):
            lon = g["lon0"] + j * g["step"]
            if lon + h < minx or lon - h > maxx:
                continue
            cell = box(lon - h, lat - h, lon + h, lat + h)
            a = cell.intersection(geom).area / cell.area
            if a > 0:
                w[(i, j)] = a
    return w


def district_series(kind, g, dists):
    """DataFrame (date x census code) of area-weighted daily means."""
    W = {}
    for code, _, geom in dists:
        w = weights(geom, g)
        W[code] = (np.array([k[0] for k in w]), np.array([k[1] for k in w]), np.array(list(w.values())))
    parts = []
    for f in sorted(glob.glob(str(RAW / f"imd-gridded_{kind}_*.grd"))):
        y = int(re.search(r"_(\d{4})\.grd$", f).group(1))
        a = np.fromfile(f, dtype="<f4").reshape(ndays(y), *g["shape"]).astype(float)
        a[g["missing"](a)] = np.nan
        cols = {}
        for code, (ii, jj, ww) in W.items():
            v = a[:, ii, jj]                     # days x cells
            m = ~np.isnan(v)
            wsum = (m * ww).sum(axis=1)
            cols[code] = np.where(wsum > 0, np.nansum(v * ww, axis=1) / np.where(wsum > 0, wsum, 1), np.nan)
        parts.append(pd.DataFrame(cols, index=pd.date_range(f"{y}-01-01", periods=ndays(y))))
    cells = {code: len(W[code][2]) for code in W}
    return pd.concat(parts), cells


# ---------------------------------------------------------------- rainfall

def longest_run(mask):
    best = cur = 0
    for v in mask:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best


def dry_spells(mask, min_len=7):
    """Number of runs of at least min_len consecutive True values."""
    n = cur = 0
    for v in list(mask) + [False]:
        if v:
            cur += 1
        else:
            n += cur >= min_len
            cur = 0
    return n


def spi(x):
    """Standardised Precipitation Index of yearly totals x (Series by year): gamma distribution fitted
    to the LPA years, with the share of zero totals handled as in McKee et al. (1993)."""
    base = x[(x.index >= LPA[0]) & (x.index <= LPA[1])].dropna()
    q = (base == 0).mean()
    a, loc, scale = stats.gamma.fit(base[base > 0], floc=0)
    p = q + (1 - q) * stats.gamma.cdf(x, a, loc=0, scale=scale)
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return pd.Series(stats.norm.ppf(p), index=x.index).where(x.notna())


def rain_indices(s):
    """s: daily district rainfall (mm) for one district. Returns one row per complete year."""
    rows = []
    for y, d in s.groupby(s.index.year):
        if d.notna().sum() < ndays(y):
            continue
        m = d.index.month
        jjas = d[(m >= 6) & (m <= 9)]
        rows.append(dict(
            year=y,
            rainfall_annual_mm=d.sum(),
            rainfall_mar_may_mm=d[(m >= 3) & (m <= 5)].sum(),
            rainfall_jun_sep_mm=jjas.sum(),
            rainfall_oct_dec_mm=d[m >= 10].sum(),
            rainy_days_2_5mm=int((d >= 2.5).sum()),
            heavy_rain_days_64_5mm=int((d >= 64.5).sum()),
            very_heavy_rain_days_115_6mm=int((d >= 115.6).sum()),
            extremely_heavy_rain_days_204_5mm=int((d >= 204.5).sum()),
            rx1day_mm=d.max(),
            rx5day_mm=d.rolling(5).sum().max(),
            consecutive_dry_days=longest_run(d < 1),
            monsoon_dry_spells_7day=dry_spells(jjas < 2.5),
            monsoon_longest_dry_spell_days=longest_run(jjas < 2.5),
        ))
    r = pd.DataFrame(rows).set_index("year")
    for col, short in (("rainfall_annual_mm", "annual"), ("rainfall_mar_may_mm", "mar_may"),
                       ("rainfall_jun_sep_mm", "jun_sep"), ("rainfall_oct_dec_mm", "oct_dec")):
        lpa = r.loc[LPA[0]:LPA[1], col].mean()
        r[f"rainfall_{short}_departure_pct"] = 100 * (r[col] / lpa - 1)
    r["spi_annual"] = spi(r["rainfall_annual_mm"])
    r["spi_jun_sep"] = spi(r["rainfall_jun_sep_mm"])
    return r


def rain_variability(r):
    b = r.loc[LPA[0]:LPA[1]]
    out = {}
    for col, short in (("rainfall_annual_mm", "annual"), ("rainfall_jun_sep_mm", "jun_sep")):
        out[f"rainfall_{short}_mean_mm"] = b[col].mean()
        out[f"rainfall_{short}_sd_mm"] = b[col].std(ddof=1)
        out[f"rainfall_{short}_cv_pct"] = 100 * b[col].std(ddof=1) / b[col].mean()
    out["years"] = int(b["rainfall_annual_mm"].notna().sum())
    return out


# ---------------------------------------------------------------- temperature

def doy365(idx):
    return np.minimum(idx.dayofyear, 365)


def daily_normal(s):
    base = s[(s.index.year >= NORMAL[0]) & (s.index.year <= NORMAL[1])]
    clim = base.groupby(doy365(base.index)).mean().reindex(range(1, 366))
    ext = pd.concat([clim.iloc[-15:], clim, clim.iloc[:15]])
    return pd.Series(ext.rolling(31, center=True).mean().iloc[15:-15].values, index=range(1, 366))


def p90(s):
    base = s[(s.index.year >= NORMAL[0]) & (s.index.year <= NORMAL[1])]
    doy = doy365(base.index)
    return pd.Series({d: np.nanpercentile(base.values[np.isin(doy, [((d - 1 + k) % 365) + 1 for k in range(-2, 3)])], 90)
                      for d in range(1, 366)})


def temp_indices(tmax, tmin):
    dmax = tmax - daily_normal(tmax).reindex(doy365(tmax.index)).values
    dmin = tmin - daily_normal(tmin).reindex(doy365(tmin.index)).values
    T = pd.DataFrame({
        "tmax": tmax, "tmin": tmin,
        "hw": (tmax >= 40) & ((dmax >= 4.5) | (tmax >= 45)),
        "severe": (tmax >= 40) & ((dmax >= 6.5) | (tmax >= 47)),
        "warm": (dmin >= 4.5) & (tmax >= 40),
        "hot": tmax > p90(tmax).reindex(doy365(tmax.index)).values,
        "hotnight": tmin > p90(tmin).reindex(doy365(tmin.index)).values,
    })
    mam = T[T.index.month.isin([3, 4, 5])]
    g, gm = T.groupby(T.index.year), mam.groupby(mam.index.year)
    r = pd.DataFrame({
        "tmax_mean_c": g["tmax"].mean(),
        "tmin_mean_c": g["tmin"].mean(),
        "tmax_highest_c": g["tmax"].max(),
        "tmin_highest_c": g["tmin"].max(),
        "tmin_lowest_c": g["tmin"].min(),
        "tmax_mean_mar_may_c": gm["tmax"].mean(),
        "tmin_mean_mar_may_c": gm["tmin"].mean(),
        "days_tmax_40c_or_more": g["tmax"].apply(lambda s: int((s >= 40).sum())),
        "days_tmax_45c_or_more": g["tmax"].apply(lambda s: int((s >= 45).sum())),
        "heatwave_days": g["hw"].sum().astype(int),
        "severe_heatwave_days": g["severe"].sum().astype(int),
        "warm_nights": g["warm"].sum().astype(int),
        "days_tmax_above_p90": g["hot"].sum().astype(int),
        "nights_tmin_above_p90": g["hotnight"].sum().astype(int),
    })
    complete = (g["tmax"].count() >= 360) & (g["tmin"].count() >= 360)
    r = r[complete]
    r.index.name = "year"
    return r


# ---------------------------------------------------------------- output

def keys(dists):
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    geo = geo[(geo.level == "district") & (geo.census2011_district_code != "")]
    k = []
    for code, name, _ in dists:
        hit = geo[geo.census2011_district_code == code]
        if len(hit) != 1:
            raise SystemExit(f"Census 2011 district {code} {name}: {len(hit)} matches in geography.csv")
        h = hit.iloc[0]
        k.append(dict(census=code, state_ut="Maharashtra", lgd_state_code=h.lgd_state_code,
                      district=h.district, lgd_district_code=h.lgd_district_code, district_census_code=code))
    return pd.DataFrame(k)


def write(name, df, ints=()):
    for c in df.columns:
        if c in ints:
            df[c] = df[c].astype("Int64")
    out = Path(name)
    out.mkdir(exist_ok=True)
    df.to_csv(out / f"{name}.csv", index=False, lineterminator="\n")
    print(name, df.shape)


def assemble(per_district, K):
    parts = []
    for code, r in per_district.items():
        r = r.reset_index()
        k = K[K.census == code].drop(columns="census").iloc[0]
        for i, c in enumerate(reversed(list(k.index))):
            r.insert(0, c, k[c])
        parts.append(r)
    return pd.concat(parts).sort_values(["district", "year"]).reset_index(drop=True)


def main():
    dists = districts()
    K = keys(dists)

    rain, rcells = district_series("rain-025deg", RAIN_GRID, dists)
    R = {code: rain_indices(rain[code]) for code, _, _ in dists}
    df = assemble(R, K)
    one = [c for c in df.columns if c.endswith(("_mm", "_pct"))]
    df[one] = df[one].round(1)
    df[["spi_annual", "spi_jun_sep"]] = df[["spi_annual", "spi_jun_sep"]].round(2)
    write(NAMES["rain"], df, ints=[c for c in df.columns if "days" in c or "spells" in c])

    V = pd.DataFrame([dict(census=code, **rain_variability(R[code])) for code, _, _ in dists])
    V = K.merge(V, on="census").drop(columns="census").sort_values("district")
    V.insert(V.columns.get_loc("district_census_code") + 1, "period", f"{LPA[0]}-{LPA[1]}")
    V[[c for c in V.columns if c.endswith(("_mm", "_pct"))]] = V[[c for c in V.columns if c.endswith(("_mm", "_pct"))]].round(1)
    write(NAMES["var"], V, ints=["years"])

    tmax, tcells = district_series("tmax-1deg", TEMP_GRID, dists)
    tmin, _ = district_series("tmin-1deg", TEMP_GRID, dists)
    T = {code: temp_indices(tmax[code], tmin[code]) for code, _, _ in dists}
    dt = assemble(T, K)
    two = [c for c in dt.columns if c.endswith("_c")]
    dt[two] = dt[two].round(2)
    write(NAMES["temp"], dt, ints=[c for c in dt.columns if c.startswith(("days_", "nights_", "heatwave", "severe", "warm"))])

    cells = pd.DataFrame([dict(district=K[K.census == c].district.iloc[0], census=c,
                               rain_cells=rcells[c], temp_cells=tcells[c]) for c, _, _ in dists])
    print(cells.sort_values("rain_cells").to_string(index=False))


if __name__ == "__main__":
    main()
