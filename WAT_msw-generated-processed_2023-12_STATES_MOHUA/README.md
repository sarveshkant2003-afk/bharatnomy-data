# Municipal solid waste generated and processed by state, Dec 2023

Municipal solid waste generated and processed per day in each state/UT's cities and towns.

## Source

- **Data:** Ministry of Housing and Urban Affairs (MoHUA), Swachhatam portal
- **Table taken from:** Lok Sabha Unstarred Question No. 3198 "Waste Processing Rates", answered 21 Dec 2023 (Annexure)
- **Link:** https://eparlib.nic.in/bitstream/123456789/2972782/1/AU3198.pdf
- **Downloaded:** 19 Oct 2026

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `waste_generated_tpd` | Municipal solid waste generated, tonnes per day |
| `waste_processed_tpd` | Municipal solid waste processed, tonnes per day |

## Notes

- Urban areas only. Lakshadweep is not in the source, and there is no All India row.
- `lgd_state_code` added on 5 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
