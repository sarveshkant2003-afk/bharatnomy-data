# Land Use Statistics at a Glance 2024-25 (all ten tables)

Every table in the Ministry of Agriculture's yearly land-use book: how each state's land is used (nine-fold classification),
how much is irrigated and from which source, and the area under each crop. National series go back to 1950-51;
state series cover 2015-16 to 2024-25. All areas are in thousand hectares.

## Source

- **Data:** Department of Agriculture & Farmers Welfare (MoA&FW), Economics, Statistics & Evaluation Division, *Land Use Statistics at a Glance 2024-25* (uploaded June 2026)
- **Link:** https://desagri.gov.in/document-report-category/land-use-statistics-at-a-glance/ (file: https://desagri.gov.in/wp-content/uploads/2026/06/LUS-Publication-2024-25.pdf)
- **Original:** [`raw/moafw-lus_land-use-statistics-at-a-glance_2024-25.pdf`](raw/) (287 pages; tables on pages 105-274 of the printed numbering)
- **Downloaded:** 19 Oct 2026
- **Code:** [`scripts/lus_2024-25.py`](scripts/) reads the PDF and writes all ten CSVs; [`scripts/check_lus.py`](scripts/) runs the checks.

## Files

| File | Table | Rows |
|---|---|---|
| `moafw-lus_land-use-classification_india_1950-51-to-2024-25.csv` | 1. Land use classification, All India | 75 years |
| `moafw-lus_net-irrigated-area-by-source_india_1950-51-to-2024-25.csv` | 2. Net irrigated area by source and gross irrigated area, All India | 75 years |
| `moafw-lus_irrigated-area-by-crop_india_1950-51-to-2024-25.csv` | 3. Irrigated area under crops, All India | 75 years |
| `moafw-lus_area-under-crops_india_1950-51-to-2024-25.csv` | 4. Area under crops, All India | 75 years |
| `moafw-lus_land-use-classification_state_2015-16-to-2024-25.csv` | 5. Land use classification by state | 370 |
| `moafw-lus_irrigated-area_state_2015-16-to-2024-25.csv` | 6. Irrigated area by state | 370 |
| `moafw-lus_net-irrigated-area-by-source_state_2015-16-to-2024-25.csv` | 7. Net irrigated area by source, by state | 370 |
| `moafw-lus_irrigated-area-by-crop_state_2015-16-to-2024-25.csv` | 8. Irrigated area by crop, by state | 370 |
| `moafw-lus_gross-irrigated-area-by-source_state_2015-16-to-2024-25.csv` | 9. Gross irrigated area by source, by state | 275 |
| `moafw-lus_area-under-crops_state_2015-16-to-2024-25.csv` | 10. Area under crops by state (83 crops and totals) | 370 |

## Columns

Every file starts with `state_ut` (`All India` in tables 1-4) and `year` (agricultural year, July-June, e.g. `2024-25`).
All other numbers are thousand hectares (`_000_ha`) unless the name ends in `_pct`.

**Land use (tables 1 and 5)**

| Column | Meaning |
|---|---|
| `geographical_area_000_ha` | Total geographical area |
| `reporting_area_000_ha` | Area for which land-use returns exist (sum of the five main classes below) |
| `forests_000_ha` | Land classed as forest by law or administered as forest |
| `area_non_agricultural_uses_000_ha`, `barren_unculturable_land_000_ha`, `not_available_for_cultivation_total_000_ha` | Land not available for cultivation, and its two parts |
| `permanent_pastures_grazing_land_000_ha`, `misc_tree_crops_groves_000_ha`, `culturable_waste_land_000_ha`, `other_uncultivated_land_total_000_ha` | Other uncultivated land excluding fallow, and its three parts |
| `fallow_other_than_current_000_ha`, `current_fallows_000_ha`, `fallow_land_total_000_ha` | Fallow land (out of cultivation 1-5 years / this year) and total |
| `net_area_sown_000_ha` | Area sown at least once in the year |
| `gross_cropped_area_000_ha`, `area_sown_more_than_once_000_ha` | Total cropped area counting each sowing; gross minus net |
| `agricultural_land_000_ha` | Culturable land: tree crops + culturable waste + fallow + net sown |
| `cultivated_land_000_ha` | Current fallows + net sown |
| `cropping_intensity_pct` (table 1) | Gross cropped area as % of net sown area (above 100 by design) |
| `uncultivable_land_000_ha`, `uncultivated_land_000_ha` (table 5) | Reporting area minus agricultural land; minus cultivated land |

**Irrigation (tables 2, 6, 7, 9)**

