# Installed power capacity by state and sector, 30 September 2026

Power generating capacity available to each state's utilities, by fuel (coal, lignite, gas, diesel, nuclear, hydro, other renewables) and by owner (state, private, central), in megawatts.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *Installed Capacity* monthly report, as on 30.09.2026
- **Table taken from:** sheet "IC Value": the All India table and the region-wise tables "Installed capacity (in MW) of power utilities in the States/UTs located in ... Region including allocated shares in joint & central sector utilities"
- **Link:** https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1003&subSubHeadingId=10014&title=Installed%20Capacity&lang=en (Excel for 2026-09)
- **Downloaded:** 12 Nov 2026 (original in [`_sources/cea-installed-capacity/raw/`](../_sources/cea-installed-capacity/raw/))
- **Script:** [`pipelines/cea/build_installed_capacity.py`](../pipelines/cea/build_installed_capacity.py)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national rows; blank for rows that are not a single state (Jammu & Kashmir and Ladakh together, NLC, DVC, Central - Unallocated, region totals) |
| `region` | Power region: Northern, Western, Southern, Eastern, North-Eastern, Islands |
| `utility_area` | Row label as printed (state, NLC, DVC, "Central - Unallocated", "Total (... Region)") |
| `sector` | `State`, `Private`, `Central` utilities; `Sub-Total` (state total), `Total` (unallocated central capacity), `Grand Total` (region or All India) |
| `coal_mw`, `lignite_mw`, `gas_mw`, `diesel_mw` | Thermal capacity by fuel, MW |
| `thermal_total_mw` | Total thermal, MW |
| `nuclear_mw` | Nuclear, MW |
| `hydro_mw` | Large hydro (including pumped storage), MW |
| `res_mnre_mw` | Other renewables as counted by MNRE (small hydro, biomass, waste-to-energy, solar, wind), MW |
| `renewable_total_mw` | Hydro + other renewables, MW |
| `grand_total_mw` | Total, MW |

## Notes

- **State rows include allocated shares** of central and jointly owned stations, so they show capacity a state's utilities can draw on, not capacity physically located in the state. Central capacity not allocated to any state is in the "Central - Unallocated" rows.
- The source does not split `res_mnre_mw` into wind and solar by state; All India wind capacity is 59,201.07 MW and solar 171,051.46 MW on the same date (summary sheet).
- CEA notes: long-outage units (coal 2,825 MW, gas 4,400.84 MW, nuclear 100 MW from 30.04.2025; a further 370 MW coal/lignite, 978.4 MW gas, 300.861 MW diesel from 31.08.2026) are temporarily removed; off-grid RE included from August 2021; the sector split of RE is provisional; "figures at decimal may not tally due to rounding off".
- Values are kept to 4 decimals (the Excel cells carry floating-point noise beyond that).
- Older monthly reports (2014-03 to 2026-08) are on the same CEA page as PDF only; they are not taken.
- Checks (12 Nov 2026): 181 rows; State + Private + Central = Sub-Total for every state; fuels add up to thermal, hydro + RES to renewable, thermal + nuclear + renewable to grand total in every row; region grand totals = state sub-totals + unallocated; the six regions add up to the All India total, 558,896.39 MW, which matches the summary sheet; no negative values.
