# Local Government Directory (LGD)

Original files used for:

- [`_reference/geography.csv`](../../_reference/geography.csv), the state and district master
- the `lgd_state_code` / `lgd_district_code` columns in the state- and district-level datasets

## Source

- **Data:** Local Government Directory, Ministry of Panchayati Raj. Official codes and names for every state/UT, district and sub-district, with their Census 2011 and 2001 codes
- **Link:** https://lgdirectory.gov.in/ (web services `https://lgdirectory.gov.in/webservices/lgdws/stateList`, `districtList`, `subdistrictList`, POST with form fields `stateCode` / `districtCode`)
- **Downloaded:** 5 Nov 2026
- **Why the web service:** the "Download Directory" page (https://lgdirectory.gov.in/downloadDirectory.do) needs a CAPTCHA for each file, so the same lists are taken from LGD's public web service instead

## Files in `raw/`

| File | What it holds |
|---|---|
| `lgd_states.json` | Every state/UT: LGD code, English and local name, Census 2011 and 2001 codes |
| `lgd_districts.json` | Districts of each state, keyed by LGD state code |
| `lgd_subdistricts.json` | Sub-districts (tehsil / taluka / mandal) of each district, keyed by LGD district code, with Census 2011 sub-district codes |

## Scripts

In [`pipelines/lgd/`](../../pipelines/lgd/), run from the repo root:

1. `fetch_lgd.py`: downloads the three lists into `raw/` (about an hour; the sub-district step resumes if interrupted; `--fresh` re-downloads states and districts too)
2. `build_geography.py`: builds `_reference/geography.csv` from `raw/`, the Census 2011 sub-district file in [`_sources/orgi-census2011/raw/`](../orgi-census2011/raw/) and the names used in the repo's datasets
3. `add_lgd_codes.py`: adds the LGD code columns to the datasets and their READMEs

## Notes

- LGD gives Census 2011 code `00` (Telangana, Ladakh) or none (Dadra & Nagar Haveli and Daman & Diu) for units formed after 2011, and district code `000` or blank for districts formed after 2011. These are stored as blank.
- LGD is updated continuously (new districts, renames). A later download can differ; re-run the three scripts to refresh.
