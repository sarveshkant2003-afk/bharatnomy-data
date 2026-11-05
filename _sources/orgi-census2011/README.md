# Census of India 2011 (ORGI)

Original files for this release. The cleaned data is in one folder per table:

- [`POP_census-pca_2011_STATES_ORGI_DIST/`](../../POP_census-pca_2011_STATES_ORGI_DIST/)
- [`POP_single-year-age_2011_MH_ORGI_DIST/`](../../POP_single-year-age_2011_MH_ORGI_DIST/)
- [`HOU_slum-population_2011_STATES_ORGI_CITY/`](../../HOU_slum-population_2011_STATES_ORGI_CITY/)
- [`HOU_household-amenities-hh14_2011_MH_ORGI_SDT/`](../../HOU_household-amenities-hh14_2011_MH_ORGI_SDT/): `raw/hl14-mh/`, table HH-14 for the 35 districts of Maharashtra (catalog 9795-9829, downloaded 5 Nov 2026, 51 MB; fetch and build scripts in [`pipelines/orgi-census2011/`](../../pipelines/orgi-census2011/)). Only district and sub-district rows are converted; town, ward and village rows are not yet
- [`_reference/geography.csv`](../../_reference/geography.csv): `orgi-census2011_basic-population-subdistrict-town_2011.xlsx` (catalog 42559, Basic Population Figures of India/State/District/Sub-District/Town, downloaded 5 Nov 2026) gives the Census 2011 code and name of every state, district and sub-district

## Source

- **Link:** https://censusindia.gov.in/nada/index.php/catalog (catalog 6191 PCA district level, 6190 PCA slum town level, 1457 C-13 Maharashtra)
- **Downloaded:** 28 Oct 2026
- **`raw/`:** the three Excel files as downloaded, renamed. The rest of Census 2011 (houselisting amenities, town PCA, other states' C-13, District Census Handbooks) is on the same portal and not taken yet