| Column | Meaning |
|---|---|
| `canals_government_000_ha`, `canals_private_000_ha`, `canals_total_000_ha` | Area irrigated by canals |
| `tanks_000_ha`, `tube_wells_000_ha`, `other_wells_000_ha`, `other_sources_000_ha` | Area irrigated by each other source |
| `net_irrigated_area_000_ha` | Area irrigated at least once (tables 2, 6, 7) |
| `gross_irrigated_area_000_ha` | Irrigated area counting each crop season (tables 2, 6; table 9 splits it by source) |
| `area_irrigated_more_than_once_000_ha` | Gross minus net irrigated area |
| `net_unirrigated_area_000_ha`, `gross_unirrigated_area_000_ha` (table 6) | Sown area that is not irrigated |
| `gross_irrigated_to_gross_cropped_pct` | Gross irrigated area as % of gross cropped area |
| `cropping_intensity_pct` (table 6) | Gross cropped area as % of net sown area |

**Crops (tables 3, 4, 8, 10)**: one column per crop or crop group, named after it, e.g. `rice_000_ha`, `tur_arhar_000_ha`,
`rapeseed_mustard_000_ha`. Tables 3 and 8 give the *irrigated* area under each crop; tables 4 and 10 the *total* area.
Columns starting with `total_` are the publication's own subtotals (cereals, pulses, foodgrains, oilseeds, fibres, food
crops, non-food crops, all crops). `other_*` columns are the publication's "Others" within a group. Table 10 also has
`total_area_sown_000_ha`, `area_sown_more_than_once_000_ha` and `net_area_sown_000_ha`; `gross_fodder_crops_000_ha`
includes guar seed and oats.

**Markers**

| Column | Meaning |
|---|---|
| `source_flag` | `provisional` where the year is printed with `(p)` (all 2024-25 figures; 2021-22 for Dadra & Nagar Haveli and Daman & Diu) |
| `source_marks` | Symbols printed next to a number, kept as `<column>:<symbol>`, separated by `; `. See notes. |

## Notes

- **Blank cells are blank in the publication.** It leaves a cell empty where a state has no area under that item or did not report it; it does not say which. Blanks are not zeros.
- **Asterisks.** Many numbers, years and state names carry `*`, `**` or `***` (kept in `source_marks`, e.g. `forests_000_ha:*`, `year:***`, `state_ut:*`). The publication does not explain them. Its notes (pp. 59-61) say Manipur, Maharashtra and West Bengal sent partial data, that missing items were estimated or repeated from the previous year, and that forest area for Manipur and Meghalaya was taken from the Forest Survey of India; the asterisks probably mark these, but that is not confirmed. RBI's Handbook, which republishes these figures, footnotes the same `*` as "from the latest Agriculture Census or estimated".
- **Bracketed numbers (tables 3 and 4).** Kept as e.g. `total_pulses_000_ha:(8)`. The publication: "Figures in parenthesis give area in thousand hectares for which crop-wise details are not available but has been included in Total". This is why some printed totals are larger than the sum of their crops.
- `(a)` in table 2 (tube wells, early years): "Included under Other Wells as separate figures were not collected". `N.A.S.` in table 3: not available separately. One table 10 cell is printed as a lone `.`; it is kept blank with the mark `.`.
- **A page is missing from the source.** Printed page 137 repeats page 130, so table 5 columns 12-21 (fallow land to uncultivated land, including net area sown) are not published for Goa 2024-25, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka and Kerala. Those 61 rows carry `columns_12_to_21:page_missing_in_publication`. Net area sown for these states is still available in table 10 (`net_area_sown_000_ha`).
- Table 9 has no All India row ("not compiled due to non-availability of data from all the States/U.Ts"). West Bengal and some UTs appear only for 2023-24 and 2024-25.
- `Dadra & Nagar Haveli` and `Daman & Diu` appear for 2015-16 to 2018-19; the merged UT from 2019-20.
- **Check results (19 Oct 2026):** no duplicate keys, all state names valid, all numbers parse, none negative, percentages within 0-100. Printed subtotals match their parts within 1 (rounding) in almost every row; the exceptions are bracketed-area rows (above) and a few source inconsistencies, e.g. irrigated non-food crops 2023-24 (25541 printed vs 24273 from its parts), Goa total food crops 2020-21 (117 vs 81). State sums match All India within 0.5% except a handful of small crops. In table 5, 68 rows show reporting area larger than geographical area (e.g. Chhattisgarh, Rajasthan); this is as published.
- Older state-level years (before 2015-16) are not in this edition. The RBI Handbook series in [`../rbi-hsis/`](../rbi-hsis/) has net sown and net irrigated area by state from 2004-05.
