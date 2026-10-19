"""District-wise forest cover for every state/UT from ISFR 2023 Volume II (Table 10.x.3).

Reads  raw/fsi-isfr_india-state-of-forest-report-vol-2_2023.pdf
Writes fsi-isfr_forest-cover_district_2023.csv
"""
import csv, os, re
import pdfplumber

DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PDF = os.path.join(DIR, "raw", "fsi-isfr_india-state-of-forest-report-vol-2_2023.pdf")
OUT = os.path.join(DIR, "fsi-isfr_forest-cover_district_2023.csv")
COLS = ["geographical_area_sq_km", "very_dense_forest_sq_km", "moderately_dense_forest_sq_km",
        "open_forest_sq_km", "forest_cover_total_sq_km", "forest_cover_pct_of_area",
        "change_since_2021_sq_km", "scrub_sq_km"]
NUM = r"-?[\d,]+(?:\.\d+)?"
ROW = re.compile(rf"^(.*?)\s*((?:{NUM}\s+){{7}}{NUM})$")
TITLE = re.compile(r"^Table 10\.(\d+)\.3 District-?\s?wise Forest Cover in (.+)$", re.I)
FIX = {"Andaman & Nicobar Islands": "Andaman & Nicobar Islands", "Jammu & Kashmir": "Jammu & Kashmir",
       "Dadra & Nagar Haveli and Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu"}


def state_name(s):
    s = re.sub(r"\s+", " ", s.replace(" and ", " & ")).strip()
    s = s.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra & Nagar Haveli and Daman & Diu")
    return {"NCT of Delhi": "Delhi", "Delhi NCT": "Delhi",
            "Dadra & Nagar Haveli": "Dadra & Nagar Haveli and Daman & Diu"}.get(s, s)  # title wraps


def main():
    pdf = pdfplumber.open(PDF)
    lines = []
    for page in pdf.pages:
        lines += (page.extract_text() or "").split("\n")
    out, i = [], 0
    while i < len(lines):
        m = TITLE.match(lines[i].strip())
        if not m or not any(l.strip().startswith("(km") for l in lines[i + 1:i + 3]):
            i += 1  # also skips the list of tables at the front
            continue
        state = state_name(m.group(2))
        i += 1
        frag = []
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith(("Table ", "Figure ")):
                break
            r = ROW.match(line)
            if r:
                name = r.group(1)
                if not name:  # name wrapped around the numbers
                    after = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    name = " ".join(frag + ([after] if after and not ROW.match(after) and not after.startswith(("Total", "*", "Table", "Figure")) else []))
                    if after and name.endswith(after):
                        i += 1
                elif frag and name[:1].islower():
                    name = " ".join(frag + [name])
                frag = []
                vals = [v.replace(",", "") for v in r.group(2).split()]
                marks = []
                if name.startswith("*"):
                    marks.append("district:" + re.match(r"\*+", name).group())
                    name = name.lstrip("*").strip()
                if re.search(r"[a-z]H\b", name):
                    marks.append("district:H")  # hill district
                    name = re.sub(r"(?<=[a-z])H\b", "", name)
                district = "State total" if re.fullmatch(r"(Grand )?Total", name) else name
                out.append([state, district] + vals + ["; ".join(marks)])
                if district == "State total":
                    break
            elif re.search(r"\d", line) or line.startswith(("(km", "2023", "District", "Forest", "Calculated", "Area", "based", "w.r.t", "% of", "SoI", "Raster")):
                frag = []
            else:
                frag.append(line)
            i += 1
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["state_ut", "district"] + COLS + ["source_marks"])
        w.writerows(out)
    print(f"{len(out)} rows, {len({r[0] for r in out})} states -> {OUT}")


if __name__ == "__main__":
    main()
