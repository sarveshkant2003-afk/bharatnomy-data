# Periodic Labour Force Survey (MoSPI)

Original files for this release. The cleaned data is in one folder per table:

- [`LAB_plfs-persons-nagpur_2025_MH_MOSPI_DIST/`](../../LAB_plfs-persons-nagpur_2025_MH_MOSPI_DIST/)
- [`LAB_plfs-households-nagpur_2025_MH_MOSPI_DIST/`](../../LAB_plfs-households-nagpur_2025_MH_MOSPI_DIST/)

## Source

- **Unit-level data, Calendar Year 2025:** https://microdata.gov.in/NADA/index.php/catalog/284 (free login needed). Downloaded 23 Oct 2026 as `Data_in_CSV.zip` (34.6 MB: `chhv12025.csv`, 270,472 households; `cperv12025.csv`, 1,148,634 persons). Not committed because it is over 25 MB; it is kept locally as `raw/mospi-plfs_unit-level-first-visit-csv_2025.zip`.
- **`raw/docs-2025/`:** the release's public documents from the same catalog page (questionnaire, data layout, district and state code lists, basic strata list, field instructions, MoSPI's README). Downloaded 23 Oct 2026.
- Other PLFS releases on the portal (2017-18 to 2023-24, monthly and quarterly 2025) are at https://microdata.gov.in/NADA/index.php/catalog/PLFS. MoSPI's PLFS API (https://api.mospi.gov.in/api/plfs/getData) has state-level estimates only.
