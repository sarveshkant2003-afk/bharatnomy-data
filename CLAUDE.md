# CLAUDE.md

Instructions for Claude Code in the Bharatnomy data repository.
Also read @README.md: its naming pattern, source codes and conventions are binding.

## What this repo is

A shared, browsable store of public datasets for Bharatnomy's research (first use: heat resilience).
It is not a database yet: one folder per theme, tidy CSV files, and a README.md in every folder.
Most teammates only read it on GitHub, so every file must make sense in the browser.

## Main job: add a dataset

When I say something like "add this: <link | file | pasted table>", do the whole job without asking.
Ask only when the source itself is ambiguous (which table, year, unit or geography I mean) or a rule below says stop.

1. **Get the original.** Download it with `curl -L` into `<theme>/raw/`, named like the CSV will be (same base name, original extension). Prefer the agency's own CSV/XLSX, then PDF, then an HTML table. If the site needs a login, form, CAPTCHA or API key, or blocks scripts, stop and ask me to put the file in `raw/` myself.
2. **Extract exactly what is published.** Parse the file with code; never retype numbers that can be parsed. If the only copy is a scan or image, tell me before transcribing and say so in the README.
3. **Clean** it to the CSV rules below. Save the conversion code as `scripts/<csv base name>.py`: it reads from `raw/`, writes the CSV, and can be re-run.
4. **Name** the file with the pattern in README.md. New theme: new folder (lowercase, hyphenated). New source: add its code to the Source codes table in README.md.
5. **Check** it (section below). Never edit values to make a check pass; report the failure instead.
6. **Document** it: write or update `<theme>/README.md` from the template below, and add a row to the "What's here" table in the root README.md.
7. **Report back:** file path, rows x columns, period covered, every check with its result, and anything odd in the source.
8. **Commit** (see Git). Do not push unless I ask.

Newer release of an existing dataset: replace the CSV (use `git mv` if the period in the name changes), refresh `raw/`, the script and the README, then re-run all checks.

## CSV rules

- UTF-8, comma-separated, one header row, LF line endings. No notes, footnotes, blank rows or merged headers inside the CSV; those go in the README.
- One source table per CSV. Key columns first: `state_ut`, then `district` / `city` if any, then time.
- Time: `year` for annual data, written as published (`2023`, `2023-24`); `month` as `YYYY-MM`; `date` as `YYYY-MM-DD`.
- Data with more than one period is stored long: one row per place per period, one column per variable.
- Column names in snake_case with the unit as a suffix: `_sq_km`, `_000_ha` (thousand hectares), `_tpd` (tonnes per day), `_pct`, `_inr_crore`. Keep the source's unit; never rescale.
- Numbers: plain digits, `.` as decimal. Convert Indian grouping (`1,23,456.78` becomes `123456.78`). Keep the source's decimals. No `%`, `₹` or words in numeric cells.
- A blank cell needs a reason in a `source_flag` column, using only: `not_applicable`, `not_available`, `estimated`, `provisional`, `revised`. Say in the README which source symbol maps to which flag. Leave out `source_flag` if the source has no markers or blanks.
- Keep published totals as rows: `All India` in state files, `State total` in district files.
- Store data as published: no derived columns (shares, per capita, growth) and no filling of gaps.
- Sort by the key columns, totals last.

## Place names

Use exactly these for `state_ut`:
Andaman & Nicobar Islands, Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chandigarh, Chhattisgarh,
Dadra & Nagar Haveli and Daman & Diu, Delhi, Goa, Gujarat, Haryana, Himachal Pradesh, Jammu & Kashmir,
Jharkhand, Karnataka, Kerala, Ladakh, Lakshadweep, Madhya Pradesh, Maharashtra, Manipur, Meghalaya,
Mizoram, Nagaland, Odisha, Puducherry, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura,
Uttar Pradesh, Uttarakhand, West Bengal, All India.

Old units only for years when they existed: `Dadra & Nagar Haveli` and `Daman & Diu` (merged in 2020).

