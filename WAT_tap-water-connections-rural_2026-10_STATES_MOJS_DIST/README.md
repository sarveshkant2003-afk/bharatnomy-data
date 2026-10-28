# Rural households with tap water connections by district, Oct 2026

Number of rural households and how many have a functional household tap connection under the Jal Jeevan Mission (JJM), for every district, as shown on the JJM dashboard on 28 Oct 2026.

## Source

- **Data:** Department of Drinking Water & Sanitation, Ministry of Jal Shakti, Jal Jeevan Mission IMIS
- **Table taken from:** JJM dashboard, "Households with tap water supply" table, state-wise and each state's district-wise view (the dashboard's `Bind_table_graph` data)
- **Link:** https://ejalshakti.gov.in/jjmreport/JJMIndia.aspx
- **Downloaded:** 28 Oct 2026
- **Original file:** [`_sources/jalshakti-jjm/raw/`](../_sources/jalshakti-jjm/raw/) (the JSON the dashboard returns)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT. `State total` rows are the dashboard's state figures |
| `district` | District as spelled on the dashboard |
| `date` | Date the dashboard was read (figures are live, as on that date) |
| `jjm_district_code` | District code used by the dashboard |
| `total_households` | Rural households |
| `households_with_tap` | Rural households with a tap connection |
| `households_with_tap_pct` | Share with a tap connection, % (as published) |
| `households_with_tap_on_2019_08_15` | Households that had a tap connection when JJM started (15 Aug 2019) |
| `households_without_tap` | Households still without a tap connection |

## Notes

- Rural households only. Urban water supply (e.g. Nagpur city) is not covered by JJM; Delhi and Chandigarh are not on the dashboard.
- The dashboard is live; a later download will give different figures.
