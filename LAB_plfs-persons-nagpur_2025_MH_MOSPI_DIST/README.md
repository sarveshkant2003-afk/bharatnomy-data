# PLFS person records for Nagpur district, January-December 2025

One row per person surveyed in Nagpur district (Maharashtra) by the Periodic Labour Force Survey (PLFS) in calendar year 2025: age, education, training, usual activity (industry, occupation, employer type, job contract, social security), daily activity and earnings in the survey week. This is the survey record itself, not a table of estimates: weight each row by `mult` / 100 before counting or averaging anything.

## Source

- **Data:** National Statistics Office (NSO), Ministry of Statistics and Programme Implementation (MoSPI), Periodic Labour Force Survey, Schedule 10.4, first visit
- **Table taken from:** Unit-level data "Periodic Labour Force Survey (PLFS), Calendar Year 2025 (Jan-Dec25)", person file `cperv12025.csv` (catalog created 27 Mar 2026, last modified 17 Jun 2026), rows with state code 27 and district code 09
- **Link:** https://microdata.gov.in/NADA/index.php/catalog/284 (free login needed to download)
- **Downloaded:** 23 Oct 2026
- **Original file:** not committed (34.6 MB zip, all India). Code books, data layout and questionnaire are in [`_sources/mospi-plfs/raw/docs-2025/`](../_sources/mospi-plfs/raw/docs-2025/)

## Columns

Field names are MoSPI's, from the data layout `mospi-plfs_data-layout-first-visit_2025.xlsx` (sheet "Data Layout", person file). Codes below are from the schedule (`mospi-plfs_schedule-10-4-first-visit_2025-01-to-2025-06.pdf`).

| Column | Meaning |
|---|---|
| `state_ut`, `district` | Maharashtra, Nagpur |
| `month` | Month of survey, `2025-01` to `2025-12` |
| `file_id`, `sch`, `qtr`, `visit` | File code (CFVP5), schedule (104), quarter (Q1-Q4), visit (V1 = first visit) |
| `sec` | Sector: 1 = rural, 2 = urban |
| `state_code`, `district_code` | PLFS codes: 27 = Maharashtra, 09 = Nagpur |
| `nss_reg`, `bstrm`, `strm`, `grp`, `sstrm`, `sro` | NSS region, basic stratum (`D009` = Nagpur district), stratum (201 = Nagpur city stratum in urban), group, sub-stratum, field office sub-region |
| `mfsu`, `sss`, `ssu`, `srl` | Village/urban block (FSU), second-stage stratum, household number, person number. Together with `month` they identify a person |
| `rel`, `sex`, `age`, `marst` | Relation to head; sex (1 male, 2 female, 3 transgender); age in years; marital status (1 never married, 2 married, 3 widowed, 4 divorced/separated) |
| `gedu_lvl` | General education: 01 not literate, 02-04 literate without schooling, 05 below primary, 06 primary, 07 middle, 08 secondary, 10 higher secondary, 11 diploma/certificate, 12 graduate, 13 postgraduate and above |
| `tedu_lvl` ... `voc_cert` | Technical education, years of schooling, current attendance, vocational training (block 4 and 4.1 of the schedule) |
| `pas` | Usual principal activity status: 11 own-account worker, 12 employer, 21 unpaid family helper, 31 regular wage/salaried, 41 casual labour in public works, 51 other casual labour, 81 unemployed, 91 student, 92-93 domestic duties, 94 rentier/pensioner, 95 disabled, 97 others |
| `ind_pas`, `ocu_pas` | Industry (NIC-2008, 5 digits) and occupation (NCO-2015, 3 digits) of the principal activity |
| `loc_pas` | Workplace location (10-19 rural, 20-29 urban, 99 no fixed workplace) |
| `etyp_pas` | Enterprise type: 01 proprietary male, 02 proprietary female, 03-04 partnership, 05 government/local body, 06 public sector enterprise, 07 autonomous body, 08 public/private limited company, 10 co-operative, 11 trust/non-profit, 12 private household as employer, 19 others |
| `wrkr_pas` | Workers in the enterprise: 1 under 6, 2 6-9, 3 10-19, 4 20 and more, 9 not known |
| `job_pas` | Job contract: 1 no written contract, 2 written, up to 1 year, 3 written, 1-3 years, 4 written, over 3 years |
| `leave_pas` | Eligible for paid leave: 1 yes, 2 no |
| `ssec_pas` | Social security: 1 PF/pension only, 2 gratuity only, 3 health care/maternity only, 4 PF/pension + gratuity, 5 PF/pension + health, 6 gratuity + health, 7 all three, 8 none, 9 not known |
| `ecoprd_pas` | Use of the product (own consumption vs sale) |
| `has_sas`, `sas` ... `ecoprd_sas` | Whether the person had a subsidiary activity, and the same fields for it |
| `wrk_365` ... `rea` | Duration of work, job search, unemployment spell, reasons for not working (block 5.3) |
| `das1d`, `ind1d`, `hr1d`, `ern1d_inr` | Daily activity in the survey week for day `d` (7 = day before the survey ... 1 = seventh day back): status (block 6 codes, includes 42 = MGNREG work), industry (NIC 2 digits), hours worked, wage earned in ₹. `das2d` ... `ern2d_inr` are the same for the second activity |
| `hrd`, `ahrd` | Total hours worked and hours available for more work on day `d` |
| `tothrs_wrk`, `totadl_wrk` | Hours worked and hours available for more work in the week |
| `acws`, `aind_cws`, `ocu_cws` | Current weekly status, its industry (NIC 2 digits) and occupation (NCO 3 digits) |
| `ern_reg_inr` | Earnings from regular wage/salaried work in the last calendar month, ₹ |
| `ern_self_inr` | Gross earnings from self-employment in the last 30 days, ₹ |
| `nsc` | Number of FSUs surveyed in the sub-stratum |
| `mult` | Survey weight × 100 (two implied decimals). Final weight = `mult` / 100 |
| `totalsd`, `zst`, `caph`, `smallh`, `panel` | Sub-divisions, size of the basic stratum, households listed and selected in the FSU, panel code |

## Notes

- Sample: 2,593 people in 707 households (rural 1,035 people; urban 1,558, of which 1,018 in the Nagpur city stratum), 170-247 people a month. 1,130 of them are workers by usual principal status. Small breakdowns (single industries, occupations, earnings by group) rest on few cases; check the unweighted count before using one.
- Nagpur is its own basic stratum (`D009`) in both sectors, so district estimates follow MoSPI's design. MoSPI's README for the release says the unit-level data should be used only for employment and unemployment indicators.
- Changes from the original file: rows other than state 27 / district 09 dropped; leading and trailing spaces trimmed; `month` written as `YYYY-MM`; `st`, `dc` renamed `state_code`, `district_code`; `_inr` added to money columns (`ern*`). No values changed.
- Blank cells are blank in the source and mean the question was skipped for that person (e.g. industry for a student). The source gives no reason code, so there is no `source_flag` column.
- The schedule changed in July 2025 (some education and training items asked only before or only after; see the remarks in the data layout). The July-December 2025 instructions are in `docs-2025/`.
- Checks: rows match the raw file (2,593); no duplicate person keys; ages 0-96; weekly hours at most 98; persons per household match `hh_size` in the household file for all 707 households.
