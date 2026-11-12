# CEA Peak Power Supply Position reports

Original files for [`ENG_peak-demand_2013-01-to-2026-08_STATES_CEA/`](../../ENG_peak-demand_2013-01-to-2026-08_STATES_CEA/).

- **Link:** https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1003&subSubHeadingId=10011&title=Power%20Supply%20Position%20-%20Peak&lang=en (no login)
- **Downloaded:** 12 Nov 2026
- **`raw/`:** [`cea-psp_peak_file-list.tsv`](raw/cea-psp_peak_file-list.tsv) (month and CEA file id of each report, from the page above). The 164 monthly PDFs (`cea-psp_peak_YYYY-MM.pdf`, about 50 MB) are not committed: run `sh pipelines/cea/fetch_psp_peak.sh` from the repo root to download them. The 2015-09 file is empty on CEA's server.
- **Scripts:** [`pipelines/cea/fetch_psp_peak.sh`](../../pipelines/cea/fetch_psp_peak.sh), [`pipelines/cea/build_psp_peak.py`](../../pipelines/cea/build_psp_peak.py)
- Not taken yet: the companion *Energy* Power Supply Position reports (energy requirement and supplied, MU) on the same CEA site.
