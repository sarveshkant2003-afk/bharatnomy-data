# Weekly storage in India's important reservoirs, April 2015 to May 2025

For each reservoir CWC monitors (91 in 2015, rising to 161 in 2025), every week: water level, live storage, storage as a share of capacity this year, last year and normal, plus the irrigation and hydropower each reservoir serves.

## Source

- **Data:** Central Water Commission (CWC), Ministry of Jal Shakti, weekly bulletin "Live storage status of important reservoirs of India"
- **Table taken from:** the reservoir-wise table of each bulletin ("Region/State wise weekly report of important reservoirs of India"; in older bulletins "Weekly report of nn important reservoirs of India")
- **Link:** https://cwc.gov.in/en/reservoir-level-storage-bulletin (527 bulletins listed on 22 pages, one PDF each)
- **Downloaded:** 12 Nov 2026 (PDFs not committed, about 700 MB; `pipelines/cwc/fetch_bulletins.sh` downloads them, see [`_sources/cwc-reservoir-bulletin/`](../_sources/cwc-reservoir-bulletin/))
- **Script:** [`pipelines/cwc/build_reservoirs.py`](../pipelines/cwc/build_reservoirs.py)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State (standard name); blank for `Andhra Pradesh & Telangana` (reservoirs CWC lists under both states, e.g. Srisailam, Nagarjuna Sagar) |
| `lgd_state_code` | State code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv) |
| `state_as_printed` | State heading as printed in the bulletin (normalised spelling) |
| `region` | CWC region heading (Northern, Eastern, Western, Central, Southern Region) |
| `reservoir` | Reservoir name as printed in that bulletin (spellings change over the years, e.g. `GOBIND SAGAR(BHAKRA)` / `GOBIND SAGAR`) |
| `year` | Year of the bulletin |
| `bulletin_date` | Date of the bulletin ("week ending"), YYYY-MM-DD |
| `reading_date` | Date of the reservoir reading, YYYY-MM-DD (usually the bulletin date, sometimes a few days earlier) |
| `serial` | Serial number in the bulletin (blank where none is printed) |
| `marks_before_serial` | Marks printed before the serial: `*` = reservoir with hydropower benefit of more than 60 MW (CWC), `@`, `#`, `†` = see the bulletin's footnotes (shared irrigation command with other reservoirs) |
| `frl_m` | Full reservoir level, m |
| `current_level_m` | Current water level, m |
| `live_capacity_frl_bcm` | Live storage capacity at full reservoir level, billion cubic metres |
| `current_live_storage_bcm` | Current live storage, billion cubic metres |
| `storage_pct_of_capacity` | Current storage as % of live capacity |
| `storage_last_year_pct_of_capacity` | Storage on the same date last year, % of live capacity |
| `storage_avg_or_normal_pct_of_capacity` | Average of the last 10 years (older bulletins) or "normal" storage (newer bulletins), % of live capacity |
| `irrigation_cca_000_ha` | Culturable command area served, thousand hectares |
| `hydel_capacity_mw` | Installed hydropower capacity, MW |
| `source_marks` | Symbols printed in a value column, as `<column>:<symbol>`: `$`, `@`, `#` in the irrigation column point to footnotes (command area shared with another reservoir) |

## Notes

- Blank cells: `-` in the bulletin (no irrigation or hydropower benefit, or no value) is left blank.
- Dates such as `5/7/2015` in some 2015 bulletins are month/day; each reading date is read as the date nearest the bulletin date.
- Missing bulletins: 10 files on CWC's site return an error page instead of a PDF (2022: 06 Oct, 16 Jun, 02 Jun, 28 Apr, 21 Apr, 13 Apr, 07 Apr, 31 Mar, 10 Mar, 03 Mar), and a few could not be read (scanned images or no reservoir table: e.g. 03 Apr 2025, 27 Mar 2025, 19 Nov 2020, 08 Oct 2020, 03 Jan 2019, 26 Jul 2018, 25 May 2017). Two news-clipping files in the list are not bulletins. A few bulletins are listed twice; duplicates are dropped.
- Reservoir names and the set of reservoirs change over time (CWC added reservoirs in 2019-2025). To follow one reservoir, filter on its name variants.
- Checks (12 Nov 2026): 58,650 rows from 499 bulletins; no duplicate bulletin-state-reservoir keys; storage never above capacity; percentages within 0-100; reading dates never after the bulletin date. 446 bulletins print a "Total for nn reservoirs" line: in 438 the number of rows equals nn, and in 429 the summed capacity and storage match the printed totals within 0.01 BCM. The rest are short by 1-3 reservoirs whose rows are printed in a layout the script does not read (2021-02-04, Aug 2024 to Jan 2025).
