"""District and state multidimensional poverty, NFHS-4 (2015-16) and NFHS-5 (2019-21), from NITI Aayog's
National Multidimensional Poverty Index: A Progress Review 2023.

Reads  _sources/niti-mpi/raw/niti-mpi_national-mpi-progress-review_2023.pdf
       - "<State>: Overview of Districts" pages (district headcount ratio, intensity, MPI)
       - "<State>'s Headcount Ratio, Intensity and MPI" block of each state profile (state totals)
Writes SOC_multidimensional-poverty_2015-16-to-2019-21_STATES_NITI_DIST/<same>.csv
Run from the repo root.
"""
import re
import sys
from pathlib import Path

import pandas as pd
import pdfplumber

sys.path.insert(0, str(Path(__file__).parents[1] / "lgd"))
from build_geography import match_district  # noqa: E402

PDF = "_sources/niti-mpi/raw/niti-mpi_national-mpi-progress-review_2023.pdf"
NAME = "SOC_multidimensional-poverty_2015-16-to-2019-21_STATES_NITI_DIST"
V = r"(?:\d+\.\d+%|0?\.\d+|\d\.\d+|–|-)"
ROW = re.compile(rf"^(.*?)\s*({V})\s+({V})\s+({V})\s+({V})\s+({V})\s+({V})\s*$")
STATE_ROW = re.compile(rf"^(2019-21|2015-16)\s+({V})\s+({V})\s+({V})\s*$")
FIX = {"Andaman & Nicobar": "Andaman & Nicobar Islands", "Andaman & Nicobar Island": "Andaman & Nicobar Islands",
       "Jammu & Kashmir": "Jammu & Kashmir", "Dadra & Nagar Haveli & Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu",
       "Dadra & Nagar Haveli and Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu", "NCT of Delhi": "Delhi"}


def val(s):
    if s in ("–", "-"):
        return ""
    return s.rstrip("%")


def state_name(s):
    s = re.sub(r"\s+", " ", s.replace(" and ", " & ")).strip()
    return FIX.get(s, s)


COLX = [205, 268, 334, 394, 456, 522]  # x-centres of the six value columns on the overview pages
# Bihar's overview page (0-based 107) is overprinted with a squeezed copy of Assam's table; the two layers
# share font, size and colour for the numbers and cannot be separated reliably, so Bihar's districts are skipped.
SKIP = {107}


def overview_rows(page, pi, pdf):
    if pi in SKIP:
        return []
    page = page.dedupe_chars()
    words = page.extract_words()
    title = min((w["top"] for w in words if "Overview" in w["text"]), default=0)
    hw = [w["bottom"] for w in words if w["text"] == "MPI" and w["x0"] > 480 and w["top"] > title]
    head = min(hw)  # the column-header row ("Headcount Ratio Intensity MPI ... MPI") below the title
    body = [w for w in words if w["top"] > head + 2 and w["top"] < page.height - 60]
    lines = []
    for w in sorted(body, key=lambda w: w["top"]):
        if lines and w["top"] - lines[-1][0] <= 4:
            lines[-1][1].append(w)
        else:
            lines.append([w["top"], [w]])
    rows, frags = [], []
    for top, ws in lines:
        vals = [w for w in ws if w["x0"] > 180 and re.fullmatch(V, w["text"])]
        name = " ".join(w["text"] for w in sorted(ws, key=lambda w: w["x0"]) if w["x0"] < 180)
        if vals:
            cells = [""] * 6
            for w in vals:
                k = min(range(6), key=lambda j: abs((w["x0"] + w["x1"]) / 2 - COLX[j]))
                cells[k] = w["text"]
            if rows and not name and abs(top - rows[-1]["top"]) < 12 and all(not (c and rows[-1]["cells"][k]) for k, c in enumerate(cells)):
                rows[-1]["cells"] = [x or y for x, y in zip(rows[-1]["cells"], cells)]  # "– – –" printed just above the name
                continue
            rows.append(dict(top=top, name=[(top, name)] if name else [], cells=cells))
        elif name:
            frags.append((top, name))
    for top, name in frags:
        if rows:
            min(rows, key=lambda r: abs(r["top"] - top))["name"].append((top, name))
    out = []
    for r in rows:
        name = re.sub(r"\s+", " ", " ".join(n for _, n in sorted(r["name"]))).strip()
        out.append([name] + [val(c) if c else "" for c in r["cells"]])
    return out