Common variants: NCT of Delhi → Delhi; A&N Islands / Andaman and Nicobar Islands → Andaman & Nicobar Islands;
Jammu and Kashmir / J&K → Jammu & Kashmir; Orissa → Odisha; Pondicherry → Puducherry; Uttaranchal → Uttarakhand;
DNH&DD / Dadra Nagar Haveli and Daman & Diu → Dadra & Nagar Haveli and Daman & Diu;
ALL INDIA / All-India / India / Total → All India.

Districts: keep the source's spelling. If the source gives LGD or Census codes, keep them as columns
(`district_lgd_code`, `district_census_code`, and the same for states). Never guess codes.

## Checks (run every time and show me the results)

- Row count matches places x periods; no duplicate keys; no empty key cells.
- Every `state_ut` value is in the list above.
- Numeric columns parse as numbers; no negative counts or areas.
- If the source prints totals, recompute them and compare. Report differences; never change data to match.
- Logical limits: percentages within 0-100; a part never larger than its whole (e.g. irrigated area <= sown area).
- Spot check: show me 5 random rows next to the same cells in the source.
- Size: a CSV over 25 MB, stop and ask. Never commit any file over 50 MB (GitHub warns at 50 MB and rejects over 100 MB). Raw files over 25 MB are not committed; put their link in the README instead.

## Folder README template

One README.md per folder. If a folder holds several CSVs, repeat the block for each under a `## <file name>` heading.
Keep it short and plain: it is for teammates who will never open the code.

```markdown
# <What, where, when, e.g. Net irrigated area by state, 2004-05 to 2020-21>

<One or two plain sentences on what the numbers measure.>

## Source

- **Data:** <original agency, publication or series>
- **Table taken from:** <exact table or page used, with its publication date; omit if it is the agency's own file>
- **Link:** <URL>
- **Downloaded:** <today's date, e.g. 19 Oct 2026>

## Columns

| Column | Meaning |
|---|---|
| `column_name` | What it is, with unit |

## Notes

- <Breaks in the series, state splits or mergers, missing places, definitions, check results worth knowing>
```

## Sources

- Free, publicly downloadable sources only. No RTI requests.
- Prefer the original agency. Official republications (RBI Handbook of Statistics on Indian States, PIB releases, Lok Sabha / Rajya Sabha answers) are fine: record both the agency and the exact table used.
- Never use aggregators or secondary sites (Wikipedia, Indiastat, dataful, news or coaching sites) as the source; use them only to find the official one. If there is no official source, ask me.

## Git

- One dataset per commit. Messages: `Add <dataset> (<source>, <period>)`, `Update <dataset> to <period>`, `Fix <what> in <file>`.
- Run `git status` first and stage only the files you created or changed.
- Never force-push, rewrite history or delete a dataset unless I ask.
- Push only when I say so.

## First-time setup (only if `git remote -v` shows nothing)

1. Not a git repo yet: `git init -b main`, then commit everything as `Initial data repository`.
2. I create the GitHub organisation myself on github.com (it can't be done from the terminal). Ask me for its name.
3. If `gh` is missing: `brew install gh`. I will run `gh auth login` myself.
4. `gh repo create <org>/bharatnomy-data --private --source=. --remote=origin --push`

## Environment

- macOS with Homebrew. Use `python3` in a venv at `.venv/` (`python3 -m venv .venv && source .venv/bin/activate`). Install only what a task needs: `pandas`, `openpyxl`, `pdfplumber`.
- For "do we have data on X?", search filenames and READMEs (`git ls-files`, `grep -ril`) before going online.

## Known gaps (update this list as you fix them)

- `land-use/` and `irrigation/` stop at 2020-21. RBI's Handbook of Statistics on Indian States 2024-25 has both up to 2023-24 (net irrigated area is Table 56 there). Update the two together so they stay joinable on `state_ut` + `year`.
- The first five datasets have no `raw/` files yet. Save the originals (the RBI table pages offer XLSX downloads; the Lok Sabha answer is a PDF; the forest table is in a PIB release), confirm they match the CSVs, then add their `scripts/`.
- Everything is state level. The heat-resilience work needs district-level data next.
