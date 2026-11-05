"""Build _reference/geography.csv: one row per state/UT and district, keyed on LGD codes.

Inputs
  _sources/lgd/raw/lgd_states.json, lgd_districts.json, lgd_subdistricts.json   (fetch_lgd.py)
  _sources/orgi-census2011/raw/orgi-census2011_basic-population-subdistrict-town_2011.xlsx
      (Census 2011 codes and names of every state, district and sub-district)
  every dataset CSV in the repo (for the spellings used as aliases)

Outputs
  _reference/geography.csv
  _reference/geography_unmatched.csv  (repo names that could not be matched to an LGD district)

Run from the repo root:  python3 pipelines/lgd/build_geography.py
"""
import glob
import json
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd

RAW = Path("_sources/lgd/raw")
CENSUS = Path("_sources/orgi-census2011/raw/orgi-census2011_basic-population-subdistrict-town_2011.xlsx")
OUT = Path("_reference")

# Official state/UT spellings used in this repo (CLAUDE.md "Place names"), keyed by LGD state code
STATE_NAMES = {
    1: "Jammu & Kashmir", 2: "Himachal Pradesh", 3: "Punjab", 4: "Chandigarh", 5: "Uttarakhand",
    6: "Haryana", 7: "Delhi", 8: "Rajasthan", 9: "Uttar Pradesh", 10: "Bihar", 11: "Sikkim",
    12: "Arunachal Pradesh", 13: "Nagaland", 14: "Manipur", 15: "Mizoram", 16: "Tripura",
    17: "Meghalaya", 18: "Assam", 19: "West Bengal", 20: "Jharkhand", 21: "Odisha",
    22: "Chhattisgarh", 23: "Madhya Pradesh", 24: "Gujarat", 27: "Maharashtra",
    28: "Andhra Pradesh", 29: "Karnataka", 30: "Goa", 31: "Lakshadweep", 32: "Kerala",
    33: "Tamil Nadu", 34: "Puducherry", 35: "Andaman & Nicobar Islands", 36: "Telangana",
    37: "Ladakh", 38: "Dadra & Nagar Haveli and Daman & Diu",
}
STATE_NOTES = {
    1: "Ladakh (Leh, Kargil) was part of the state until 31 Oct 2019; it became a union territory then.",
    28: "Telangana was part of the state until 2 Jun 2014.",
    36: "Formed 2 Jun 2014 from Andhra Pradesh; in Census 2011 its districts are under Andhra Pradesh (state code 28).",
    37: "Formed 31 Oct 2019 from Jammu & Kashmir; in Census 2011 its districts are under Jammu & Kashmir (state code 01).",
    38: "Formed 26 Jan 2020 by merging Dadra & Nagar Haveli and Daman & Diu.",
}
# Old units that no longer exist in LGD; Census 2011 codes from the Census file
OLD_STATES = [
    ("Dadra & Nagar Haveli", "26", "Merged into Dadra & Nagar Haveli and Daman & Diu (LGD 38) on 26 Jan 2020; LGD no longer lists it, so no LGD code."),
    ("Daman & Diu", "25", "Merged into Dadra & Nagar Haveli and Daman & Diu (LGD 38) on 26 Jan 2020; LGD no longer lists it, so no LGD code."),
]

