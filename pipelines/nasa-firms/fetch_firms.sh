#!/bin/sh
# Download NASA FIRMS MODIS active fire detections for India, one CSV per year (2000-2025), from the
# FIRMS country archive (no login needed).
# Run from the repo root:  sh pipelines/nasa-firms/fetch_firms.sh
set -e
OUT=_sources/nasa-firms/raw
mkdir -p "$OUT"
for y in $(seq 2000 2025); do
  f="$OUT/firms_modis-india_$y.csv"
  [ -s "$f.gz" ] && continue
  curl -sfL -m 600 -A "Mozilla/5.0" -o "$f" \
    "https://firms.modaps.eosdis.nasa.gov/data/country/modis/$y/modis_${y}_India.csv"
  gzip -f "$f"
  echo "$y done"
done
