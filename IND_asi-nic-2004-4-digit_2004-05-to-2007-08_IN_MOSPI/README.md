# Annual Survey of Industries by industry (NIC 2004, 4-digit), 2004-05 to 2007-08

Factory-sector statistics from MoSPI's Annual Survey of Industries (ASI), for All India only, by industry at NIC 2004 4-digit level: factories, employment, wages, capital, inputs, output and value added.

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
| `year` | Financial year (April-March) |
| `sector` | Combined |
| `nic_code` | NIC 2004 industry code. `99999` = all industries; `99998` = other industries |
| `nic_description` | Industry name as given by the API |
| all other columns | One ASI indicator each, named after the API's label. Unit as suffix: `_inr_lakh` = ₹ lakh, `_inr_000` = ₹ thousand, `_000` = thousand, `_000_tonne`, `_000_kwh`; no suffix = a count |

## Notes

- The API has only the Combined sector (no rural/urban split) for this classification.
- Industries + Other = All (factories) in 1 of 4 years (max difference 3).
- Some value columns (output, product value, depreciation, rent) have a few negative values; they are as returned by the API.
- No blank cells.
- `total_emoluments`, `workmen_and_staff_welfare_exps` and the count columns have no unit in the API; the money ones are probably ₹ lakh but the API does not say.