# Spellings in the repo that differ from both the LGD and the Census 2011 name, checked by hand.
# (state_ut, spelling) -> LGD district name. Renames such as Aurangabad -> Chhatrapati Sambhajinagar
# are caught through the Census 2011 name and need no entry here.
# Spellings in the repo that match neither the LGD nor the Census 2011 name, checked by hand against
# the LGD list (each is a respelling or an official rename visible in LGD's Census 2011 name).
# (state_ut, spelling) -> LGD district name. Names like "Prayagraj/ Allahabad" are split on "/" automatically.
# Left unmatched on purpose: Mirpur, Muzaffarbad (not in LGD), East Siang & Siang (two districts combined),
# Shahdara (not in LGD's current Delhi list), Mahe, Yanam (LGD lists only Puducherry and Karaikal).
MANUAL_ALIASES = {
    ('Andhra Pradesh', 'Konaseema'): 'Dr. B.R. Ambedkar Konaseema',
    ('Assam', 'South Salmara- Mankachar'): 'South Salmara Mancachar',
    ('Bihar', 'East Champaran'): 'Purbi Champaran',
    ('Bihar', 'West Champaran'): 'Pashchim Champaran',
    ('Chhattisgarh', 'Balrampur'): 'Balrampur-Ramanujganj',
    ('Chhattisgarh', 'Dantewada'): 'Dakshin Bastar Dantewada',
    ('Chhattisgarh', 'Gariaband'): 'Gariyaband',
    ('Chhattisgarh', 'Kawardha (Kabirdham)'): 'Kabeerdham',
    ('Chhattisgarh', 'Uttar Bastar Kanker (Kanker)'): 'Uttar Bastar Kanker',
    ('Delhi', 'Central Delhi'): 'Central',
    ('Delhi', 'East Delhi'): 'East',
    ('Delhi', 'North Delhi'): 'North',
    ('Delhi', 'North-East Delhi'): 'North East',
    ('Delhi', 'North-West Delhi'): 'North West',
    ('Delhi', 'South Delhi'): 'South',
    ('Delhi', 'South-East Delhi'): 'South East',
    ('Delhi', 'South-West Delhi'): 'South West',
    ('Delhi', 'West Delhi'): 'West',
    ('Gujarat', 'Dang'): 'Dangs',
    ('Haryana', 'Charki Dadri'): 'Charkhi Dadri',
    ('Jammu & Kashmir', 'Bandipura'): 'Bandipora',
    ('Jammu & Kashmir', 'Rajauri'): 'Rajouri',
    ('Jharkhand', 'East Singhbhum'): 'East Singhbum',
    ('Karnataka', 'Bengaluru'): 'Bengaluru Urban',
    ('Karnataka', 'Chamarajanagara'): 'Chamarajanagar',
    ('Karnataka', 'Chikkballapura'): 'Chikkaballapura',
    ('Karnataka', 'Davangere'): 'Davanagere',
    ('Karnataka', 'Vijayanagar'): 'Vijayanagara',
    ('Ladakh', 'Leh'): 'Leh Ladakh',
    ('Madhya Pradesh', 'Narsinghpur'): 'Narsimhapur',
    ('Maharashtra', 'Ahmednagar'): 'Ahilyanagar',
    ('Maharashtra', 'Mumbai City'): 'Mumbai',
    ('Odisha', 'Angul'): 'Anugola',
    ('Odisha', 'Baleswar'): 'Baleshwar',
    ('Odisha', 'Deogarh'): 'Debagada',
    ('Odisha', 'Jagatsinghpur'): 'Jagatsinghapur',
    ('Odisha', 'Sonepur'): 'Subarnapur',
    ('Puducherry', 'Pondicherry'): 'Puducherry',
    ('Rajasthan', 'Shriganga Nagar'): 'Ganganagar',
    ('Sikkim', 'East Sikkim'): 'Gangtok',
    ('Sikkim', 'North Sikkim'): 'Mangan',
    ('Sikkim', 'South Sikkim'): 'Namchi',
    ('Sikkim', 'West Sikkim'): 'Gyalshing',
    ('Tamil Nadu', 'Thoothukudi'): 'Thoothukkudi',
    ('Tamil Nadu', 'Tiruchchirapalli'): 'Tiruchirappalli',
    ('Tamil Nadu', 'Tiruvallur'): 'Thiruvallur',
    ('Telangana', 'Jagtial'): 'Jagitial',
    ('Telangana', 'Jangaon'): 'Jangoan',
    ('Telangana', 'Jayashankar Bhupalpally'): 'Jayashankar Bhupalapally',
    ('Telangana', 'Kumuram Bheem'): 'Kumuram Bheem Asifabad',
    ('Uttar Pradesh', 'Shravasti'): 'Shrawasti',
    ('Uttarakhand', 'Udam Singh Nagar'): 'Udham Singh Nagar',
    ('West Bengal', 'Hoogly'): 'Hooghly',
}
# Not places: totals and labels used as rows in some datasets
NOT_PLACES = {"state total", "all india", "total", "maharashtra_total"}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower().replace("&", "and"))


