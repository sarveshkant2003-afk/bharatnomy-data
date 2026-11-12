"""IMD RSMC New Delhi best tracks of cyclonic disturbances over the North Indian Ocean, 1982-2026.

Reads  _sources/imd-rsmc/raw/imd-rsmc_best-tracks_1982-2026.xlsx (one sheet per year)
Writes CLM_cyclone-best-tracks_1982-to-2026_IN_IMD/<same>.csv

Merged cells (serial number, basin, name and date are printed once per system or day) are read
as the sheet shows them: every cell of a merged range gets the range's value. Rows holding only
IMD's free-text remark (landfall, weakening) are kept in a `remark` column on the track point of
the same system and date that precedes them. From 2018 the serial number is printed only on each
system's first row; the following rows carry it. Run from the repo root.
"""
import re
from datetime import datetime
from pathlib import Path

import openpyxl
import pandas as pd

SRC = Path("_sources/imd-rsmc/raw/imd-rsmc_best-tracks_1982-2026.xlsx")
NAME = "CLM_cyclone-best-tracks_1982-to-2026_IN_IMD"
COLS = ["serial", "basin", "name", "date", "time_utc", "latitude_deg_n", "longitude_deg_e", "ci_number",
        "central_pressure_hpa", "max_sustained_wind_kt", "pressure_drop_hpa", "grade",
        "outermost_isobar_hpa", "outermost_isobar_size_deg"]
NUMERIC = COLS[5:11] + COLS[12:]
NUMERIC.remove("grade") if "grade" in NUMERIC else None


def sheet_values(ws):
    grid = [[c for c in row] for row in ws.iter_rows(values_only=True)]
    for rng in ws.merged_cells.ranges:
        v = grid[rng.min_row - 1][rng.min_col - 1]
        for r in range(rng.min_row, rng.max_row + 1):
            for c in range(rng.min_col, rng.max_col + 1):
                if r - 1 < len(grid) and c - 1 < len(grid[r - 1]):
                    grid[r - 1][c - 1] = v
    return grid


def text(v):
    if v is None:
        return ""
    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return re.sub(r"\s+", " ", str(v)).strip()


def parse_date(s, year):
    if re.fullmatch(r"\d{4}-\d\d-\d\d", s):
        return s
    m = re.fullmatch(r"(\d\d?)[-/.](\d\d?)[-/.](\d{4})", s)
    if m:
        return f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    return ""


def num(s):
    """Return (value, mark): the number as printed, or blank and the printed text as a mark."""
    if s in ("", "-", "--"):
        return "", ""
    if re.fullmatch(r"-?\d+(\.\d+)?", s):
        return s, ""
    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)[.,]?\s*", s)
    if m:
        return m.group(1), s  # stray punctuation after the number
    return "", s


def main():
    wb = openpyxl.load_workbook(SRC, data_only=True)
    out = []
    for ws in wb.worksheets:
        year = ws.title
        grid = sheet_values(ws)
        h = next(i for i, r in enumerate(grid[:5]) if any("serial" in text(v).lower() for v in r))
        last = None
        for r in grid[h + 1:]:
            cells = [text(v) for v in (list(r) + [None] * 14)[:14]]
            if not any(cells):
                continue
            lat_ok = re.match(r"^-?\d+(\.\d+)?\.?$", cells[5]) and re.match(r"^-?\d+(\.\d+)?\.?$", cells[6])
            date = parse_date(cells[3], year)
            if lat_ok and date:
                if cells[0]:
                    serial = cells[0]
                elif last is not None and last["year"] == year:
                    cells[0] = serial  # from 2018 the serial is printed only on a system's first row
                rec = dict(zip(COLS, cells))
                rec["year"], rec["date"], rec["remark"] = year, date, ""
                rec["time_utc"] = cells[4].zfill(4) if cells[4].isdigit() else cells[4]
                marks = []
                for c in NUMERIC:
                    rec[c], m = num(rec[c])
                    if m:
                        marks.append(f"{c}:{m}")
                rec["source_marks"] = "; ".join(marks)
                out.append(rec)
                last = rec
            else:
                # a remark row: the text is in the first cell after the key columns that is not a date/time
                t = next((c for c in cells[3:] if c and not parse_date(c, year) and not c.isdigit()), "")
                if t and last is not None and last["year"] == year:
                    last["remark"] = (last["remark"] + " | " + t) if last["remark"] and t not in last["remark"] else (last["remark"] or t)
    df = pd.DataFrame(out)
    df = df[["year", "serial", "basin", "name", "date", "time_utc"] + COLS[5:] + ["remark", "source_marks"]]
    df["serial"] = df.serial.str.replace(r"\.0$", "", regex=True)
    df = df.sort_values(["year", "date", "time_utc"], kind="stable")
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(len(df), "track points;", df.groupby("year").serial.nunique().sum(), "systems")


if __name__ == "__main__":
    main()
