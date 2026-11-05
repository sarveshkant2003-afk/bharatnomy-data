# District boundaries, Census 2011 (DataMeet)

Original files used for:

- [`CLM_rainfall-indices_1951-to-2025_MH_BNY_DIST/`](../../CLM_rainfall-indices_1951-to-2025_MH_BNY_DIST/)
- [`CLM_rainfall-variability_1971-to-2020_MH_BNY_DIST/`](../../CLM_rainfall-variability_1971-to-2020_MH_BNY_DIST/)
- [`CLM_temperature-indices_1951-to-2024_MH_BNY_DIST/`](../../CLM_temperature-indices_1951-to-2024_MH_BNY_DIST/)

## Source

- **Data:** DataMeet community maps, `Districts/Census_2011/2011_Dist` shapefile: 641 districts of Census 2011 with state and district Census codes (`ST_CEN_CD`, `DT_CEN_CD`, `censuscode`)
- **Link:** https://github.com/datameet/maps/tree/5ea90379e67dece749b01448ca438161a3534b79/Districts/Census_2011 (fixed version of 22 May 2014)
- **Licence:** as stated by the repository (GitHub reports MIT)
- **Downloaded:** 5 Nov 2026

## Why a community map

Official boundary files (Survey of India, ISRO Bhuvan) need a login, which we do not have. This map is used **only to decide which grid cells belong to each district**; no values come from it. Its `censuscode` links each polygon to Census 2011 and, through [`_reference/geography.csv`](../../_reference/geography.csv), to today's LGD codes.

## Files in `raw/`

`datameet-maps_census2011-districts_2011.{shp,shx,dbf,prj}`: the shapefile (geographic coordinates, WGS 84), renamed.

## Notes

- Boundaries are those of 2011: districts created later (e.g. Palghar, 2014) are inside their parent (Thane).
- Community maps can differ slightly from official boundaries along borders; this matters little for 0.25- and 1-degree grids.