def main():
    pdf = pdfplumber.open(PDF)
    rows, totals = [], []
    for pi, page in enumerate(pdf.pages):
        t = page.extract_text() or ""
        lines = [l.strip() for l in t.split("\n")]
        m = next((re.match(r"^(.+?): Overview of Districts?$", l) for l in lines if re.search(r"Overview of Districts?$", l)), None)
        if m:
            state = state_name(m.group(1))
            for r in overview_rows(page, pi, pdf):
                rows.append([state] + r)
        # state totals: "<State>'s Headcount Ratio, Intensity and MPI" followed by two year rows
        for k, l in enumerate(lines):
            h = re.match(r"^(.+?)['’]s? Headcount Ratio, Intensity and MPI$", l)
            if h:
                yrs = {}
                for l2 in lines[k + 1:k + 5]:
                    s2 = STATE_ROW.match(l2)
                    if s2:
                        yrs[s2.group(1)] = [val(s2.group(i)) for i in (2, 3, 4)]
                if len(yrs) == 2:
                    totals.append([state_name(h.group(1).replace("'", "")), "State total"] + yrs["2015-16"] + yrs["2019-21"])
    cols = ["state_ut", "district", "hcr_2015_16_pct", "intensity_2015_16_pct", "mpi_2015_16",
            "hcr_2019_21_pct", "intensity_2019_21_pct", "mpi_2019_21"]
    wide = pd.DataFrame(rows + totals, columns=cols).drop_duplicates()
    long = []
    for r in wide.itertuples(index=False):
        for y, a, b, c in (("2015-16", r.hcr_2015_16_pct, r.intensity_2015_16_pct, r.mpi_2015_16),
                           ("2019-21", r.hcr_2019_21_pct, r.intensity_2019_21_pct, r.mpi_2019_21)):
            long.append([r.state_ut, r.district, y, a, b, c])
    df = pd.DataFrame(long, columns=["state_ut", "district", "year", "headcount_ratio_pct", "intensity_pct", "mpi"])
    india = df.state_ut == "India"
    df.loc[india, ["state_ut", "district"]] = ["All India", "All India"]
    df["source_flag"] = ["not_available" if not a else "" for a in df.headcount_ratio_pct]
    geo = pd.read_csv("_reference/geography.csv", dtype=str, keep_default_na=False)
    gs = geo[geo.level == "state"].set_index("state_ut").lgd_state_code.to_dict()
    gd = geo[geo.level == "district"]
    df.insert(1, "lgd_state_code", df.state_ut.map(lambda s: gs.get(s, "")))
    codes = {}
    for s, d in set(zip(df.state_ut, df.district)):
        if d != "State total":
            name = re.sub(r"^.*\((.+)\)$", r"\1", d) if match_district(gd, s, d, None) is None else d
            idx = match_district(gd, s, name, None)
            codes[(s, d)] = "" if idx is None else gd.at[idx, "lgd_district_code"]
    df.insert(3, "lgd_district_code", [codes.get((s, d), "") for s, d in zip(df.state_ut, df.district)])
    df = df.assign(_a=df.state_ut == "All India", _t=df.district == "State total")
    df = df.sort_values(["_a", "state_ut", "_t", "district", "year"]).drop(columns=["_a", "_t"])
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, df.shape, "states:", df.state_ut.nunique(), "districts:", (df.district != "State total").sum() // 2,
          "state totals:", (df.district == "State total").sum() // 2)
    un = sorted({(s, d) for s, d, c in zip(df.state_ut, df.district, df.lgd_district_code) if d != "State total" and not c})
    print("no LGD code:", len(un), un[:60])
    return df


if __name__ == "__main__":
    main()
