# National Air Quality Index daily bulletins (CPCB)

Original files for this release. The cleaned data is in:

- [`ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY/`](../../ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY/)

## Source

- **Link:** https://cpcb.nic.in/AQI_Bulletin.php (each day's PDF is at `https://cpcb.nic.in/upload/Downloads/AQI_Bulletin_YYYYMMDD.pdf`)
- **Downloaded:** 28 Oct 2026
- **`raw/`:** not committed (4,193 PDFs, 213 MB).
- `aqi_parse_failures.txt`: bulletin dates with no readable city table (missing days, "server problem" notices)
