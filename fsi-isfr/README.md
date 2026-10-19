# India State of Forest Report 2023 (Forest Survey of India)

Forest cover from FSI's satellite-based assessment, published every two years. Forest cover is all land of 1 ha or more
with tree canopy density of at least 10%, whatever its ownership or legal status (it includes orchards, bamboo and palm).

## Source

- **Data:** Forest Survey of India (FSI), MoEFCC, *India State of Forest Report 2023*, Volumes I and II
- **Link:** https://fsi.nic.in/forest-report-2023
- **Originals:** [`raw/`](raw/) holds both volumes (Vol I: national and state tables; Vol II: one chapter per state/UT)
- **Downloaded:** 19 Oct 2026

## fsi-isfr_forest-cover_district_2023.csv

Forest cover by canopy density in every district, from the "District-wise Forest Cover" table (Table 10.x.3) of each
state chapter in Volume II. 750 districts in 36 states/UTs, plus a `State total` row per state.
Code: [`scripts/isfr_2023_district.py`](scripts/); checks: [`scripts/check_isfr_district.py`](scripts/).

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory |
| `district` | District as spelled in the report. `State total` = the state's published total |
| `geographical_area_sq_km` | District area calculated by FSI from Survey of India boundaries, sq km |
| `very_dense_forest_sq_km` | Canopy density 70% and above, sq km |
| `moderately_dense_forest_sq_km` | Canopy density 40% to under 70%, sq km |
| `open_forest_sq_km` | Canopy density 10% to under 40%, sq km |
| `forest_cover_total_sq_km` | Very dense + moderately dense + open forest, sq km |
| `forest_cover_pct_of_area` | Forest cover as % of the district's geographical area |
| `change_since_2021_sq_km` | Change in forest cover compared with the 2021 assessment (re-run on the 2023 raster), sq km. Can be negative |
| `scrub_sq_km` | Degraded land with canopy density under 10%, sq km (not counted as forest cover) |
| `source_marks` | `district:H` = hill district (printed as a superscript H after the name); `district:**` = marked `**` in the report, which gives no reason |

Notes:

- Checks (19 Oct 2026): no duplicates, nothing negative except change, very dense + moderately dense + open = total in every row, the % matches total / area in every row, and districts add up to the State total in every state (Uttarakhand's area is off by 0.2 sq km in the source). Five random rows match the PDF.
- Geographical area is printed with decimals for some states and as whole numbers for others; kept as printed.
- Some districts have two names in the report, e.g. `Amroha/ Jyotiba Phule Nagar`; kept as printed.
- The rest of the report (forest cover inside/outside recorded forest, forest types, fire, carbon stock, tree cover, mangroves, growing stock) is still only in the PDFs in `raw/`.

## fsi-isfr_forest-tree-cover_state_2023.csv

Forest cover and tree cover by state, taken from a parliamentary answer that republishes ISFR 2023.

- **Table taken from:** PIB release "Parliament Question: Steps To Bring More Area Under Green Cover" (Rajya Sabha Unstarred Q. 367), 6 Feb 2025
- **Link:** https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2100254

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `geographical_area_sq_km` | Geographical area, sq km |
| `forest_cover_sq_km` | Forest cover, sq km |
| `tree_cover_sq_km` | Tree cover, sq km: tree patches under 1 ha outside forest areas, including scattered trees in villages and cities |
| `forest_and_tree_cover_sq_km` | Forest cover + tree cover, sq km |

Notes:

- Ladakh's geographical area is blank in the source; the single figure of 2,22,236 sq km sits on the Jammu & Kashmir row.
- Leave out the `All India` row before adding states up.
