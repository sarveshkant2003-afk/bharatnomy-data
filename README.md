# Bharatnomy Data Repository

Public datasets for Bharatnomy's research. One folder per table; each folder's `README.md` gives the source and explains every column.

## What's here

One folder per table, named by the [naming rules](#folder-names) below. Each folder holds the CSV (same name as the folder) and a `README.md` with its source and columns.

| Folder | What it holds | Source |
|---|---|---|
| [`AGR_area-under-crops_1950-51-to-2024-25_IN_MOAFW`](AGR_area-under-crops_1950-51-to-2024-25_IN_MOAFW/) | Area under crops, All India | Land Use Statistics at a Glance 2024-25 |
| [`AGR_area-under-crops_2015-16-to-2024-25_STATES_MOAFW`](AGR_area-under-crops_2015-16-to-2024-25_STATES_MOAFW/) | Area under crops by state | Land Use Statistics at a Glance 2024-25 |
| [`AGR_gross-irrigated-area-by-source_2015-16-to-2024-25_STATES_MOAFW`](AGR_gross-irrigated-area-by-source_2015-16-to-2024-25_STATES_MOAFW/) | Gross irrigated area by source, by state | Land Use Statistics at a Glance 2024-25 |
| [`AGR_irrigated-area_2015-16-to-2024-25_STATES_MOAFW`](AGR_irrigated-area_2015-16-to-2024-25_STATES_MOAFW/) | Net and gross irrigated area by state | Land Use Statistics at a Glance 2024-25 |
| [`AGR_irrigated-area-by-crop_1950-51-to-2024-25_IN_MOAFW`](AGR_irrigated-area-by-crop_1950-51-to-2024-25_IN_MOAFW/) | Irrigated area by crop, All India | Land Use Statistics at a Glance 2024-25 |
| [`AGR_irrigated-area-by-crop_2015-16-to-2024-25_STATES_MOAFW`](AGR_irrigated-area-by-crop_2015-16-to-2024-25_STATES_MOAFW/) | Irrigated area by crop, by state | Land Use Statistics at a Glance 2024-25 |
| [`AGR_land-use-classification_1950-51-to-2024-25_IN_MOAFW`](AGR_land-use-classification_1950-51-to-2024-25_IN_MOAFW/) | Land use classification, All India | Land Use Statistics at a Glance 2024-25 |
| [`AGR_land-use-classification_2015-16-to-2024-25_STATES_MOAFW`](AGR_land-use-classification_2015-16-to-2024-25_STATES_MOAFW/) | Land use classification by state | Land Use Statistics at a Glance 2024-25 |
| [`AGR_net-irrigated-area_2004-05-to-2020-21_STATES_RBI`](AGR_net-irrigated-area_2004-05-to-2020-21_STATES_RBI/) | Net irrigated area by state (older years) | RBI Handbook of Statistics on Indian States |
| [`AGR_net-irrigated-area-by-source_1950-51-to-2024-25_IN_MOAFW`](AGR_net-irrigated-area-by-source_1950-51-to-2024-25_IN_MOAFW/) | Net irrigated area by source, All India | Land Use Statistics at a Glance 2024-25 |
| [`AGR_net-irrigated-area-by-source_2015-16-to-2024-25_STATES_MOAFW`](AGR_net-irrigated-area-by-source_2015-16-to-2024-25_STATES_MOAFW/) | Net irrigated area by source, by state | Land Use Statistics at a Glance 2024-25 |
| [`AGR_net-sown-area_2004-05-to-2020-21_STATES_RBI`](AGR_net-sown-area_2004-05-to-2020-21_STATES_RBI/) | Net sown area by state (older years) | RBI Handbook of Statistics on Indian States |
| [`ENV_forest-cover_2023_STATES_FSI_DIST`](ENV_forest-cover_2023_STATES_FSI_DIST/) | Forest cover by district | India State of Forest Report 2023 |
| [`ENV_forest-tree-cover_2023_STATES_FSI`](ENV_forest-tree-cover_2023_STATES_FSI/) | Forest and tree cover by state | India State of Forest Report 2023 |
| [`IND_factories_2004-05-to-2023-24_STATES_RBI`](IND_factories_2004-05-to-2023-24_STATES_RBI/) | Number of factories by state | RBI Handbook of Statistics on Indian States |
| [`WAT_msw-generated-processed_2023-12_STATES_MOHUA`](WAT_msw-generated-processed_2023-12_STATES_MOHUA/) | Municipal solid waste generated and processed | MoHUA Swachhatam portal |

Original source files (PDFs, API downloads) are in [`_sources/`](_sources/), one folder per release.

## Find data by topic

| Topic | Where |
|---|---|
| Land use, net sown area, fallow | `AGR_land-use-classification_*`; older state years in `AGR_net-sown-area_*_RBI` |
| Irrigation | `AGR_*irrigated-area*`; older state years in `AGR_net-irrigated-area_*_RBI` |
| Crop area | `AGR_area-under-crops_*`, `AGR_irrigated-area-by-crop_*` |
| Factories, industry | `IND_*` |
| Forest cover | `ENV_forest-*` |
| Urban solid waste | `WAT_msw-*` |

## Folder names

```
CATEGORY_subject_PERIOD_GEOGRAPHY_SOURCE[_LEVEL]/CATEGORY_subject_PERIOD_GEOGRAPHY_SOURCE[_LEVEL].csv
```

Underscores separate the parts; hyphens join words within a part. Codes in capitals, subject in small letters, under 80 characters. Press `t` on the repository page to search names.

- **CATEGORY**: `AGR` Agriculture, `NAC` National and State Accounts, `PRC` Prices and Inflation, `IND` Industry and Mining, `LAB` Labour and Employment, `CON` Household Consumption, `POP` Population, `HLT` Health and Nutrition, `EDU` Education, `ENG` Energy and Power, `CLM` Climate and Weather, `ENV` Environment and Forests, `WAT` Water and Sanitation, `HOU` Housing, `TRN` Transport, `COM` Communication, `FIN` Banking and Finance, `PUB` Public Finance, `TRD` Trade, `TOU` Tourism, `SOC` Social Welfare, `GOV` Governance and Elections, `SDG` SDG and Indices
- **subject**: short description, e.g. `net-sown-area`
- **PERIOD**: a year (`2023`), a financial year (`FY2023-24`), a month (`2023-12`) or a range (`2015-to-2025`; for split years `2015-16-to-2024-25`)
- **GEOGRAPHY**: `IN` (All India), `STATES` (all states), a state code (`UP`), two or three codes joined (`UP-BR`), or `MULTI`
- **SOURCE**: the organisation the data is taken from, always spelled the same (see below). `BNY` = our own data
- **LEVEL** (optional): `DIST`, `SDT` (sub-district), `VIL` (village) or `CITY` for data below state level

Example: `AGR_area-under-crops_2015-16-to-2024-25_STATES_MOAFW`.

## Source codes

| Code | Meaning |
|---|---|
| `FSI` | Forest Survey of India |
| `MOAFW` | Ministry of Agriculture & Farmers' Welfare |
| `MOHUA` | Ministry of Housing & Urban Affairs |
| `RBI` | Reserve Bank of India (republished tables; the original agency is in each README) |

## Conventions

- CSV, UTF-8, plain numbers. The unit is in the column name (`_000_ha` = thousand hectares, `_sq_km`, `_pct`, `_tpd` = tonnes per day).
- One row per place per year. State names are spelled the same in every file, so files can be joined.
- `All India` and `State total` rows are published totals; leave them out before adding up.
- `source_flag` says why a cell is blank or its status (`provisional`, `estimated`, ...). `source_marks` keeps other symbols printed next to a number.
- Original source files are in `_sources/<release>/raw/`.
