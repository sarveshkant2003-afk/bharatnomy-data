#!/bin/sh
# Download every CWC weekly "Live storage status of important reservoirs" bulletin listed in
# raw/cwc-reservoir-bulletin_file-list.tsv (date as listed, PDF link, title; from the 22 pages of
# https://cwc.gov.in/en/reservoir-level-storage-bulletin, listed 12 Nov 2026).
# Files are saved as raw/pdf/cwc-reservoir-bulletin_<n>_<date>.pdf (n = line number, since a few dates repeat).
# Run from the repo root:  sh pipelines/cwc/fetch_bulletins.sh
R=_sources/cwc-reservoir-bulletin/raw
mkdir -p "$R/pdf"
n=0
while IFS="$(printf '\t')" read -r date url title; do
  n=$((n+1))
  f="$R/pdf/cwc-reservoir-bulletin_$(printf %03d $n)_${date:-nodate}.pdf"
  [ -s "$f" ] || curl -sL -m 300 -o "$f" "$url"
done < "$R/cwc-reservoir-bulletin_file-list.tsv"
ls "$R/pdf" | wc -l
