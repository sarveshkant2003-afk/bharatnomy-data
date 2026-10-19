# Bharatnomy Data Repository

Shared store of the datasets behind Bharatnomy's research, starting with the heat-resilience work.
**One folder per source, and we keep the source's whole release**: every table and indicator it publishes,
not only the one we needed first, so the data is already here when another question comes up.
Every folder has a `README.md` saying where the data came from and what each column means.
GitHub shows it automatically when you open the folder.

## What's here

| Folder | Source | What it holds | Level | Period |
|---|---|---|---|---|
| [`moafw-lus/`](moafw-lus/) | Land Use Statistics at a Glance 2024-25, MoA&FW | All 10 tables: nine-fold land use, irrigation by source and by crop, area under 80+ crops | All India; state | 1950-51 to 2024-25 (national); 2015-16 to 2024-25 (state) |
| [`rbi-hsis/`](rbi-hsis/) | RBI Handbook of Statistics on Indian States | Number of factories (from ASI); net sown and net irrigated area (from Land Use Statistics) | State | 2004-05 to 2023-24 / 2020-21 |
| [`fsi-isfr/`](fsi-isfr/) | India State of Forest Report 2023, Forest Survey of India | Forest cover by canopy density for 750 districts; forest and tree cover by state | District; state | 2023 |
| [`mohua-swachhatam/`](mohua-swachhatam/) | MoHUA, Swachhatam portal (via Lok Sabha answer) | Municipal solid waste generated and processed | State | Dec 2023 |

## Find data by topic

| Topic | Where |
|---|---|
| Land use, forest area (land records), fallow, net sown area | `moafw-lus/` (tables 1, 5); older state years in `rbi-hsis/` |
| Irrigation (by source, by crop) | `moafw-lus/` (tables 2, 3, 6-9); older state years in `rbi-hsis/` |
| Crop area | `moafw-lus/` (tables 4, 10) |
| Factories, industry | `rbi-hsis/` |
| Forest cover by district, forest and tree cover (satellite) | `fsi-isfr/` |
| Urban solid waste | `mohua-swachhatam/` |

## File naming

```
<source>/<source>_<indicator>_<geography>_<period>.csv
```

- Lowercase only. Words inside a part are joined with `-`; parts are separated with `_`.
- **source** = `<agency>-<series>`, e.g. `mospi-asi`, `fsi-isfr`. It is also the folder name.
- **indicator** = what the table measures, e.g. `land-use-classification`, `area-under-crops`
- **geography** = `india`, `state`, `district` or `city`; for a single state's file add the state, e.g. `district-uttar-pradesh`
- **period** = one year (`2023`), a month (`2023-12`) or a range (`2004-05-to-2020-21`)

Example: `moafw-lus/moafw-lus_area-under-crops_state_2015-16-to-2024-25.csv`

**Finding files:** press `t` on the repository page and type any part of a name, e.g. `state_2023`, `irrigated`, `crops`.

## Source codes

| Code | Meaning |
|---|---|
| `mospi-asi` | MoSPI, Annual Survey of Industries |
| `moafw-lus` | Ministry of Agriculture & Farmers' Welfare, Land Use Statistics |
| `fsi-isfr` | Forest Survey of India, India State of Forest Report |
| `mohua-swachhatam` | Ministry of Housing & Urban Affairs, Swachhatam portal (Swachh Bharat Mission-Urban) |
| `rbi-hsis` | Reserve Bank of India, Handbook of Statistics on Indian States |

New source? Add a row here: `<agency>-<series>`, lowercase.

## Conventions

- CSV, UTF-8, one header row, plain numbers (no thousand separators). Units are in the column name (`_000_ha` = thousand hectares, `_pct`, `_sq_km`, ...).
- Year-wise data is stored long: one row per state per year. Easy to filter, and loads straight into a database later.
- State/UT names are spelled the same way in every file, so files can be joined.
- `All India` rows are national totals as published. Leave them out before adding states up.
- `source_flag` gives the reason for a blank or a status (`provisional`, `estimated`, ...). `source_marks` keeps any other symbol the source printed next to a number.
- Original downloads go in the folder's `raw/` subfolder (when under 25 MB).

## Adding a dataset

1. Make a folder named after the source code (or use the existing one) and save the original file(s) in `raw/`.
2. Convert every table in the release, not just the one you need, and name each file using the pattern above.
3. Add a `README.md` (or a section in the existing one): what the data is, source with link and download date, one line per column.
4. Commit with a message like `Add <dataset> (<source>, <period>)`.
