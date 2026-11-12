"""CEA monthly Peak Power Supply Position reports (PDF, one page each), Jan 2013 to Aug 2026: peak demand and peak met by state.

Reads  _sources/cea-power-supply-position/raw/cea-psp_peak_YYYY-MM.pdf (fetch_psp_peak.sh)
Writes ENG_peak-demand_2013-01-to-2026-08_STATES_CEA/<same>.csv
Only the month's own four columns are kept (the April-to-date columns are the highest monthly values so far).
Run from the repo root.
"""
import glob
import re
from pathlib import Path

import pandas as pd
import pdfplumber

RAW = "_sources/cea-power-supply-position/raw"
NAME = "ENG_peak-demand_2013-01-to-2026-08_STATES_CEA"
NUM = r"-?[\d,]+(?:\.\d+)?"
ROW = re.compile(rf"^(.*?)\s*((?:{NUM}\s+){{3}}{NUM}(?:\s+(?:{NUM}\s+){{3}}{NUM})?)\s*$")
STATE = {"Chandigarh": "Chandigarh", "Delhi": "Delhi", "Haryana": "Haryana", "Himachal Pradesh": "Himachal Pradesh",
         "Jammu & Kashmir": "Jammu & Kashmir", "Punjab": "Punjab", "Rajasthan": "Rajasthan", "Uttar Pradesh": "Uttar Pradesh",
         "Uttarakhand": "Uttarakhand", "Chhattisgarh": "Chhattisgarh", "Gujarat": "Gujarat", "Madhya Pradesh": "Madhya Pradesh",
         "Maharashtra": "Maharashtra", "Daman & Diu": "Daman & Diu", "Dadra & Nagar Haveli": "Dadra & Nagar Haveli",
         "Dadra & Nagar Haveli and Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu", "Goa": "Goa",
         "Andhra Pradesh": "Andhra Pradesh", "Telangana": "Telangana", "Karnataka": "Karnataka", "Kerala": "Kerala",
         "Tamil Nadu": "Tamil Nadu", "Puducherry": "Puducherry", "Lakshadweep": "Lakshadweep", "Bihar": "Bihar",
         "Jharkhand": "Jharkhand", "Odisha": "Odisha", "West Bengal": "West Bengal", "Sikkim": "Sikkim",
         "Andaman & Nicobar": "Andaman & Nicobar Islands", "Andaman & Nicobar Islands": "Andaman & Nicobar Islands",
         "Arunachal Pradesh": "Arunachal Pradesh", "Assam": "Assam", "Manipur": "Manipur", "Meghalaya": "Meghalaya",
         "Mizoram": "Mizoram", "Nagaland": "Nagaland", "Tripura": "Tripura", "All India": "All India"}


# labels whose first or second half is on another line (the other half is a separate line of text)
FRAG = {"Nicobar": "Andaman- Nicobar", "Arunachal": "Arunachal Pradesh", "Region": "North-Eastern Region",
        "Region*": "North-Eastern Region*", "Nagar Haveli": "Dadra & Nagar Haveli", "Haveli": "Dadra & Nagar Haveli",
        "Dadra & Nagar": "Dadra & Nagar Haveli", "DNH": "Dadra & Nagar Haveli", "Telenagana": "Telangana",
        "Dadra & Nagar Haveli and Daman &": "Dadra & Nagar Haveli and Daman & Diu"}


def english(s):
    """English part of a bilingual label 'हिंदी / English (#)'."""
    s = s.split("/")[-1] if "/" in s else s
    s = re.sub(r"\(#+\)|#+|\(\*\)|\(\$\)|\$|\(\)", "", s)
    s = re.sub(r"[^\x20-\x7e]", "", s)
    return re.sub(r"\s+", " ", s).strip(" -")


def canon(name):
    n = name.replace(" and ", " & ").replace("&", " & ")
    n = re.sub(r"\s+", " ", n).strip()
    n = {"Orissa": "Odisha", "Andaman- Nicobar": "Andaman & Nicobar", "Andaman-Nicobar": "Andaman & Nicobar",
         "Dadra & Nagar Haveli & Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu",
         "Dadar Nagar Haveli": "Dadra & Nagar Haveli", "Dadra Nagar Haveli": "Dadra & Nagar Haveli"}.get(n, n)
    return n


