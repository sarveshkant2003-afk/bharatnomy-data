# Land use classification, All India, 1950-51 to 2024-25

From the Ministry of Agriculture's annual land use publication. Areas in thousand hectares (`_000_ha`) unless the column ends in `_pct`.

## Source

- **Data:** Department of Agriculture & Farmers Welfare (MoA&FW), *Land Use Statistics at a Glance 2024-25*, Table 1
- **Link:** https://desagri.gov.in/document-report-category/land-use-statistics-at-a-glance/
- **Downloaded:** 19 Oct 2026
- **Original file:** [`_sources/moafw-lus/raw/`](../_sources/moafw-lus/raw/)

## Columns

`state_ut`, then `year` (agricultural year, July-June).

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
| `source_flag` | `provisional` = year printed with `(p)` |
| `source_marks` | Symbols printed next to a number, as `<column>:<symbol>`. `*` is not explained by the source; bracketed numbers are area included in the total without a crop-wise split |

## Notes

- Blank cells are blank in the publication; they are not zeros.
