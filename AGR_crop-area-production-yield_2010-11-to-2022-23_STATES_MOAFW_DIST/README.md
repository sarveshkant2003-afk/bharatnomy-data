# Crop area, production and yield by district, 2010-11 to 2022-23

Area sown, production and yield of every crop and season reported for every district of India, by agricultural year. This is one of two files (split by year range to keep each under 25 MB); the other is [`AGR_crop-area-production-yield_1997-98-to-2009-10_STATES_MOAFW_DIST`](../AGR_crop-area-production-yield_1997-98-to-2009-10_STATES_MOAFW_DIST/).

## Source

- **Data:** Directorate of Economics & Statistics (DES), Ministry of Agriculture & Farmers Welfare, Crop Production Statistics (Area, Production and Yield, APY), district level
- **Table taken from:** "Crops APY report" on the DES data portal: all states one at a time, all districts, all crops, all seasons, 1997-98 to 2022-23, format "Horizontal Crop and Vertical Year"
- **Link:** https://data.desagri.gov.in/website/crops-apy-report-web
- **Downloaded:** 12 Nov 2026 (report pages not committed, about 150 MB; `pipelines/moafw-apy/fetch_apy.py` downloads them, see [`_sources/moafw-apy/`](../_sources/moafw-apy/))
- **Script:** [`pipelines/moafw-apy/build_apy.py`](../pipelines/moafw-apy/build_apy.py)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (`Dadra & Nagar Haveli`, `Daman & Diu` as reported for the years before their merger) |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv) |
| `district` | District as spelled by DES |
| `lgd_district_code` | District code in the LGD; blank where the DES name could not be matched (50 of 748 names, e.g. old or differently spelled districts) |
| `year` | Agricultural year (July-June), e.g. `2022-23` |
| `crop` | Crop as named by DES (includes DES totals such as `Total foodgrain`, `Pulses total`, `Oilseeds total` where reported) |
| `season` | `Kharif`, `Rabi`, `Autumn`, `Winter`, `Summer`, `Whole Year` |
| `area_ha` | Area, hectares |
| `production` | Production, in `production_unit` |
| `yield` | Yield, in `yield_unit` (production / area) |
| `production_unit` | `Tonnes`; `Bales` for cotton (lint), jute and mesta; `Nuts` for coconut (as labelled by DES) |
| `yield_unit` | `Tonne/Hectare`, `Bales/Hectare` or `Nuts/Hectare` |

## Notes

- One row per district, year, crop and season that has at least one value. Blank cells are blank in the report (DES gives no reason). Crop-season pairs not reported for a district do not appear.
- Values are as printed by DES (thousands separators removed, decimals kept). Some values look odd but are DES's own, e.g. Ahilyanagar sugarcane 1997-98: 45,900 ha, 38,940 tonnes, yield 0.85; checked against single-crop queries of the same portal.
- No state or India totals: the report gives districts only.
- District boundaries and names change over time (new districts appear in later years); match across years with care.
- Checks (12 Nov 2026): 224,209 rows in this file (407,903 in both); no duplicate district-year-crop-season keys; all state names valid; yield equals production / area within rounding in all but 11 of 402,928 rows that have all three (tiny areas such as 0.01 ha); no negative values.
