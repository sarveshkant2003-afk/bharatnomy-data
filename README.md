# Bharatnomy Data Repository

Public datasets for Bharatnomy's research. One folder per source; each folder's `README.md` gives the source and explains every column.

## What's here

| Folder | Source | What it holds | Level | Period |
|---|---|---|---|---|
| [`moafw-lus/`](moafw-lus/) | Land Use Statistics at a Glance 2024-25, MoA&FW | Land use, irrigation by source and by crop, area under crops | All India; state | 1950-51 to 2024-25 (national); 2015-16 to 2024-25 (state) |
| [`rbi-hsis/`](rbi-hsis/) | RBI Handbook of Statistics on Indian States | Number of factories; net sown and net irrigated area | State | 2004-05 to 2023-24 / 2020-21 |
| [`fsi-isfr/`](fsi-isfr/) | India State of Forest Report 2023, Forest Survey of India | Forest cover by district; forest and tree cover by state | District; state | 2023 |
| [`mohua-swachhatam/`](mohua-swachhatam/) | MoHUA, Swachhatam portal | Municipal solid waste generated and processed | State | Dec 2023 |

## Find data by topic

| Topic | Where |
|---|---|
| Land use, net sown area, fallow | `moafw-lus/`; older state years in `rbi-hsis/` |
| Irrigation | `moafw-lus/`; older state years in `rbi-hsis/` |
| Crop area | `moafw-lus/` |
| Factories | `rbi-hsis/` |
| Forest cover | `fsi-isfr/` |
| Urban solid waste | `mohua-swachhatam/` |

## File names

```
<source>/<source>_<indicator>_<geography>_<period>.csv
```

- **source** = `<agency>-<series>`, also the folder name
- **geography** = `india`, `state`, `district` or `city`
- **period** = a year (`2023`), a month (`2023-12`) or a range (`2004-05-to-2020-21`)

Example: `moafw-lus/moafw-lus_area-under-crops_state_2015-16-to-2024-25.csv`. Press `t` on the repository page to search file names.

## Source codes

| Code | Meaning |
|---|---|
| `moafw-lus` | Ministry of Agriculture & Farmers' Welfare, Land Use Statistics |
| `fsi-isfr` | Forest Survey of India, India State of Forest Report |
| `mohua-swachhatam` | Ministry of Housing & Urban Affairs, Swachhatam portal |
| `rbi-hsis` | Reserve Bank of India, Handbook of Statistics on Indian States |

## Conventions

- CSV, UTF-8, plain numbers. The unit is in the column name (`_000_ha` = thousand hectares, `_sq_km`, `_pct`, `_tpd` = tonnes per day).
- One row per place per year. State names are spelled the same in every file, so files can be joined.
- `All India` and `State total` rows are published totals; leave them out before adding up.
- `source_flag` says why a cell is blank or its status (`provisional`, `estimated`, ...). `source_marks` keeps other symbols printed next to a number.
- Original source files are in each folder's `raw/`.
