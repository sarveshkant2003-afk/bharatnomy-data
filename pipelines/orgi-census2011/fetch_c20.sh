#!/bin/sh
# Download Census 2011 C-20 (disabled population by type of disability, age and sex) for India and every
# state/UT from the Census NADA catalog. Catalog ids and areas: raw/orgi-census2011_c20-catalog-ids_2011.tsv
# (found with the catalog search "disabled population", 12 Nov 2026).
# Run from the repo root:  sh pipelines/orgi-census2011/fetch_c20.sh
R=_sources/orgi-census2011/raw
OUT=$R/c20
mkdir -p "$OUT"
while IFS="$(printf '\t')" read -r id area; do
  page=$(curl -sL -m 60 -A "Mozilla/5.0" "https://censusindia.gov.in/nada/index.php/catalog/$id/related-materials")
  dl=$(printf '%s' "$page" | grep -oE "catalog/$id/download/[0-9]+" | head -1)
  name=$(printf '%s' "$page" | grep -oE '[A-Za-z0-9_-]+\.(xlsx|xls)' | head -1)
  ext=${name##*.}
  slug=$(printf '%s' "$area" | tr 'A-Z' 'a-z' | sed -E 's/&/and/g; s/[^a-z0-9]+/-/g; s/^-|-$//g')
  f="$OUT/orgi-census2011_c20-$slug_2011.$ext"
  f="$OUT/orgi-census2011_c20-${slug}_2011.${ext:-xlsx}"
  [ -s "$f" ] || curl -sL -m 300 -A "Mozilla/5.0" "https://censusindia.gov.in/nada/index.php/$dl" -o "$f"
  echo "$id $area $name -> $f"
  sleep 0.5
done < "$R/orgi-census2011_c20-catalog-ids_2011.tsv"
