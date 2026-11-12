# NASA POWER daily data, Maharashtra

Used for [`CLM_wind-humidity_1981-to-2025_MH_BNY_DIST/`](../../CLM_wind-humidity_1981-to-2025_MH_BNY_DIST/) (daily data) and [`CLM_aerosol-soil-evaporation-boundary-layer_1981-to-2025_MH_BNY_DIST/`](../../CLM_aerosol-soil-evaporation-boundary-layer_1981-to-2025_MH_BNY_DIST/) (monthly data).

- **Link:** https://power.larc.nasa.gov/api/temporal/daily/point (no login; parameters WS10M, WS10M_MAX, WS10M_MIN, WD10M, WS50M, WS50M_MAX, RH2M, T2M, T2M_MAX, T2MWET; 1981-2025)
- **Downloaded:** 5 Nov 2026
- **`raw/`:** not committed (118 gzipped JSON files, one per MERRA-2 cell over Maharashtra). Run `python3 pipelines/nasa-power/fetch_power.py` from the repo root to download them (about an hour).
- **`raw/monthly/`:** not committed (118 gzipped JSON files, monthly AOD_55, GWETTOP, GWETROOT, GWETPROF, EVLAND, PBLTOP, PS, T2M, WS10M, 1981-2025; downloaded 12 Nov 2026). Run `python3 pipelines/nasa-power/fetch_power_monthly.py` from the repo root (about 5 minutes).
