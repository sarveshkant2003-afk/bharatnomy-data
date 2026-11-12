#!/bin/sh
# Download Global Wind Atlas (v3, DTU / World Bank, CC BY 4.0) country rasters for India: mean power density and
# mean wind speed at 100 m (250 m grid). No login. About 450 MB.
# Run from the repo root:  sh pipelines/global-wind-atlas/fetch_gwa.sh
R=_sources/global-wind-atlas/raw
mkdir -p "$R"
for layer in power-density wind-speed; do
  f="$R/gwa_IND_${layer}_100m.tif"
  [ -s "$f" ] || curl -sL -m 3600 -o "$f" "https://globalwindatlas.info/api/gis/country/IND/$layer/100"
done
ls -la "$R"
