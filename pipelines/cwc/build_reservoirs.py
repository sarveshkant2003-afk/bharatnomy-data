"""CWC weekly bulletins "Live storage status of important reservoirs": reservoir-wise table, April 2015 to May 2025.

Reads  _sources/cwc-reservoir-bulletin/raw/pdf/*.pdf (fetch_bulletins.sh)
Writes WAT_reservoir-storage_2015-to-2025_STATES_CWC/<same>.csv
Uses the reservoir-wise weekly report pages ("REGION/STATE WISE WEEKLY REPORT ..." when present, otherwise
"WEEKLY REPORT OF nn IMPORTANT RESERVOIRS"). Run from the repo root.
"""
import glob
import re
import sys
from pathlib import Path

import pandas as pd
import pdfplumber

RAW = "_sources/cwc-reservoir-bulletin/raw/pdf"
NAME = "WAT_reservoir-storage_2015-to-2025_STATES_CWC"
N = r"(?:-?\d+(?:\.\d+)?|-|\$|@|#|\*+|NA|N\.A\.?)"
DATE = r"(\d{1,2})[./-](\d{1,2})[./-](\d{4}|\d{2})"
ROW = re.compile(rf"^([*@#$'’†]*)\s*(\d+)?\s*([A-Za-z].+?)\s*({N})\s+({N})\s+({N})\s+({N})\s+{DATE}\s*({N})\s+({N})\s+({N})(?:\s+({N}))?(?:\s+({N}))?\s*$")
STATES = {
    "himachal pradesh": "Himachal Pradesh", "punjab": "Punjab", "rajasthan": "Rajasthan", "jharkhand": "Jharkhand",
    "odisha": "Odisha", "orissa": "Odisha", "west bengal": "West Bengal", "tripura": "Tripura", "gujarat": "Gujarat",
    "gujrat": "Gujarat", "maharashtra": "Maharashtra", "uttar pradesh": "Uttar Pradesh", "uttarakhand": "Uttarakhand",
    "madhya pradesh": "Madhya Pradesh", "chhattisgarh": "Chhattisgarh", "chattisgarh": "Chhattisgarh",
    "andhra pradesh": "Andhra Pradesh", "telangana": "Telangana", "ap&tg": "Andhra Pradesh & Telangana",
    "ap & tg": "Andhra Pradesh & Telangana", "a.p & tg": "Andhra Pradesh & Telangana",
    "andhra pradesh & telangana": "Andhra Pradesh & Telangana", "karnataka": "Karnataka", "kerala": "Kerala",
    "tamil nadu": "Tamil Nadu", "assam": "Assam", "bihar": "Bihar", "meghalaya": "Meghalaya", "mizoram": "Mizoram",
    "nagaland": "Nagaland", "goa": "Goa", "sikkim": "Sikkim", "manipur": "Manipur", "jammu & kashmir": "Jammu & Kashmir",
    "arunachal pradesh": "Arunachal Pradesh",
}


def norm_state(line):
    k = re.sub(r"\s+", " ", line.strip().lower().replace(" and ", " & ")).strip(" :")
    return STATES.get(k)


def bulletin_date(text):
    m = re.search(r"(?:WEEK ENDING\s*:?-?|AS ON\s*:?)\s*" + DATE, text, re.I) or re.search(r"^\s*" + DATE + r"\s*$", text, re.M)
    if not m:
        return ""
    d, mo, y = m.groups()
    y = y if len(y) == 4 else "20" + y
    return f"{y}-{int(mo):02d}-{int(d):02d}"


def read_date(a, b, y, line, bdate):
    """Reading date; dd-mm-yyyy normally, but some 2015 bulletins print m/d/yyyy: take the reading nearest the bulletin date."""
    y = y if len(y) == 4 else "20" + y
    cands = []
    for d, m in ((a, b), (b, a)):
        try:
            cands.append(pd.Timestamp(int(y), int(m), int(d)))
        except ValueError:
            pass
    if not cands:
        return ""
    if bdate:
        ref = pd.Timestamp(bdate)
        cands.sort(key=lambda t: abs((t - ref).days))
    return cands[0].strftime("%Y-%m-%d")


