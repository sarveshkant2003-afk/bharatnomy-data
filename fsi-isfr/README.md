# Forest and tree cover by state, ISFR 2023

Area under forest cover and tree cover in every state/UT, from the India State of Forest Report 2023
(the Forest Survey of India's satellite and field based assessment, published every two years).

## Source

- **Data:** Forest Survey of India (FSI), MoEFCC, *India State of Forest Report 2023*
- **Table taken from:** PIB release "Parliament Question: Steps To Bring More Area Under Green Cover" (Rajya Sabha Unstarred Q. 367), 6 Feb 2025
- **Link:** https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2100254
- **Full report:** https://fsi.nic.in/forest-report-2023
- **Downloaded:** 19 Oct 2026

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `geographical_area_sq_km` | Geographical area, sq km |
| `forest_cover_sq_km` | Forest cover, sq km: all land of 1 ha or more with tree canopy density of at least 10%, whatever its ownership or legal status (includes orchards, bamboo and palm) |
| `tree_cover_sq_km` | Tree cover, sq km: tree patches under 1 ha outside forest areas, including scattered trees in villages and cities |
| `forest_and_tree_cover_sq_km` | Forest cover + tree cover, sq km |

## Notes

- Ladakh's geographical area is blank in the source; the single figure of 2,22,236 sq km sits on the Jammu & Kashmir row.
- Leave out the `All India` row before adding states up.
