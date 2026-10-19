# Land Use Statistics at a Glance 2024-25

Land use, irrigation and crop area from the Ministry of Agriculture. National series from 1950-51; state series 2015-16 to 2024-25. All areas in thousand hectares.

## Source

- **Data:** Department of Agriculture & Farmers Welfare (MoA&FW), *Land Use Statistics at a Glance 2024-25*
- **Link:** https://desagri.gov.in/document-report-category/land-use-statistics-at-a-glance/
- **Downloaded:** 19 Oct 2026

## Files

| File | Table |
|---|---|
| `moafw-lus_land-use-classification_india_1950-51-to-2024-25.csv` | 1. Land use classification, All India |
| `moafw-lus_net-irrigated-area-by-source_india_1950-51-to-2024-25.csv` | 2. Net irrigated area by source, All India |
| `moafw-lus_irrigated-area-by-crop_india_1950-51-to-2024-25.csv` | 3. Irrigated area under crops, All India |
| `moafw-lus_area-under-crops_india_1950-51-to-2024-25.csv` | 4. Area under crops, All India |
| `moafw-lus_land-use-classification_state_2015-16-to-2024-25.csv` | 5. Land use classification by state |
| `moafw-lus_irrigated-area_state_2015-16-to-2024-25.csv` | 6. Irrigated area by state |
| `moafw-lus_net-irrigated-area-by-source_state_2015-16-to-2024-25.csv` | 7. Net irrigated area by source, by state |
| `moafw-lus_irrigated-area-by-crop_state_2015-16-to-2024-25.csv` | 8. Irrigated area by crop, by state |
| `moafw-lus_gross-irrigated-area-by-source_state_2015-16-to-2024-25.csv` | 9. Gross irrigated area by source, by state |
| `moafw-lus_area-under-crops_state_2015-16-to-2024-25.csv` | 10. Area under crops by state |

## Columns

Every file starts with `state_ut` and `year` (agricultural year, July-June). Numbers are thousand hectares (`_000_ha`) unless the name ends in `_pct`.

**Land use (tables 1, 5)**

| Column | Meaning |
|---|---|
| `geographical_area_000_ha` | Total geographical area |
| `reporting_area_000_ha` | Area with land-use records |
| `forests_000_ha` | Land classed as forest |
| `area_non_agricultural_uses_000_ha`, `barren_unculturable_land_000_ha`, `not_available_for_cultivation_total_000_ha` | Land not available for cultivation, and its parts |
| `permanent_pastures_grazing_land_000_ha`, `misc_tree_crops_groves_000_ha`, `culturable_waste_land_000_ha`, `other_uncultivated_land_total_000_ha` | Other uncultivated land, and its parts |
| `fallow_other_than_current_000_ha`, `current_fallows_000_ha`, `fallow_land_total_000_ha` | Fallow land |
| `net_area_sown_000_ha` | Area sown at least once in the year |
| `gross_cropped_area_000_ha`, `area_sown_more_than_once_000_ha` | Cropped area counting each sowing; gross minus net |
| `agricultural_land_000_ha`, `cultivated_land_000_ha` | Culturable land; current fallows + net sown |
| `cropping_intensity_pct` | Gross cropped area as % of net sown area |
| `uncultivable_land_000_ha`, `uncultivated_land_000_ha` | Reporting area minus agricultural / cultivated land |

**Irrigation (tables 2, 6, 7, 9)**

| Column | Meaning |
|---|---|
| `canals_government_000_ha`, `canals_private_000_ha`, `canals_total_000_ha` | Irrigated by canals |
| `tanks_000_ha`, `tube_wells_000_ha`, `other_wells_000_ha`, `other_sources_000_ha` | Irrigated by each other source |
| `net_irrigated_area_000_ha` | Area irrigated at least once |
| `gross_irrigated_area_000_ha` | Irrigated area counting each season |
| `area_irrigated_more_than_once_000_ha` | Gross minus net irrigated area |
| `net_unirrigated_area_000_ha`, `gross_unirrigated_area_000_ha` | Sown area not irrigated |
| `gross_irrigated_to_gross_cropped_pct` | Gross irrigated as % of gross cropped area |

**Crops (tables 3, 4, 8, 10):** one column per crop, e.g. `rice_000_ha`. Tables 3 and 8 give irrigated area; tables 4 and 10 total area. `total_*` columns are the publication's subtotals.

**Markers**

| Column | Meaning |
|---|---|
| `source_flag` | `provisional` = year printed with `(p)` |
| `source_marks` | Symbols printed next to a number, as `<column>:<symbol>`. `*` is not explained by the source; bracketed numbers are area included in the total without a crop-wise split |

## Notes

- Blank cells are blank in the publication; they are not zeros.
- Table 5 has no data in columns 12-21 for Goa 2024-25, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka and Kerala (a page is missing from the source); these rows are marked `columns_12_to_21:page_missing_in_publication`.
- Table 9 has no All India row.
