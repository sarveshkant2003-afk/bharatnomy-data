# Land use and irrigation by district, Maharashtra, 1998-99 to 2024-25

The nine-fold land use classification (forests, non-agricultural uses, barren land, pastures, tree crops, culturable waste, fallows, net sown area), cropped area, and net and gross irrigated area by source (canal, tank, tubewell, other wells, other sources) for each district of Maharashtra, in hectares.

## Source

- **Data:** Directorate of Economics & Statistics (DES), Ministry of Agriculture & Farmers' Welfare (MoA&FW), Land Use Statistics Information System
- **Table taken from:** LUS portal "Grand Query Report", district data, Maharashtra, all land-use and source-of-irrigation items, unit hectare, queried one year at a time
- **Link:** https://data.desagri.gov.in/weblus/lus-grand-query-report
- **Downloaded:** 28 Oct 2026
- **Original files:** [`_sources/moafw-lus-district/raw/`](../_sources/moafw-lus-district/raw/) (the report HTML for each year)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | Maharashtra |
| `district` | District as spelled on the portal (current names, e.g. Ahilyanagar, even for old years). `State total` = the portal's "Total of Maharashtra" row. `Maharashtra_Total` = a second total row the portal prints for 2021-22 to 2023-24 with only cropped-area and irrigation figures |
| `year` | Agricultural year (July-June) |
| `reporting_area_ha` | Area for which land use is reported, ha |
| `forests_ha` ... `fallow_land_total_ha` | Classification of reporting area, ha (same items as `AGR_land-use-classification_*`) |
| `net_area_sown_ha`, `gross_cropped_area_ha`, `area_sown_more_than_once_ha` | ha |
| `net_irrigated_<source>_ha` | Net irrigated area by source: `canal_government`, `canal_private`, `canal_total`, `tank`, `tubewell`, `other_well`, `well_total`, `other_sources`, `area_total` |
| `gross_irrigated_<source>_ha` | Gross irrigated area, same sources |

## Notes

- The portal has district data for Maharashtra only for 1998-99 to 2002-03 and 2020-21 to 2024-25; other years return empty tables.
- Since 2020-21 most districts show `-` for cropped and irrigated area (district irrigation is not reported), so irrigation is only available for 1998-99 to 2002-03. Cells printed as `-` or left empty are blank here; the portal does not say why.
- Agricultural vs non-agricultural land: agricultural land = net sown + current fallows + other fallows + culturable waste + tree crops (the LUS definition of agricultural or culturable land, as in `agricultural_land_000_ha` of `AGR_land-use-classification_*`); non-agricultural uses are in `area_non_agricultural_uses_ha`. Irrigated vs rain-fed: rain-fed = `net_area_sown_ha` - `net_irrigated_area_total_ha`.
