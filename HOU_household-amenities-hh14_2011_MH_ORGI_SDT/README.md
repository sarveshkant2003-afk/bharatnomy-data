# Household amenities and assets by district and sub-district, Maharashtra, 2011

Share of households by condition and material of the house (roof, wall, floor), rooms, size, ownership, drinking water source and location, lighting, latrine, bathing, drainage, cooking fuel, kitchen, banking and assets, for every district and sub-district (tehsil) of Maharashtra, total / rural / urban. All 135 indicators of Census 2011 table HH-14.

## Source

- **Data:** Office of the Registrar General & Census Commissioner, India (ORGI), Census of India 2011, Houselisting and Housing Census, table HH-14 "Percentage of households to total households by amenities and assets" (one file per district, `HLPCA-27<district code>-2011_H14_census.xlsx`)
- **Link:** https://censusindia.gov.in/nada/index.php/catalog (catalog ids 9795-9829; e.g. Nagpur: https://censusindia.gov.in/nada/index.php/catalog/9803)
- **Downloaded:** 5 Nov 2026
- **Original files:** [`_sources/orgi-census2011/raw/hl14-mh/`](../_sources/orgi-census2011/raw/hl14-mh/)
- **Scripts:** [`pipelines/orgi-census2011/fetch_hl14_mh.sh`](../pipelines/orgi-census2011/fetch_hl14_mh.sh), [`build_hl14_mh.py`](../pipelines/orgi-census2011/build_hl14_mh.py)

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code` | Maharashtra, 27 |
| `district`, `lgd_district_code` | District by its current name and LGD code (from [`_reference/geography.csv`](../_reference/geography.csv)) |
| `district_census_code`, `district_census_name` | Census 2011 district code and name |
| `area_level` | `district` or `sub-district` |
| `subdistrict`, `subdistrict_census_code` | Sub-district (tehsil) name and Census 2011 code; blank on district rows |
| `residence` | `Total`, `Rural` or `Urban` |
| `house_condition_<use>_<condition>_pct` | Households by condition of the census house (`good`, `livable`, `dilapidated`, `total`), for all houses (`total`), houses used only as residence (`residence`) and residence-cum-other use, % of households |
| `roof_*_pct`, `wall_*_pct`, `floor_*_pct` | Households by predominant material of roof / wall / floor, % (e.g. `roof_g_i_metal_asbestos_sheets_pct`, `roof_grass_thatch_bamboo_wood_mud_etc_pct`, `roof_concrete_pct`) |
| `dwelling_rooms_*_pct`, `household_size_*_pct`, `married_couples_*_pct` | Households by number of dwelling rooms, persons, married couples, % |
| `ownership_owned_pct`, `ownership_rented_pct`, `ownership_any_others_pct` | Ownership of the house, % |
| `drinking_water_source_*_pct` | Main source of drinking water (treated / untreated tap water, wells, handpump, tubewell, spring, river, tank, other), % |
| `drinking_water_location_within_premises_pct`, `_near_premises_pct`, `_away_pct` | Location of the drinking water source, % |
| `lighting_*_pct` | Main source of lighting (electricity, kerosene, solar, other oil, any other, none), % |
| `latrine_within_premises_total_pct` and `latrine_flush_*`, `latrine_pit_*`, `latrine_night_soil_open_drain_pct`, `latrine_service_*` | Households with a latrine within the premises, and by type, % |
| `latrine_none_within_premises_total_pct`, `latrine_none_public_latrine_pct`, `latrine_none_open_pct` | Households without a latrine within the premises, and what they use instead, % |
| `bathing_*_pct`, `waste_water_*_pct` | Bathing facility within premises (bathroom / enclosure without roof / none); waste water outlet (closed / open / no drainage), % |
| `cooking_fuel_*_pct` | Fuel used for cooking (fire-wood, crop residue, cowdung cake, coal, kerosene, LPG/PNG, electricity, biogas, other, no cooking), % |
| `kitchen_*_pct` | Cooking inside / outside the house, with or without a kitchen, % |
| `banking_services_availed_pct` | Households availing banking services, % |
| `assets_*_pct` | Households with radio, TV, computer (with / without internet), phone (landline / mobile / both), bicycle, two-wheeler, car, all of TV-computer-phone-vehicle, none of these, % |
| `house_structure_*_pct` | Type of structure: permanent, semi-permanent, temporary (total, serviceable, non-serviceable), unclassifiable, % |

## Notes

- **2011 geography.** Rows are the 35 districts and their tehsils as in Census 2011; `Thane` includes today's Palghar (2014). District names and LGD codes are today's.
- Mumbai City and Mumbai Suburban are fully urban, so they have no `Rural` row.
- Values are percentages as printed (one decimal). A category group adds up to 100 within rounding (99.7 to 100.3).
- Kutcha / tin / asbestos roofs (a heat-exposure indicator) are `roof_grass_thatch_bamboo_wood_mud_etc_pct`, `roof_plastic_polythene_pct` and `roof_g_i_metal_asbestos_sheets_pct`; temporary houses are `house_structure_*temporary_pct`.
- The same files also have town, ward and village rows; these are not converted yet (they are in `raw/`).
- Checks (5 Nov 2026): 1,081 rows (103 district + 978 sub-district rows); no duplicate keys; all values 0-100; category groups add up to 100 within rounding. Nagpur district (total): concrete roof 50.0%, metal/asbestos roof 11.2%, water within premises 71.4%, electricity 92.1%, fire-wood 32.0%, LPG 60.2%, the same as in the file.
