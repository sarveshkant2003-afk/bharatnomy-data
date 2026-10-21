# Area under crops, All India, 1950-51 to 2024-25

From the Ministry of Agriculture's annual land use publication. Areas in thousand hectares (`_000_ha`) unless the column ends in `_pct`.

## Source

- **Data:** Department of Agriculture & Farmers Welfare (MoA&FW), *Land Use Statistics at a Glance 2024-25*, Table 4
- **Link:** https://desagri.gov.in/document-report-category/land-use-statistics-at-a-glance/
- **Downloaded:** 19 Oct 2026
- **Original file:** [`_sources/moafw-lus/raw/`](../_sources/moafw-lus/raw/)

## Columns

`state_ut`, then `year` (agricultural year, July-June).

One column per crop, e.g. `rice_000_ha`. `total_*` columns are the publication's subtotals.

| Column | Meaning |
|---|---|
| `source_flag` | `provisional` = year printed with `(p)` |
| `source_marks` | Symbols printed next to a number, as `<column>:<symbol>`. `*` is not explained by the source; bracketed numbers are area included in the total without a crop-wise split |

## Notes

- Blank cells are blank in the publication; they are not zeros.