def load_census():
    c = pd.read_excel(CENSUS, dtype=str, usecols=["State", "District", "Subdistt", "Level", "Name", "TRU"])
    c = c[c.TRU == "Total"]
    states = c[c.Level == "STATE"].set_index("State").Name.str.strip().to_dict()
    dist = c[c.Level == "DISTRICT"].drop_duplicates("District").set_index("District")
    dist_name = dist.Name.str.strip().to_dict()
    dist_state = dist.State.to_dict()
    sub = c[c.Level == "SUB-DISTRICT"].drop_duplicates("Subdistt")
    sub_to_dist = dict(zip(sub.Subdistt, sub.District))
    return states, dist_name, dist_state, sub_to_dist


def census_code(x):
    x = (x or "").strip()
    return "" if x.strip("0") == "" else x


def build():
    states = json.loads((RAW / "lgd_states.json").read_text())
    districts = json.loads((RAW / "lgd_districts.json").read_text())
    subd = json.loads((RAW / "lgd_subdistricts.json").read_text())
    c_states, c_dname, c_dstate, c_sub = load_census()

    rows = []
    for s in sorted(states, key=lambda x: x["stateCode"]):
        sc = s["stateCode"]
        name = STATE_NAMES[sc]
        aliases = {s["stateNameEnglish"].strip()} - {name}
        ccode = census_code(s.get("census2011Code"))
        if ccode and ccode in c_states:
            aliases.add(c_states[ccode].title().replace(" And ", " & "))
        aliases -= {name}
        rows.append(dict(level="state", state_ut=name, lgd_state_code=sc, census2011_state_code=ccode,
                         district="", lgd_district_code="", census2011_district_code="",
                         census2011_name=c_states.get(ccode, ""), aliases=aliases,
                         created_after_2011="yes" if sc in (36, 37, 38) else "",
                         note=STATE_NOTES.get(sc, "")))
        for d in sorted(districts[str(sc)], key=lambda x: x["districtNameEnglish"]):
            dcode = census_code(d.get("census2011Code"))
            note, after = "", ""
            if dcode:
                if dcode not in c_dname:
                    note = f"LGD gives Census 2011 code {dcode}, which is not in the Census 2011 district list."
            else:
                after = "yes"
                parents = defaultdict(list)
                for sd in subd.get(str(d["districtCode"]), []):
                    p = c_sub.get(census_code(sd.get("census2011Code")).zfill(5))
                    if p:
                        parents[p].append(sd["subdistrictNameEnglish"])
                if parents:
                    plist = "; ".join(f"{c_dname[p].title()} (Census 2011 district {p})"
                                      for p in sorted(parents, key=lambda p: -len(parents[p])))
                    note = f"Created after 2011 from: {plist}. Found by mapping its LGD sub-districts to their Census 2011 districts."
                else:
                    note = "Created after 2011. Its LGD sub-districts carry no Census 2011 codes, so the parent district could not be traced."
            rows.append(dict(level="district", state_ut=name, lgd_state_code=sc, census2011_state_code=ccode,
                             district=d["districtNameEnglish"].strip(), lgd_district_code=d["districtCode"],
                             census2011_district_code=dcode, census2011_name=c_dname.get(dcode, ""),
                             aliases=set(), created_after_2011=after, note=note))

    for name, ccode, note in OLD_STATES:
        rows.append(dict(level="state", state_ut=name, lgd_state_code="", census2011_state_code=ccode,
                         district="", lgd_district_code="", census2011_district_code="",
                         census2011_name=c_states.get(ccode, ""), aliases=set(),
                         created_after_2011="", note=note))

    geo = pd.DataFrame(rows)
    # Census 2011 names that differ from the LGD name are aliases
    for i, r in geo[geo.level == "district"].iterrows():
        cn = r.census2011_name.title() if r.census2011_name else ""
        if cn and norm(cn) != norm(r.district):
            geo.at[i, "aliases"].add(cn)

    # Census 2011 districts that LGD no longer lists under any code
    used = set(geo.census2011_district_code)
    for code, cname in c_dname.items():
        if code not in used:
            st = c_dstate[code]
            print(f"Census 2011 district not in LGD: {code} {cname} (state {st})")
            srow = geo[(geo.level == "state") & (geo.census2011_state_code == st)].iloc[0]
            geo.loc[len(geo)] = dict(level="district", state_ut=srow.state_ut, lgd_state_code=srow.lgd_state_code,
                                     census2011_state_code=st, district=cname.title(), lgd_district_code="",
                                     census2011_district_code=code, census2011_name=cname, aliases=set(),
                                     created_after_2011="",
                                     note="Census 2011 district that LGD does not list as a district today, so no LGD district code.")

    unmatched = add_repo_aliases(geo)

    geo["aliases"] = geo.aliases.apply(lambda a: "; ".join(sorted(a)))
    order = {"state": 0, "district": 1}
    geo["_o"] = geo.level.map(order)
    geo = geo.sort_values(["state_ut", "_o", "district"]).drop(columns="_o")
    OUT.mkdir(exist_ok=True)
    geo.to_csv(OUT / "geography.csv", index=False, lineterminator="\n")
    pd.DataFrame(unmatched, columns=["dataset", "state_ut", "district"]).to_csv(
        OUT / "geography_unmatched.csv", index=False, lineterminator="\n")
    print(f"{(geo.level == 'state').sum()} state rows, {(geo.level == 'district').sum()} district rows, "
          f"{len(unmatched)} unmatched repo names")


