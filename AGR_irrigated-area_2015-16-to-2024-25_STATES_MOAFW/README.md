# Irrigated area by state, 2015-16 to 2024-25

From the Ministry of Agriculture's annual land use publication. Areas in thousand hectares (`_000_ha`) unless the column ends in `_pct`.

## Source

- **Data:** Department of Agriculture & Farmers Welfare (MoA&FW), *Land Use Statistics at a Glance 2024-25*, Table 6
- **Link:** https://desagri.gov.in/document-report-category/land-use-statistics-at-a-glance/
- **Downloaded:** 19 Oct 2026
- **Original file:** [`_sources/moafw-lus/raw/`](../_sources/moafw-lus/raw/)

## Columns

`state_ut`, then `year` (agricultural year, July-June).

| Column | Meaning |
|---|---|
| `cropping_intensity_pct` | Gross cropped area as % of net sown area |
| `net_irrigated_area_000_ha` | Area irrigated at least once |
| `gross_irrigated_area_000_ha` | Irrigated area counting each season |
| `area_irrigated_more_than_once_000_ha` | Gross minus net irrigated area |
| `net_unirrigated_area_000_ha`, `gross_unirrigated_area_000_ha` | Sown area not irrigated |
| `gross_irrigated_to_gross_cropped_pct` | Gross irrigated as % of gross cropped area |
| `source_flag` | `provisional` = year printed with `(p)` |
| `source_marks` | Symbols printed next to a number, as `<column>:<symbol>`. `*` is not explained by the source; bracketed numbers are area included in the total without a crop-wise split |

## Notes

- Blank cells are blank in the publication; they are not zeros.
