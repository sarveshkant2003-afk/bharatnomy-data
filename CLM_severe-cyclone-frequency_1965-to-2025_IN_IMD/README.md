# Severe cyclones per month by intensity, North Indian Ocean, 1965 to 2025

Number of severe cyclonic storms (and stronger) that formed over the Bay of Bengal and Arabian Sea in each month, by the highest intensity they reached.

## Source

- **Data:** India Meteorological Department (IMD), RSMC New Delhi, cyclone climatology: "Monthly and annual frequency of SCS / VSCS / ESCS / SuCS over NIO during 1965-2024"
- **Link:** https://rsmcnewdelhi.imd.gov.in/report.php?internal_menu=MzM= (file `scs.xls`, six sheets)
- **Downloaded:** 12 Nov 2026 (original in [`_sources/imd-rsmc/raw/`](../_sources/imd-rsmc/raw/))
- **Script:** [`pipelines/imd-rsmc/build_cyclone_climatology.py`](../pipelines/imd-rsmc/build_cyclone_climatology.py)

## Columns

| Column | Meaning |
|---|---|
| `year`, `month` | Year; month as YYYY-MM |
| `scs_48_63kt_count` | Severe cyclonic storms (peak wind 48-63 kt) |
| `vscs_64_89kt_count` | Very severe cyclonic storms (64-89 kt) |
| `escs_90_119kt_count` | Extremely severe cyclonic storms (90-119 kt) |
| `sucs_120kt_plus_count` | Super cyclonic storms (120 kt or more) |
| `vscs_and_above_64kt_plus_count` | Very severe and stronger (64 kt or more), IMD's own sheet |
| `scs_and_above_48kt_plus_count` | Severe and stronger (48 kt or more), IMD's own sheet |

## Notes

- Counts cover the whole North Indian Ocean basin, including storms that hit Bangladesh, Myanmar, Pakistan, Oman etc. or never reached land. For storms by place, see the best tracks ([`CLM_cyclone-best-tracks_1982-to-2026_IN_IMD`](../CLM_cyclone-best-tracks_1982-to-2026_IN_IMD/)).
- The sheet titles say 1965-2024, but each sheet also has a 2025 row; it is kept.
- The sheets' Annual column equals the sum of the months in every row and is left out; so are the Total and Mean rows.
- The two "and above" sheets do not always equal the sum of the separate sheets (as published): 2019-04, 2019-05 (cyclone Fani, April-May 2019, counted in April in the "and above" sheets and in May in the ESCS sheet), 2019-12 (one SCS in "SCS and above" only) and 2020-11 (VSCS + ESCS = 4, "and above" = 2).
- Checks (12 Nov 2026): 732 rows = 61 years x 12 months; no duplicate months; no negative counts.
