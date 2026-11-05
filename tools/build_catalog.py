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
    build_registry({c["name"]: c for c in catalog})


# ---------------------------------------------------------------- variable registry

LENS_FIELDS = ["lens_id", "lens_name", "sub_theme_id", "sub_theme_name"]
VAR_FIELDS = ["variable_id", "name", "lens_id", "sub_theme_id", "dataset", "column", "unit", "geo_level",
              "frequency", "earliest_period", "latest_period", "type"]
VAR_TYPES = {"raw", "derived"}


def read_table(path, fields, errors):
    if not path.exists():
        errors.append(f"{path.relative_to(ROOT)}: file is missing")
        return []
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        if r.fieldnames != fields:
            errors.append(f"{path.relative_to(ROOT)}: columns must be {', '.join(fields)} (found {', '.join(r.fieldnames or [])})")
            return []
        return list(r)


def build_registry(datasets):
    """Validate _reference/lenses.csv and _reference/variables.csv, then write registry.json (and registry.js).

    Exits with an error, writing nothing, if a variable points to a dataset folder or column that does not
    exist, or to a lens / sub-theme that is not in lenses.csv.
    """
    ref = ROOT / "_reference"
    errors = []
    lenses = read_table(ref / "lenses.csv", LENS_FIELDS, errors)
    variables = read_table(ref / "variables.csv", VAR_FIELDS, errors)
    sub_themes, lens_names = {}, {}
    for i, r in enumerate(lenses, 2):
        if r["sub_theme_id"] in sub_themes:
            errors.append(f"lenses.csv line {i}: sub-theme {r['sub_theme_id']} appears twice")
        if lens_names.setdefault(r["lens_id"], r["lens_name"]) != r["lens_name"]:
            errors.append(f"lenses.csv line {i}: lens {r['lens_id']} has two names")
        sub_themes[r["sub_theme_id"]] = r
    seen, headers = set(), {}
    for i, v in enumerate(variables, 2):
        where = f"variables.csv line {i} ({v['variable_id'] or 'no id'})"
        for f in VAR_FIELDS:
            if not v[f].strip() and f not in ("earliest_period", "latest_period"):
                errors.append(f"{where}: `{f}` is empty")
        if v["variable_id"] in seen:
            errors.append(f"{where}: variable_id appears twice")
        seen.add(v["variable_id"])
        if v["lens_id"] not in lens_names:
            errors.append(f"{where}: lens `{v['lens_id']}` is not in lenses.csv")
        st = sub_themes.get(v["sub_theme_id"])
        if not st:
            errors.append(f"{where}: sub-theme `{v['sub_theme_id']}` is not in lenses.csv")
        elif st["lens_id"] != v["lens_id"]:
            errors.append(f"{where}: sub-theme {v['sub_theme_id']} belongs to lens {st['lens_id']}, not {v['lens_id']}")
        if v["type"] not in VAR_TYPES:
            errors.append(f"{where}: type must be raw or derived, not `{v['type']}`")
        folder = ROOT / v["dataset"]
        if not folder.is_dir():
            errors.append(f"{where}: dataset folder `{v['dataset']}` does not exist")
            continue
        if v["dataset"] not in headers:
            f = folder / f"{v['dataset']}.csv"
            headers[v["dataset"]] = set(next(csv.reader(open(f, newline="", encoding="utf-8")))) if f.exists() else set()
        if v["column"] not in headers[v["dataset"]]:
            errors.append(f"{where}: column `{v['column']}` is not in {v['dataset']}.csv")
    if errors:
        print(f"\nREGISTRY ERRORS ({len(errors)}); registry.json not written:", file=sys.stderr)
        for e in errors[:200]:
            print("  - " + e, file=sys.stderr)
        if len(errors) > 200:
            print(f"  ... and {len(errors) - 200} more", file=sys.stderr)
        sys.exit(1)

    tree = []
    for r in lenses:
        lens = next((l for l in tree if l["id"] == r["lens_id"]), None)
        if not lens:
            lens = {"id": r["lens_id"], "name": r["lens_name"], "sub_themes": []}
            tree.append(lens)
        lens["sub_themes"].append({"id": r["sub_theme_id"], "name": r["sub_theme_name"]})
    ds = {}
    for name in sorted({v["dataset"] for v in variables}):
        c = datasets.get(name, {})
        ds[name] = {"title": c.get("title", ""), "agency": c.get("agency", ""), "source": c.get("source", ""),
                    "level": c.get("level", ""), "geo": c.get("geo", ""), "link": c.get("link", "")}
    registry = {"lenses": tree, "datasets": ds, "variables": variables}
    body = json.dumps(registry, ensure_ascii=False, separators=(",", ":"))
    (ROOT / "registry.json").write_text(body + "\n", encoding="utf-8")
    (ROOT / "registry.js").write_text("// Generated by tools/build_catalog.py from _reference/. Do not edit by hand.\n"
                                      "window.REGISTRY = " + body + ";\n", encoding="utf-8")
    print(f"{len(variables)} variables, {len(lenses)} sub-themes in {len(tree)} lenses -> registry.json")


if __name__ == "__main__":
    main()
