# IMD RSMC New Delhi: cyclone best tracks and climatology

Original files from India Meteorological Department's Regional Specialised Meteorological Centre for Tropical Cyclones over the North Indian Ocean. The cleaned data is in one folder per table:

- [`CLM_cyclone-best-tracks_1982-to-2026_IN_IMD/`](../../CLM_cyclone-best-tracks_1982-to-2026_IN_IMD/) (best tracks xlsx)
- [`CLM_severe-cyclone-frequency_1965-to-2025_IN_IMD/`](../../CLM_severe-cyclone-frequency_1965-to-2025_IN_IMD/) (`scs.xls`, all six sheets)
- [`CLM_cyclone-intensity-landfall_1990-to-2025_IN_IMD/`](../../CLM_cyclone-intensity-landfall_1990-to-2025_IN_IMD/) (`tcintensity.xls`, sheet TC DATA)
- [`CLM_cyclone-rainfall-damage_1990-to-2025_IN_IMD/`](../../CLM_cyclone-rainfall-damage_1990-to-2025_IN_IMD/) (`tcintensity.xls`, sheet TC RAINFALL)
- [`CLM_cyclone-crossings_1982-to-2025_STATES_BNY_DIST/`](../../CLM_cyclone-crossings_1982-to-2025_STATES_BNY_DIST/) (our calculation from the best tracks and 2011 district boundaries)

## Source

- **Link:** https://rsmcnewdelhi.imd.gov.in/report.php?internal_menu=MzM= (no login)
- **Downloaded:** 12 Nov 2026
- **`raw/`:** `imd-rsmc_best-tracks_1982-2026.xlsx`, `imd-rsmc_severe-cyclonic-storms-climatology.xls` (`scs.xls`), `imd-rsmc_tc-intensity-climatology.xls` (`tcintensity.xls`)
- **Scripts:** [`pipelines/imd-rsmc/`](../../pipelines/imd-rsmc/)
- Not taken: the yearly best-track PDF reports and the cyclone-track atlas PDF on the same page (same data as the xlsx, as maps and text).
