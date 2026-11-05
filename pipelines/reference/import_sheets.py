"""Copy each sheet variable's definition, unit and listed sources from the four climate variable sheets
into _reference/variables-draft.csv (columns `definition`, `sheet_unit`, `sheet_sources`).

The sheets are kept outside the repo; pass their folder (default: ../Climate next to the repo).
Run from the repo root:  python3 pipelines/reference/import_sheets.py [path/to/Climate]
"""
import sys
from pathlib import Path

import openpyxl
import pandas as pd

SHEETS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("../Climate")
DRAFT = Path("_reference/variables-draft.csv")


def main():
    d = pd.read_csv(DRAFT, dtype=str, keep_default_na=False)
    info = {}
    for f in sorted(SHEETS.glob("*_variables.xlsx")):
        sheet = f.stem.replace("_variables", "")
        ws = openpyxl.load_workbook(f, data_only=True).active
        for r in ws.iter_rows(min_row=2, values_only=True):
            if r[1]:
                info[(sheet, str(int(r[0])))] = (str(r[2] or "").strip(), str(r[3] or "").strip(), " ".join(str(r[4] or "").split()))
    for col, i in (("definition", 0), ("sheet_unit", 1), ("sheet_sources", 2)):
        d[col] = [info[(s, n)][i] for s, n in zip(d.sheet, d.sno)]
    d.to_csv(DRAFT, index=False, lineterminator="\n")
    print(len(d), "rows updated")


if __name__ == "__main__":
    main()
