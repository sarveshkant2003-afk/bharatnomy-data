# Gross irrigated area by source, by state, 2015-16 to 2024-25

From the Ministry of Agriculture's annual land use publication. Areas in thousand hectares (`_000_ha`) unless the column ends in `_pct`.

## Source

- **Data:** Department of Agriculture & Farmers Welfare (MoA&FW), *Land Use Statistics at a Glance 2024-25*, Table 9
- **Link:** https://desagri.gov.in/document-report-category/land-use-statistics-at-a-glance/
- **Downloaded:** 19 Oct 2026
- **Original file:** [`_sources/moafw-lus/raw/`](../_sources/moafw-lus/raw/)

## Columns

`state_ut`, then `year` (agricultural year, July-June).

| Column | Meaning |
|---|---|
| `canals_government_000_ha`, `canals_private_000_ha`, `canals_total_000_ha` | Irrigated by canals |
| `tanks_000_ha`, `tube_wells_000_ha`, `other_wells_000_ha`, `other_sources_000_ha` | Irrigated by each other source |
| `gross_irrigated_area_000_ha` | Irrigated area counting each season |
| `source_flag` | `provisional` = year printed with `(p)` |

## Notes

- Blank cells are blank in the publication; they are not zeros.
- No All India row in the source.
