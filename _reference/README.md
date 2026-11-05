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
