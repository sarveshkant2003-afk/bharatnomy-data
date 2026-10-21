"""Build catalog.js, the index behind index.html (the dataset search page).

Reads every dataset folder (CATEGORY_subject_PERIOD_GEOGRAPHY_SOURCE[_LEVEL]/): the folder name,
its README.md and its CSV. Writes catalog.js in the repo root. Standard library only.
Run after adding or changing a dataset:  python3 tools/build_catalog.py
"""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = re.compile(r"^([A-Z]{3})_([a-z0-9-]+)_([A-Za-z0-9-]+)_([A-Z]{2,6}(?:-[A-Z]{2})*)_([A-Z]+)(?:_(DIST|SDT|VIL|CITY))?$")
PREVIEW_ROWS = 5
csv.field_size_limit(sys.maxsize)


def years_of(period):
    """Start and end calendar year of a PERIOD part: 2023, FY2023-24, 2023-12, 2015-to-2025, 2015-16-to-2024-25."""
    nums = [int(y) for y in re.findall(r"(?<!\d)(\d{4})(?!\d)", period)]
    if not nums:
        return None, None
    return min(nums), max(nums)


def year_start(y):
    m = re.match(r"\s*(\d{4})", y or "")
    return int(m.group(1)) if m else None


def parse_readme(text):
    lines = text.splitlines()
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "")
    sections, cur = {}, "_intro"
    for l in lines:
        if l.startswith("## "):
            cur = l[3:].strip().lower()
            continue
        if l.startswith("# "):
            continue
        sections.setdefault(cur, []).append(l)
    intro = " ".join(l.strip() for l in sections.get("_intro", []) if l.strip()).replace("`", "")
    source = {}
    for l in sections.get("source", []):
        m = re.match(r"-\s+\*\*(.+?):\*\*\s*(.*)", l)
        if m:
            source[m.group(1).strip().lower()] = m.group(2).replace("*", "").strip()
    meanings, other = {}, ""
    for l in sections.get("columns", []):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in ("Column", "---") or set(cells[0]) <= {"-"}:
            continue
        names = re.findall(r"`([^`]+)`", cells[0])
        meaning = cells[1].replace("`", "")
        if names:
            for n in names:
                meanings[n] = meaning
        else:
            other = meaning
    notes = [re.sub(r"^-\s+", "", l.strip()).replace("`", "") for l in sections.get("notes", []) if l.strip().startswith("-")]
    return title, intro, source, meanings, other, notes


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        header = next(r)
        si = header.index("state_ut") if "state_ut" in header else None
        yi = header.index("year") if "year" in header else None
        states, years, preview, n = {}, set(), [], 0
        for row in r:
            n += 1
            if len(preview) < PREVIEW_ROWS:
                preview.append(row)
            if si is not None:
                states[row[si]] = None
            if yi is not None and row[yi]:
                years.add(row[yi])
    return header, n, list(states), sorted(years), preview


def releases():
    """Map dataset folder -> _sources/<release> by the links in each _sources README."""
    out = {}
    for readme in sorted((ROOT / "_sources").glob("*/README.md")):
        for name in re.findall(r"\(\.\./\.\./([^/)]+)/?\)", readme.read_text(encoding="utf-8")):
            out[name] = readme.parent.name
    return out


def main():
    rel = releases()
    catalog, skipped = [], []
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir() and "_" in p.name and not p.name.startswith((".", "_"))):
        m = NAME.match(d.name)
        if not m:
            skipped.append(d.name)
            continue
        cat, subject, period, geo, source, level = m.groups()
        csvs = sorted(d.glob("*.csv"))
        if not csvs:
            skipped.append(d.name)
            continue
        f = d / f"{d.name}.csv" if (d / f"{d.name}.csv").exists() else csvs[0]
        header, rows, states, years, preview = read_csv(f)
        readme = d / "README.md"
        title, intro, src, meanings, other, notes = parse_readme(readme.read_text(encoding="utf-8")) if readme.exists() else ("", "", {}, {}, "", [])
        y0, y1 = years_of(period)
        ys = [y for y in (year_start(y) for y in years) if y]
        if ys:
            y0, y1 = min(ys), max(ys)
        catalog.append({
            "name": d.name, "file": f.name, "category": cat, "subject": subject, "period": period,
            "geo": geo, "source": source, "level": level or "",
            "year_from": y0, "year_to": y1, "years": years,
            "title": title or subject.replace("-", " "), "description": intro,
            "agency": src.get("data", ""), "table": src.get("table taken from", ""),
            "link": src.get("link", ""), "downloaded": src.get("downloaded", ""),
            "release": rel.get(d.name, ""),
            "rows": rows, "columns": [{"name": c, "meaning": meanings.get(c, "")} for c in header],
            "other_columns": other, "notes": notes, "states": states, "preview": preview,
        })
    out = ROOT / "catalog.js"
    body = json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
    out.write_text("// Generated by tools/build_catalog.py. Do not edit by hand.\nwindow.CATALOG = " + body + ";\n", encoding="utf-8")
    print(f"{len(catalog)} datasets -> {out.name} ({out.stat().st_size / 1024:.0f} KB)")
    if skipped:
        print("skipped (name does not follow the SOP or no CSV):", ", ".join(skipped))


if __name__ == "__main__":
    main()
