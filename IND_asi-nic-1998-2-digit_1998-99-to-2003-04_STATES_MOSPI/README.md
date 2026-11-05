# Annual Survey of Industries by industry (NIC 1998, 2-digit), 1998-99 to 2003-04

Factory-sector statistics from MoSPI's Annual Survey of Industries (ASI), for each state and All India, by industry at NIC 1998 2-digit level: factories, employment, wages, capital, inputs, output and value added.

## Source

- **Data:** Ministry of Statistics and Programme Implementation (MoSPI), Annual Survey of Industries
- **Table taken from:** MoSPI's ASI API (the data behind eSankhyiki, https://esankhyiki.mospi.gov.in/macroindicators?product=asi)
- **Link:** https://api.mospi.gov.in/api/asi/getASIData
- **Downloaded:** 19 Oct 2026
- **Original file:** [`_sources/mospi-asi/raw/`](../_sources/mospi-asi/raw/) (one gzipped CSV per NIC classification and sector, fields as returned by the API)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `year` | Financial year (April-March) |
| `sector` | Combined, Rural, Urban |
| `nic_code` | NIC 1998 industry code. `99999` = all industries; `99998` = other industries |
| `nic_description` | Industry name as given by the API |
| all other columns | One ASI indicator each, named after the API's label. Unit as suffix: `_inr_lakh` = ₹ lakh, `_inr_000` = ₹ thousand, `_000` = thousand, `_000_tonne`, `_000_kwh`; no suffix = a count |

## Notes

- Industries + Other = All (factories) in 70 of 192 state-years (max difference 4). States vs All India differ by at most 2 factories a year.
- Some value columns (output, product value, depreciation, rent) have a few negative values; they are as returned by the API.
- No blank cells.
- `total_emoluments`, `workmen_and_staff_welfare_exps` and the count columns have no unit in the API; the money ones are probably ₹ lakh but the API does not say.
- `lgd_state_code` added on 5 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