def match_district(geo_d, state, name, census_code_value=None):
    """Return the index of the LGD district row a repo (state, district) refers to, or None."""
    if census_code_value:
        hit = geo_d[geo_d.census2011_district_code == str(census_code_value).zfill(3)]
        if len(hit) == 1:
            return hit.index[0]
    target = MANUAL_ALIASES.get((state, name))
    pool = geo_d[geo_d.state_ut == state]
    if target:
        hit = pool[pool.district == target]
        return hit.index[0] if len(hit) == 1 else None
    for part in [name] + (name.split("/") if "/" in name else []):
        n = norm(part)
        for col in ("district", "census2011_name"):
            hit = pool[pool[col].map(norm) == n]
            if len(hit) == 1:
                return hit.index[0]
    return None


def add_repo_aliases(geo):
    geo_d = geo[geo.level == "district"]
    unmatched = []
    for f in sorted(glob.glob("*_*/*.csv")):
        if f.startswith("_"):
            continue
        cols = pd.read_csv(f, nrows=0).columns
        if "state_ut" not in cols or "district" not in cols:
            continue
        use = ["state_ut", "district"] + (["district_census_code"] if "district_census_code" in cols else [])
        df = pd.read_csv(f, usecols=use, dtype=str).drop_duplicates()
        for r in df.itertuples(index=False):
            if pd.isna(r.district) or norm(r.district) in {norm(x) for x in NOT_PLACES}:
                continue
            idx = match_district(geo_d, r.state_ut, r.district, getattr(r, "district_census_code", None))
            if idx is None:
                unmatched.append((Path(f).parent.name, r.state_ut, r.district))
            elif r.district != geo.at[idx, "district"]:
                geo.at[idx, "aliases"].add(r.district)
    return sorted(set(unmatched))


if __name__ == "__main__":
    build()
