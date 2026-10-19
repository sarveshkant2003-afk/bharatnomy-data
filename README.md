# Bharatnomy Data Repository

Shared store of the datasets behind Bharatnomy's research, starting with the heat-resilience work.
One folder per theme. Every folder has a `README.md` saying where the data came from and what each column means.
GitHub shows it automatically when you open the folder.

## What's here

| Folder | Dataset | Level | Period | Original source |
|---|---|---|---|---|
| [`industries/`](industries/) | Number of factories | State | 2004-05 to 2023-24 | Annual Survey of Industries, MoSPI |
| [`land-use/`](land-use/) | Net sown area | State | 2004-05 to 2020-21 | Land Use Statistics, MoA&FW |
| [`forest-cover/`](forest-cover/) | Forest and tree cover | State | ISFR 2023 | Forest Survey of India |
| [`irrigation/`](irrigation/) | Net irrigated area | State | 2004-05 to 2020-21 | Land Use Statistics, MoA&FW |
| [`waste-management/`](waste-management/) | Municipal solid waste generated and processed | State | Dec 2023 | MoHUA (Swachhatam portal) |

## File naming

```
<theme>_<indicator>_<geography>_<period>_<source>.csv
```

- Lowercase only. Words inside a part are joined with `-`; parts are separated with `_`.
- **theme** = the folder name
- **geography** = `state`, `district` or `city`; for a single state's file add the state, e.g. `district-uttar-pradesh`
- **period** = one year (`2023`), a month (`2023-12`) or a range (`2004-05-to-2020-21`)
- **source** = `<agency>-<series>`, e.g. `mospi-asi`, `fsi-isfr`

Example: `forest-cover_forest-tree-cover_state_2023_fsi-isfr.csv`

**Finding files:** press `t` on the repository page and type any part of a name, e.g. `state_2023`, `fsi`, `irrigation`.

## Source codes

| Code | Meaning |
|---|---|
| `mospi-asi` | MoSPI, Annual Survey of Industries |
| `moafw-lus` | Ministry of Agriculture & Farmers' Welfare, Land Use Statistics |
| `fsi-isfr` | Forest Survey of India, India State of Forest Report |
| `mohua-swachhatam` | Ministry of Housing & Urban Affairs, Swachhatam portal (Swachh Bharat Mission-Urban) |

New source? Add a row here: `<agency>-<series>`, lowercase.

## Conventions

- CSV, UTF-8, one header row, plain numbers (no thousand separators).
- Year-wise data is stored long: one row per state per year. Easy to filter, and loads straight into a database later.
- State/UT names are spelled the same way in every file, so files can be joined.
- `All India` rows are national totals as published. Leave them out before adding states up.
- A blank value always has its reason in the `source_flag` column.
- Original downloads go in the folder's `raw/` subfolder (when under 25 MB); code that converts them goes in `scripts/`.

## Adding a dataset

1. Put the file in its theme folder (create a new folder for a new theme).
2. Name it using the pattern above.
3. Add a `README.md` (or a section in the existing one): what the data is, source with link and download date, one line per column.
4. Commit with a message like `Add <dataset> (<source>, <period>)`.

Using Claude Code? Its rules for this repo are in `CLAUDE.md`, so you can just ask it to `add this dataset: <link>`.
