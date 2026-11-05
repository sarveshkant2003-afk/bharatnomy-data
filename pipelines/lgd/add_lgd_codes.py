"""Add lgd_state_code (and lgd_district_code) columns to every state- and district-level dataset.

Codes come from _reference/geography.csv (build_geography.py). The new columns go right after
`state_ut` / `district`. Other cells are left untouched (read and written as text). Re-running
recomputes the columns, so the script is safe to run again after geography.csv changes.

National-only tables (every row All India) are skipped.\nBlank codes: All India and total rows, old units LGD no longer lists (Dadra & Nagar Haveli,
Daman & Diu before 2020), and district names that could not be matched (listed in
_reference/geography_unmatched.csv).

Each dataset README gets the new columns in its Columns table and a note.

Run from the repo root:  python3 pipelines/lgd/add_lgd_codes.py
"""
import glob
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from build_geography import NOT_PLACES, match_district, norm  # noqa: E402

GEO = Path("_reference/geography.csv")

STATE_ROW = ("| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from "
             "[`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |")
DIST_ROW = ("| `lgd_district_code` | District code in the Local Government Directory (LGD), from "
            "[`_reference/geography.csv`](../_reference/geography.csv). Blank for totals and names that could not be matched |")
NOTE = ("- `lgd_state_code`{d} added on {date} from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). "
        "LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, "
        "new districts) the same code covers a larger area than it does now.")


def main(date="5 Nov 2026"):
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    states = geo[geo.level == "state"].set_index("state_ut").lgd_state_code.to_dict()
    geo_d = geo[geo.level == "district"]
    for f in sorted(glob.glob("*_*/*.csv")):
        if f.startswith("_"):
            continue
        df = pd.read_csv(f, dtype=str, keep_default_na=False)
        if "state_ut" not in df.columns or set(df.state_ut) <= {"All India"}:
            continue  # no state column, or a national-only table
        df = df.drop(columns=[c for c in ("lgd_state_code", "lgd_district_code") if c in df.columns])
        sc = df.state_ut.map(lambda s: states.get(s, ""))
        df.insert(df.columns.get_loc("state_ut") + 1, "lgd_state_code", sc)
        has_d = "district" in df.columns
        if has_d:
            keys = df[["state_ut", "district"] + (["district_census_code"] if "district_census_code" in df else [])].drop_duplicates()
            codes = {}
            for r in keys.itertuples(index=False):
                if not r.district or norm(r.district) in {norm(x) for x in NOT_PLACES}:
                    continue
                idx = match_district(geo_d, r.state_ut, r.district, getattr(r, "district_census_code", None) or None)
                if idx is not None:
                    codes[(r.state_ut, r.district)] = geo_d.at[idx, "lgd_district_code"]
            dc = [codes.get((s, d), "") for s, d in zip(df.state_ut, df.district)]
            df.insert(df.columns.get_loc("district") + 1, "lgd_district_code", dc)
        df.to_csv(f, index=False, lineterminator="\n")
        update_readme(Path(f).parent / "README.md", has_d, date)
        print(f"{Path(f).name}: {len(df)} rows, state codes blank {int((df.lgd_state_code == '').sum())}"
              + (f", district codes blank {int((df.lgd_district_code == '').sum())}" if has_d else ""))


def update_readme(path, has_d, date):
    text = path.read_text()
    if "lgd_state_code" in text:
        return
    lines = text.split("\n")
    # after the first Columns-table row that names state_ut (and district, if separate)
    out, done = [], False
    rows = [STATE_ROW] + ([DIST_ROW] if has_d else [])
    for i, line in enumerate(lines):
        out.append(line)
        if done or not line.startswith("|"):
            continue
        if "`state_ut`" in line:
            if has_d and "`district`" not in line and i + 1 < len(lines) and "`district`" in lines[i + 1]:
                continue  # district is on the next row; insert after that one
            out.extend(rows)
            done = True
        elif has_d and "`district`" in line and "`state_ut`" in lines[i - 1]:
            out.extend(rows)
            done = True
    if not done:
        # state_ut is described in prose above the table: put the rows at the top of the Columns table
        out, in_cols = [], False
        for line in lines:
            out.append(line)
            if line.startswith("## Columns"):
                in_cols = True
            elif in_cols and not done and line.startswith("|---"):
                out.extend(rows)
                done = True
    if not done:
        raise SystemExit(f"{path}: no Columns table; add the LGD rows by hand")
    text = "\n".join(out).rstrip("\n")
    note = NOTE.format(d=" and `lgd_district_code`" if has_d else "", date=date)
    text = text + "\n" + note + "\n" if "## Notes" in text else text + "\n\n## Notes\n\n" + note + "\n"
    path.write_text(text)


if __name__ == "__main__":
    main()
