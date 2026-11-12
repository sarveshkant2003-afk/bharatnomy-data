# RBI Handbook of Statistics on Indian States (selected tables)

Original files for this release. The cleaned data is in one folder per table:

- [`AGR_net-irrigated-area_2004-05-to-2020-21_STATES_RBI/`](../../AGR_net-irrigated-area_2004-05-to-2020-21_STATES_RBI/)
- [`AGR_net-sown-area_2004-05-to-2020-21_STATES_RBI/`](../../AGR_net-sown-area_2004-05-to-2020-21_STATES_RBI/)
- [`IND_factories_2004-05-to-2023-24_STATES_RBI/`](../../IND_factories_2004-05-to-2023-24_STATES_RBI/)

## Source

- **Links:** each table's link is in its folder's README
- **`raw/`:** [`rbi-hsis_table-list_2025.tsv`](raw/rbi-hsis_table-list_2025.tsv): the 181 tables of the 2024-25 edition (Dec 2025) with their XLSX links, from https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=Handbook%20of%20Statistics%20on%20Indian%20States (listed 12 Nov 2026).
- **Blocked:** RBI's document server (rbidocs.rbi.org.in) answers scripts with a bot-check page instead of the file, so the tables could not be downloaded automatically. To add them, open the links in a browser and save each file in `raw/` as `rbi-hsis_table-NNN_2025.xlsx` (NNN = table number, 3 digits). Tables most needed for the climate variables: 10 (multidimensional poverty), 16 (doctors), 17 (hospitals and beds), 19-20 (per capita NSDP), 80-88 (crop yields), 104 (heat wave days), 105 (relief expenditure), 107 (groundwater extraction), 140 and 143 (installed power and renewable capacity), 142 (peak demand).
- **Downloaded:** 19 Oct 2026
