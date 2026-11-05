# PLFS household records for Nagpur district, January-December 2025

One row per household surveyed in Nagpur district (Maharashtra) by the Periodic Labour Force Survey (PLFS) in calendar year 2025: size, type, religion, social group, monthly consumer expenditure, land and unearned income. Join to the person file [`LAB_plfs-persons-nagpur_2025_MH_MOSPI_DIST`](../LAB_plfs-persons-nagpur_2025_MH_MOSPI_DIST/) on `month`, `mfsu`, `sss`, `ssu`. Weight each row by `mult` / 100.

## Source

- **Data:** National Statistics Office (NSO), Ministry of Statistics and Programme Implementation (MoSPI), Periodic Labour Force Survey, Schedule 10.4, first visit
- **Table taken from:** Unit-level data "Periodic Labour Force Survey (PLFS), Calendar Year 2025 (Jan-Dec25)", household file `chhv12025.csv` (catalog created 27 Mar 2026, last modified 17 Jun 2026), rows with state code 27 and district code 09
- **Link:** https://microdata.gov.in/NADA/index.php/catalog/284 (free login needed to download)
- **Downloaded:** 23 Oct 2026
- **Original file:** not committed (34.6 MB zip, all India). Code books, data layout and questionnaire are in [`_sources/mospi-plfs/raw/docs-2025/`](../_sources/mospi-plfs/raw/docs-2025/)

## Columns

Field names are MoSPI's, from the data layout `mospi-plfs_data-layout-first-visit_2025.xlsx` (household file).

| Column | Meaning |
|---|---|
| `state_ut`, `district` | Maharashtra, Nagpur |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `lgd_district_code` | District code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for totals and names that could not be matched |
| `month` | Month of survey, `2025-01` to `2025-12` |
| `file_id`, `sch`, `qtr`, `visit` | File code (CFVH5), schedule (104), quarter, visit (V1) |
| `sec` | Sector: 1 = rural, 2 = urban |
| `state_code`, `district_code` | PLFS codes: 27 = Maharashtra, 09 = Nagpur |
| `nss_reg`, `bstrm`, `strm`, `grp`, `sstrm`, `sro` | NSS region, basic stratum (`D009`), stratum, group, sub-stratum, field office sub-region |
| `mfsu`, `sss`, `ssu` | Village/urban block (FSU), second-stage stratum, household number |
| `smonth`, `resp_code`, `svc`, `rea_sub` | Month of survey (as number), informant's response, survey code, reason for substituting the household |
| `hh_size` | Household size, persons |
| `hhtype` | Household type. Rural: 1 self-employed in agriculture, 2 self-employed in non-agriculture, 3 regular wage/salary, 4 casual labour in agriculture, 5 casual labour in non-agriculture, 9 others. Urban: 1 self-employed, 2 regular wage/salary, 3 casual labour, 9 others |
| `relg` | Religion: 1 Hinduism, 2 Islam, 3 Christianity, 4 Sikhism, 5 Jainism, 6 Buddhism, 7 Zoroastrianism, 9 others |
| `sg` | Social group: 1 ST, 2 SC, 3 OBC, 9 others |
| `hce1_inr` ... `hce3_inr` | Usual monthly consumer expenditure on purchases, home-grown stock, and wages in kind/free items, ₹ |
| `hce4_inr`, `hce5_inr` | Annual expenditure on clothing/footwear etc. and on durables, ₹ |
| `hce_tot_inr` | Usual monthly consumer expenditure, ₹ (= items 5.1 + 5.2 + 5.3 + (5.4 + 5.5) / 12) |
| `lposs`, `llease` | Land possessed and land leased out (area class codes, see schedule block 3) |
| `rent_inr`, `interest_inr`, `pension_inr`, `remit_inr`, `inc_tot_inr` | Usual monthly rent, interest, pension, remittances received and their total, ₹ |
| `inf_srl`, `sur_date`, `sur_time` | Informant's person number, survey date (DDMMYYYY), minutes taken |
| `nsc`, `mult`, `totalsd`, `zst`, `caph`, `smallh`, `panel` | FSUs surveyed in the sub-stratum; weight × 100; sub-divisions; stratum size; households listed and selected; panel code |

## Notes

- 707 households: rural 276, urban 431 (287 in the Nagpur city stratum).
- Changes from the original file: rows other than state 27 / district 09 dropped; whole numbers that the source CSV writes as `4.0` written as `4`; `month` written as `YYYY-MM`; `st`, `dc` renamed `state_code`, `district_code`; `_inr` added to money columns. No values changed.
- Blank cells are blank in the source (e.g. `rea_sub` when the household was not a substitute). The source gives no reason code.
- Checks: `inc_tot_inr` equals the sum of its four parts in all 707 households; `hce_tot_inr` equals its formula within ₹1 (rounding) in all households; no duplicate household keys.
- `lgd_state_code` and `lgd_district_code` added on 5 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
