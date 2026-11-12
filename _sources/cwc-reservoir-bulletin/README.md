# CWC weekly reservoir storage bulletins

Original files for [`WAT_reservoir-storage_2015-to-2025_STATES_CWC/`](../../WAT_reservoir-storage_2015-to-2025_STATES_CWC/).

- **Link:** https://cwc.gov.in/en/reservoir-level-storage-bulletin (no login)
- **Downloaded:** 12 Nov 2026
- **`raw/`:** [`cwc-reservoir-bulletin_file-list.tsv`](raw/cwc-reservoir-bulletin_file-list.tsv): date (from the title), PDF link and title of all 527 entries on the page's 22 pages. The PDFs (`raw/pdf/`, about 700 MB) are not committed: run `sh pipelines/cwc/fetch_bulletins.sh` from the repo root to download them.
- **Scripts:** [`pipelines/cwc/fetch_bulletins.sh`](../../pipelines/cwc/fetch_bulletins.sh), [`pipelines/cwc/build_reservoirs.py`](../../pipelines/cwc/build_reservoirs.py)
- Only the reservoir-wise table is taken. Each bulletin also has region, basin and state summaries, drought-prone sub-division tables and maps.