def parse(f):
    pdf = pdfplumber.open(f)
    texts = [(p.extract_text() or "") for p in pdf.pages]
    pages = [t for t in texts if "REGION/STATE WISE WEEKLY REPORT" in t.upper()]
    if not pages:
        pages = [t for t in texts if re.search(r"WEEKLY REPORT OF\s+\d+\s+IMPORTANT RESERVOIRS", t, re.I)]
    if not pages:
        return [], ""
    bdate = bulletin_date(pages[0]) or bulletin_date("\n".join(texts[:6]))
    out, state, region, last = [], "", "", None
    total = None
    for t in pages:
        for line in t.split("\n"):
            s = line.strip()
            s = re.sub(r"(\d+\.\d{3})(\d+\.\d{3})", r"\1 \2", s)  # FRL glued to current level (newer bulletins)
            tm = re.search(r"TOTAL\s+(?:FOR\s+)?\D{0,12}?(\d+)\s+RESERVOIRS\s+(\d+\.\d+)\s+(\d+\.\d+)", s, re.I)
            if tm and total is None:
                total = (int(tm.group(1)), float(tm.group(2)), float(tm.group(3)))
            m = ROW.match(s)
            if m:
                g = m.groups()
                last = dict(region=region, state=state, serial=g[1] or "", reservoir=g[2].strip(), marks_before_serial=g[0],
                            frl_m=g[3], current_level_m=g[4], live_capacity_frl_bcm=g[5], current_live_storage_bcm=g[6],
                            reading_date=read_date(g[7], g[8], g[9], s, bdate),
                            storage_pct_of_capacity=g[10], storage_last_year_pct_of_capacity=g[11],
                            storage_avg_or_normal_pct_of_capacity=g[12], irrigation_cca_000_ha=g[13] or "",
                            hydel_capacity_mw=g[14] or "")
                out.append(last)
                continue
            st = norm_state(s)
            if st:
                state, last = st, None
            elif re.search(r"\bREGION\b", s, re.I) and len(s) < 40 and not re.search(r"\d", s):
                region, last = s.title(), None
            elif last is not None and re.fullmatch(r"[A-Z][A-Z .()\-&']{1,30}", s):
                last["reservoir"] += " " + s  # name wrapped onto the next line
                last = None
            else:
                last = None
    for r in out:
        r["_total"] = total
    return out, bdate


def main(files=None):
    files = files or sorted(glob.glob(f"{RAW}/*.pdf"))
    rows, log = [], []
    for f in files:
        try:
            r, d = parse(f)
        except Exception as e:  # damaged or scanned file
            log.append((Path(f).name, "error " + str(e)[:60]))
            continue
        log.append((Path(f).name, f"{len(r)} rows, date {d}"))
        for x in r:
            x["bulletin_date"] = d
        rows += r
    df = pd.DataFrame(rows)
    VAL = ["frl_m", "current_level_m", "live_capacity_frl_bcm", "current_live_storage_bcm", "storage_pct_of_capacity",
           "storage_last_year_pct_of_capacity", "storage_avg_or_normal_pct_of_capacity", "irrigation_cca_000_ha", "hydel_capacity_mw"]
    marks = [[] for _ in range(len(df))]
    for c in VAL:
        v = df[c].fillna("")
        for i, x in enumerate(v):
            if x and not re.fullmatch(r"-?\d+(?:\.\d+)?", x) and x not in ("-", "NA", "N.A", "N.A."):
                marks[i].append(f"{c}:{x}")
        df[c] = v.where(v.str.fullmatch(r"-?\d+(?:\.\d+)?"), "")
    df["source_marks"] = ["; ".join(m) for m in marks]
    return df, log


def write(df):
    geo = pd.read_csv("_reference/geography.csv", dtype=str, keep_default_na=False)
    gs = geo[geo.level == "state"].set_index("state_ut").lgd_state_code.to_dict()
    df = df[df.bulletin_date != ""].copy()
    # a few bulletins are listed twice on CWC's page (same date, same table): keep one copy
    df = df.drop_duplicates(["bulletin_date", "state", "reservoir", "current_live_storage_bcm", "reading_date"])
    df["state_as_printed"] = df.state
    df["state_ut"] = df.state.where(df.state.isin(gs.keys()), "")
    df["lgd_state_code"] = df.state_ut.map(lambda x: gs.get(x, ""))
    df["year"] = df.bulletin_date.str[:4]
    cols = ["state_ut", "lgd_state_code", "state_as_printed", "region", "reservoir", "year", "bulletin_date", "reading_date",
            "serial", "marks_before_serial", "frl_m", "current_level_m", "live_capacity_frl_bcm", "current_live_storage_bcm",
            "storage_pct_of_capacity", "storage_last_year_pct_of_capacity", "storage_avg_or_normal_pct_of_capacity",
            "irrigation_cca_000_ha", "hydel_capacity_mw", "source_marks"]
    df = df[cols].sort_values(["state_as_printed", "reservoir", "bulletin_date"])
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, df.shape)
    return df


if __name__ == "__main__":
    df, log = main(sys.argv[1:] or None)
    for l in log:
        print(*l)
    write(df)
