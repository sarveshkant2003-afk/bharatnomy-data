# IMD Pune daily gridded temperature and rainfall

Original files used for:

- [`CLM_heat-indicators-nagpur_1951-to-2025_MH_BNY_DIST/`](../../CLM_heat-indicators-nagpur_1951-to-2025_MH_BNY_DIST/)

## Source

- **Data:** India Meteorological Department (IMD), Pune. Daily maximum and minimum temperature on a 1.0 x 1.0 degree grid (Srivastava et al. 2009), 1951-2024; daily rainfall on a 0.25 x 0.25 degree grid (Pai et al. 2014), 1951-2025
- **Link:** https://imdpune.gov.in/lrfindex.php (Gridded data: `Max_1_Bin.html`, `Min_1_Bin.html`, `Rainfall_25_Bin.html`)
- **Downloaded:** 28 Oct 2026
- **`raw/`:** not committed (223 binary files, 1.9 GB). Each year is a POST to `https://imdpune.gov.in/cmpg/Griddata/{maxtemp,mintemp,rainfall}.php`
