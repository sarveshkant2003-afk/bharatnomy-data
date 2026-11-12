#!/bin/sh
# Download JRC GHSL built-up surface grids (GHS-BUILT-S R2023A, WGS84, 30 arc-seconds), total and non-residential,
# epochs 1975-2030, and keep only the GeoTIFF. No login. About 4 GB of zips; the zips are deleted after unzipping.
# Run from the repo root:  sh pipelines/jrc-ghsl/fetch_ghsl.sh
set -e
R=_sources/jrc-ghsl/raw
mkdir -p "$R"
B=https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_S_GLOBE_R2023A
for kind in BUILT_S BUILT_S_NRES; do
  for e in 1975 1980 1985 1990 1995 2000 2005 2010 2015 2020 2025 2030; do
    n=GHS_${kind}_E${e}_GLOBE_R2023A_4326_30ss
    [ -s "$R/${n}_V1_0.tif" ] && continue
    curl -sL -m 1800 -o "$R/$n.zip" "$B/$n/V1-0/${n}_V1_0.zip"
    unzip -o -q "$R/$n.zip" "*.tif" -d "$R"
    rm "$R/$n.zip"
  done
done
ls "$R"/*.tif | wc -l
