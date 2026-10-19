"""Position-based reader for the tables in Land Use Statistics at a Glance (PDF).

Each table page has a row of column numbers "(1) (2) ...". Every number on the
page is assigned to the column whose number sits above it, so blank cells stay
blank instead of shifting values left.
"""
import re
import pdfplumber

MARK = re.compile(r"\((\d+)\)")
YEAR = re.compile(r"^(\d{4}-\d{2})(\(p\))?(\*?)$")


def lines(words, tol=4):
    """Group words into rows. Some cells sit ~2pt above their row (Table 9), so a word
    joins the current row when it is within tol of the row's lowest word."""
    rows = []
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if rows and w["top"] - max(x["top"] for x in rows[-1]) <= tol:
            rows[-1].append(w)
        else:
            rows.append([w])
    return [sorted(r, key=lambda w: w["x0"]) for r in rows]


def header_marks(rows):
    """The row of "(1) (2) ..." column numbers: the line where most words are marks."""
    best = bestrow = None
    for r in rows:
        m = [w for w in r if MARK.fullmatch(w["text"])]
        if len(m) >= 3 and len(m) >= 0.8 * len(r) and (best is None or len(m) > len(best)):
            best, bestrow = m, r
    if best is None:
        return None
    # A mark can be printed overlapping other text, e.g. "A(1r2e)a" for "(12)" in
    # Table 2. Recover it when its digits give the next column number.
    for w in bestrow:
        if w in best:
            continue
        digits = re.sub(r"\D", "", w["text"])
        last = max(int(MARK.fullmatch(b["text"]).group(1)) for b in best)
        if "(" in w["text"] and digits and int(digits) == last + 1:
            best.append({**w, "text": f"({digits})"})
    return sorted(best, key=lambda w: w["x0"])


def page_table(page):
    """Return (title, marks, header_rows, body_rows) for one page."""
    words = page.extract_words(keep_blank_chars=False, use_text_flow=False)
    rows = lines(words)
    marks = header_marks(rows)
    if not marks:
        return None
    mtop = marks[0]["top"]
    title = next((" ".join(w["text"] for w in r) for r in rows if r[0]["text"] == "TABLE"), "")
    head = [r for r in rows if r[0]["top"] < mtop - 2]
    body = [r for r in rows if r[0]["top"] > mtop + 2]
    return title, marks, head, body


def assign(row, marks):
    """Map each word in a row to a column number.

    Numbers are right-aligned and sit to the right of their "(n)" mark, never as far
    as the next mark: a word belongs to column n when its right edge lies between
    mark n's right edge and mark n+1's.
    """
    edges = [(m["x1"], int(MARK.fullmatch(m["text"]).group(1))) for m in marks]
    bounds = []
    for i, (x1, n) in enumerate(edges):
        lo = x1 - 3 if i else -1e9
        hi = edges[i + 1][0] - 3 if i + 1 < len(edges) else 1e9
        bounds.append((lo, hi, n))
    out = {}
    for w in row:
        x = w["x1"]
        for lo, hi, n in bounds:
            if lo <= x < hi:
                out[n] = (out[n] + " " + w["text"]) if n in out else w["text"]
                break
    return out