def parse(f):
    month = re.search(r"(\d{4}-\d\d)\.pdf$", f).group(1)
    text = pdfplumber.open(f).pages[0].extract_text() or ""
    lines = [l.strip() for l in text.split("\n")]
    if "Energy Power Supply Position" in text or "Energy Requirement" in text:
        print(month, "is the energy report, not the peak report: skipped")
        return []
    modern = "Demand not Met" in text
    out, used = [], set()

    def label(j):
        """English text of line j if it is a free-standing label line (no numbers, not a header or footnote)."""
        if j < 0 or j >= len(lines) or j in used or ROW.match(lines[j]) or "MW" in lines[j]:
            return ""
        t = english(lines[j])
        if not re.search(r"[A-Za-z]", t) or lines[j].lstrip().startswith(("#", "(#", "*", "(*", "Note", "power", "1.", "2.", "3.")):
            return ""
        return t
    for i, l in enumerate(lines):
        # a number split into a wrapped word, e.g. "Dadra & Nagar Ha6v7e9li 679 0 0.0 688 ..." (2015-02, 2015-03)
        g = re.search(r"([A-Za-z]+)(\d)([a-z])(\d)([a-z])(\d)([a-z]+)\s", l)
        if g:
            l = l.replace(g.group(0), "".join(g.group(i) for i in (1, 3, 5, 7)) + " " + g.group(2) + g.group(4) + g.group(6) + " ")
        m = ROW.match(l)
        if not m or re.search(r"\(\s*MW\s*\)", l):
            continue
        name = english(m.group(1))
        if not re.search(r"[A-Za-z]", name):  # bare number row: label on the line above and/or below
            up = label(i - 1) if lines[i - 1].rstrip().endswith(("/", "-", "&")) or not label(i + 1) else ""
            down = label(i + 1)
            if up and down and not lines[i - 1].rstrip().endswith(("/", "-", "&")):
                up = ""
            used.update(j for j, t in ((i - 1, up), (i + 1, down)) if t)
            name = " ".join(t for t in (up, down) if t)
            name = re.sub(r"- (?=[A-Z])", "- ", name)
        prev = lines[i - 1] if i else ""
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if prev and (i - 1) not in used and re.search(r"[A-Za-z]", english(m.group(1))) and not ROW.match(prev) and (prev.rstrip().endswith(("/", "&")) or english(prev) in ("North-Eastern",)) and len(english(prev)) < 30:
            name = (english(prev) + " " + name).strip()  # label starts on the line above
        if nxt and (i + 1) not in used and not ROW.match(nxt) and english(nxt) in ("Region", "Region*", "Nagar Haveli", "Haveli", "UT of J&K and Ladakh",
                                                            "Dadra & Nagar Haveli and Daman & Diu", "Daman & Diu"):
            name = (name + " " + english(nxt)).strip()  # label ends on the line below
            used.add(i + 1)
        name = FRAG.get(name, name)
        v = [x.replace(",", "") for x in m.group(2).split()]
        if len(v) not in (4, 8):
            raise SystemExit(f"{month}: {len(v)} numbers in {l!r}")
        v = v[:4]
        out.append(dict(month=month, system=name, peak_demand_mw=v[0], peak_met_mw=v[1],
                        surplus_deficit_mw="" if modern else v[2], surplus_deficit_pct="" if modern else v[3],
                        demand_not_met_mw=v[2] if modern else "", demand_not_met_pct=v[3] if modern else ""))
    # Jan-Mar 2017: header reads "Demand not Met" but values keep the old sign (negative = shortage)
    if modern and any(float(r["demand_not_met_mw"]) < 0 for r in out):
        for r in out:
            r["surplus_deficit_mw"], r["surplus_deficit_pct"] = r["demand_not_met_mw"], r["demand_not_met_pct"]
            r["demand_not_met_mw"] = r["demand_not_met_pct"] = ""
    # "Others" appears once per region: name it after the region total that follows it
    for k, r in enumerate(out):
        if r["system"] == "Others":
            reg = next((x["system"] for x in out[k + 1:] if x["system"].endswith("Region")), "")
            r["system"] = f"Others ({reg})"
    return out


def main():
    rows = []
    for f in sorted(glob.glob(f"{RAW}/cea-psp_peak_*.pdf")):
        if Path(f).stat().st_size == 0:
            print("empty file:", f)
            continue
        rows += parse(f)
    df = pd.DataFrame(rows)
    df["system"] = df.system.map(lambda s: re.sub(r"\s+", " ", s.replace("UT of ", "")).strip())
    mark = df.system.str.extract(r"\s*(\(?\*+\)?)$")[0].fillna("")
    df["source_marks"] = ["system:" + m if m else "" for m in mark]
    df["system"] = df.system.str.replace(r"\s*\(?\*+\)?$", "", regex=True)
    df["system"] = df.system.replace({"Andaman Nicobar": "Andaman- Nicobar", "Orissa": "Odisha"})
    df.insert(0, "state_ut", df.system.map(lambda s: STATE.get(canon(s), "")))
    df.insert(1, "year", df.month.str[:4])
    df = df[["state_ut", "system", "year", "month"] + [c for c in df.columns if c not in ("state_ut", "system", "year", "month")]]
    order = [s for s in dict.fromkeys(df.system) if s != "All India"] + ["All India"]  # report order, All India last
    df = df.assign(_o=df.system.map(order.index)).sort_values(["_o", "month"]).drop(columns="_o")
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, df.shape, df.month.nunique(), "months")
    return df


if __name__ == "__main__":
    d = main()
    print(d.system.value_counts().to_string())
