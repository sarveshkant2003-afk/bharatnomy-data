#!/bin/sh
# Download Census 2011 HL-14 (percentage of households by amenities and assets) for the 35 districts of
# Maharashtra from the Census NADA catalog. Catalog ids 9790-9840 hold the HL-14 district files; the
# Maharashtra ones are named HLPCA-27<district code>-2011_H14_census.xlsx.
# Run from the repo root:  sh pipelines/orgi-census2011/fetch_hl14_mh.sh
set -e
OUT=_sources/orgi-census2011/raw/hl14-mh
mkdir -p "$OUT"
for c in $(seq 9790 9840); do
  page=$(curl -sL -m 60 -A "Mozilla/5.0" "https://censusindia.gov.in/nada/index.php/catalog/$c/related-materials")
  name=$(printf '%s' "$page" | grep -oE 'HLPCA-27[0-9]+-2011_H14_census\.xlsx' | head -1)
  [ -z "$name" ] && continue
  dl=$(printf '%s' "$page" | grep -oE "catalog/$c/download/[0-9]+" | head -1)
  dist=$(printf '%s' "$name" | sed -E 's/HLPCA-27([0-9]+)-.*/\1/')
  f="$OUT/orgi-census2011_hl14-district-$dist_2011.xlsx"
  f="$OUT/orgi-census2011_hl14-district-${dist}_2011.xlsx"
  [ -s "$f" ] || curl -sL -m 300 -A "Mozilla/5.0" "https://censusindia.gov.in/nada/index.php/$dl" -o "$f"
  echo "$c $name -> $f"
done
