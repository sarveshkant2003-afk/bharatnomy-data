# Reference files

Lookup tables shared by all datasets. Scripts that build them are in [`pipelines/`](../pipelines/).

## `geography.csv`: states and districts

One row per state/UT and per district, keyed on the codes of the **Local Government Directory (LGD)**, the Government of India's official list of administrative units. Use it to join datasets that spell places differently, or to link today's districts to Census 2011.

- **Source:** LGD web service (https://lgdirectory.gov.in/), downloaded 5 Nov 2026; Census 2011 codes and names from the Census 2011 basic population figures (ORGI). Raw files and steps: [`_sources/lgd/`](../_sources/lgd/)
- **Built by:** [`pipelines/lgd/build_geography.py`](../pipelines/lgd/build_geography.py)
- **Size:** 38 state rows (36 current states/UTs plus the two units merged in 2020), 792 district rows (790 LGD districts plus Mahe and Yanam, which LGD does not list)

| Column | Meaning |
|---|---|
| `level` | `state` or `district` |
| `state_ut` | State/UT, spelled as in every dataset in this repo |
| `lgd_state_code` | LGD state code. Blank for Dadra & Nagar Haveli and Daman & Diu as separate units (LGD lists only the merged UT, code 38) |
| `census2011_state_code` | Census 2011 state code. Blank for units that did not exist in 2011 (Telangana, Ladakh, the merged DNH & DD) |
| `district` | Current official district name (LGD). Blank on state rows |
| `lgd_district_code` | LGD district code |
| `census2011_district_code` | Census 2011 district code (3 digits). Blank for districts created after 2011 |
| `census2011_name` | Name in Census 2011, as the Census spells it |
| `aliases` | Other spellings, separated by `; `: the Census 2011 name and every spelling used in this repo's datasets (e.g. Ahilyanagar: `Ahmadnagar; Ahmednagar`) |
| `created_after_2011` | `yes` for districts (and states/UTs) formed after Census 2011 |
| `note` | For new districts, the Census 2011 district(s) they were carved from; for states, splits and mergers |

**How the parent of a new district is found:** LGD lists each district's sub-districts (tehsils / talukas) with their Census 2011 sub-district codes, and Census 2011 says which district each sub-district belonged to. So Palghar's talukas all point to Thane. Where the sub-districts carry no Census code (8 districts in Delhi, Ladakh and Tripura), the note says the parent could not be traced.

**Names in the datasets that could not be matched** to an LGD district are listed in [`geography_unmatched.csv`](geography_unmatched.csv). On 5 Nov 2026 there were four, all in `ENV_forest-cover_2023_STATES_FSI_DIST`: Mirpur and Muzaffarabad (listed by FSI, not districts in LGD), "East Siang & Siang" (two districts reported together), Shahdara (not in LGD's current Delhi list).

### LGD codes in the datasets

Every state- and district-level dataset has `lgd_state_code` (and `lgd_district_code`) right after `state_ut` (and `district`), added by [`pipelines/lgd/add_lgd_codes.py`](../pipelines/lgd/add_lgd_codes.py). National-only tables are left as they are.

- Codes are blank for `All India` and `State total` rows, for the old units Dadra & Nagar Haveli and Daman & Diu, and for the unmatched names above.
- An LGD code names today's unit. For data from before a split, the same code covers a bigger area: Andhra Pradesh before June 2014 includes Telangana; Jammu & Kashmir before November 2019 includes Ladakh; Thane in Census 2011 includes today's Palghar.
- Spellings are matched by name, the Census 2011 name, Census 2011 codes where a dataset has them, and a short hand-checked list in `build_geography.py` (`MANUAL_ALIASES`).

### Refreshing

LGD changes as districts are created or renamed. To refresh: `python3 pipelines/lgd/fetch_lgd.py --fresh`, then `build_geography.py`, then `add_lgd_codes.py`.

## `variables-draft.csv`: climate variable log (work in progress)

One row per variable in the four climate variable sheets (air quality, heat and climate resilience, rainfall, wind; 150 rows), recording where each variable ended up. Filled in source by source; a blank `status` means the variable has not been worked on yet.

| Column | Meaning |
|---|---|
| `sheet`, `sno` | Sheet the variable comes from and its serial number there (some variables appear in more than one sheet) |
| `variable_name` | As written in the sheet |
| `dataset` | Folder it ended up in |
| `column` | Column(s) in that CSV, separated by `; ` |
| `unit` | Unit of the values |
| `geo_level` | Lowest level available (`IN`, `STATE`, `DIST`, `CITY`, ...) |
| `frequency` | `annual`, `monthly`, `daily`, `one-off`, ... |
| `earliest_period`, `latest_period` | Coverage |
| `source_used` | Source the values come from |
| `sources_tried` | All sources attempted, in order |
| `status` | `found`, `partial` or `not found` |
| `reason` | Why partial or not found |

## `lenses.csv`: lenses and sub-themes

Bharatnomy's five lenses and the sub-themes variables are grouped under. Edited by hand; every variable in `variables.csv` must use a lens and sub-theme listed here.

| Column | Meaning |
|---|---|
| `lens_id`, `lens_name` | Lens: `CAR` Climate adaptation & resilience, `EPM` Energy policy & markets, `MAC` Macroeconomic health, `EQM` Equity markets, `COM` Commodity markets (21 sub-themes in all) |
| `sub_theme_id`, `sub_theme_name` | Sub-theme within the lens (e.g. `CAR-HEAT` Heat & temperature) |

To add a sub-theme, add a row here, then use its id in the `SUB_THEMES` table of `pipelines/reference/build_variables.py`.

## `variables.csv` (and `variables.xlsx`): the sheet variables we have data for

The variables of the four climate variable sheets, **named exactly as in the sheets** ("Maximum temperature", "Heatwave days", "PM2.5", ...), that exist in a dataset (status `found` or `partial` in `variables-draft.csv`): 52 of the 145 distinct sheet variable names on 5 Nov 2026. A name that appears in two sheets (e.g. "Rainfall deviation") is one variable. `variables.xlsx` is the same table as a plain spreadsheet.

| Column | Meaning |
|---|---|
| `variable_id` | The sheet name in lower case with hyphens (e.g. `heatwave-days`), unique |
| `name` | Variable name as written in the sheet |
| `lens_id`, `sub_theme_id` | Where the variable sits (from `lenses.csv`) |
| `dataset` | Folder holding the values |
| `column` | Column(s) in that folder's CSV, separated by `; ` |
| `unit` | Unit of the values in our data |
| `geo_level` | Lowest level: `IN`, `STATE`, `DIST`, `SDT` (sub-district), `CITY` |
| `frequency` | `annual`, `monthly`, `daily` or `one-off` |
| `earliest_period`, `latest_period` | Coverage |
| `type` | `derived` = computed by Bharatnomy (`BNY` datasets); `raw` = as published by the source |

**Built by** [`pipelines/reference/build_variables.py`](../pipelines/reference/build_variables.py). Its `SUB_THEMES` table assigns every sheet row a lens and sub-theme (also written into `variables-draft.csv` as `lens_id`, `sub_theme_id`). The sheets' definitions, units and listed sources are copied into `variables-draft.csv` (`definition`, `sheet_unit`, `sheet_sources`) by [`import_sheets.py`](../pipelines/reference/import_sheets.py). Columns of the datasets that are not sheet variables are searchable in the dataset search page.

## `registry.json` and the variable explorer

`python3 tools/build_catalog.py` (and the GitHub Actions on every push and pull request) checks `lenses.csv` and `variables.csv` and writes [`registry.json`](../registry.json) (lenses with their sub-themes, the datasets used, and every variable). It **stops with an error, writing nothing**, if a variable:

- points to a dataset folder that does not exist, or a column that is not in that folder's CSV;
- uses a lens or sub-theme that is not in `lenses.csv`, or a sub-theme of another lens;
- has an empty field, a duplicate `variable_id`, or a `type` other than `raw` / `derived`;
- (in `variables-draft.csv`) uses a lens or sub-theme that is not in `lenses.csv`.

The same data is written to `registry.js` for [`variables.html`](../variables.html), the **variable map** on the search site: a mind map with Bharatnomy at the centre, the five lenses around it, their sub-themes, and under each sub-theme the sheet variables by their sheet names. A green dot means we have the data, amber partly, grey not yet. Click a variable for the sheet's definition, unit and sources, and, where we have it, the dataset, columns, geography and period. Typing in the search box trims the map to the matching variables. `registry.json` holds all 145 sheet variables (`sheet_variables`, with status) besides the 52 in `variables.csv`.
