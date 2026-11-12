# Peak electricity demand and peak met by state, monthly, January 2013 to August 2026

For each state, region and All India, every month: the highest electricity demand (MW) and how much of it was met, with the shortfall.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *Peak Power Supply Position Report (Revised)*, monthly
- **Link:** https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1003&subSubHeadingId=10011&title=Power%20Supply%20Position%20-%20Peak&lang=en (one PDF per month)
- **Downloaded:** 12 Nov 2026 (162 PDFs; not committed, `pipelines/cea/fetch_psp_peak.sh` downloads them, see [`_sources/cea-power-supply-position/`](../_sources/cea-power-supply-position/))
- **Script:** [`pipelines/cea/build_psp_peak.py`](../pipelines/cea/build_psp_peak.py)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India`; blank for regions, DVC, "Others" and "J&K and Ladakh" (reported together from 2019-10) |
| `system` | Row label as printed (English part): state, DVC (Damodar Valley Corporation), region total, `Others (<region>)` (other entities drawing power directly from the inter-state grid), All India |
| `year`, `month` | Year; month as YYYY-MM |
| `peak_demand_mw` | Peak demand in the month, MW net |
| `peak_met_mw` | Peak met (supplied), MW net |
| `surplus_deficit_mw`, `surplus_deficit_pct` | Up to March 2017: "Surplus / Deficit (-)" = peak met minus peak demand, MW and %. Negative = shortage. Blank from April 2017 |
| `demand_not_met_mw`, `demand_not_met_pct` | From April 2017: "Demand not Met" = peak demand minus peak met, MW and %. Positive = shortage. Blank before |
| `source_marks` | Marks printed after the label: `system:*` (CEA: "Excludes the supply to Bangladesh", on Tripura / North-Eastern Region), `system:(**)` (not explained in the report) |

## Notes

- **Sign changes in 2017.** CEA switched from "Surplus / Deficit (-)" to "Demand not Met". The two are kept in separate columns so neither sign is changed. January-March 2017 print the new heading but still use the old sign (negative values), so they are in the surplus/deficit columns.
- Only the month's own figures are kept. Each report also has "April to <month>" figures (the highest monthly peak of the financial year so far), which can be read off the monthly rows.
- Missing months: 2015-09 (CEA's file is empty) and 2021-04 (the file listed as the April 2021 peak report is the energy report). Before 2014-06 there is no Telangana row; Jammu & Kashmir and Ladakh are reported together as "J&K and Ladakh" from 2019-10; Dadra & Nagar Haveli and Daman & Diu are merged from 2020.
- Lakshadweep and Andaman & Nicobar are stand-alone systems and are not part of the regional totals (CEA note). From 2022 the regional figures include other entities drawing power directly from the inter-state grid (the "Others" rows). From 2024 CEA notes "Peak Met has been matched with Peak Demand where Peak Demand is less than Peak Met".
- Labels split across lines in the PDFs (e.g. "Dadra & / Nagar Haveli", "North-Eastern / Region") are joined; in 2015-02 and 2015-03 the Dadra & Nagar Haveli peak (679, 714) is printed inside the word "Haveli" and is read from there.
- Checks (12 Nov 2026): 6,921 rows, 162 months; no duplicate system-month keys; shortfall equals demand minus met (within 1 MW of rounding) in every row; one row has peak met above peak demand (Madhya Pradesh, 2013-03, surplus 3 MW, as printed); percentages within -100 to 100. All India peak demand: 132,948 MW (2013-01) to 258,276 MW (2026-08).
