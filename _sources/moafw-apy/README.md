# DES crop Area, Production and Yield (APY), district level

Original report pages for:

- [`AGR_crop-area-production-yield_1997-98-to-2009-10_STATES_MOAFW_DIST/`](../../AGR_crop-area-production-yield_1997-98-to-2009-10_STATES_MOAFW_DIST/)
- [`AGR_crop-area-production-yield_2010-11-to-2022-23_STATES_MOAFW_DIST/`](../../AGR_crop-area-production-yield_2010-11-to-2022-23_STATES_MOAFW_DIST/)

- **Link:** https://data.desagri.gov.in/website/crops-apy-report-web (no login)
- **Downloaded:** 12 Nov 2026
- **`raw/`:** `moafw-apy_states.tsv` (state codes used by the portal). The 38 report pages (`moafw-apy_district-<code>_1997-to-2022.html`, about 150 MB) are not committed: run `python3 pipelines/moafw-apy/fetch_apy.py` from the repo root to download them (a few minutes).
- **Scripts:** [`pipelines/moafw-apy/`](../../pipelines/moafw-apy/)
