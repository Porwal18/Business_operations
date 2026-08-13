# Data Quality Report

Automated validation report for the GlobalServe Business Operations Analytics dataset.

## Executive Summary

- **Ticket Records:** 50,000
- **Columns:** 22
- **Quality Checks:** 14
- **Checks Passed:** 14
- **Checks Failed:** 0
- **Data Quality Score:** 100.0%

### Overall Result: PASS

All defined data-quality and business-rule checks passed successfully.

## Validation Results

| Category | Check | Result | Details |
|---|---|---|---|
| Structure | Expected ticket count | **PASS** | Found 50,000 tickets; expected 50,000. |
| Structure | Expected column count | **PASS** | Found 22 columns; expected 22. |
| Completeness | Missing values | **PASS** | Total missing values: 0. |
| Uniqueness | Duplicate Ticket IDs | **PASS** | Duplicate Ticket IDs: 0. |
| Validity | Priority values | **PASS** | Invalid priority values: 0. |
| Validity | SLA Status values | **PASS** | Invalid SLA Status values: 0. |
| Validity | Escalation values | **PASS** | Invalid escalation values: 0. |
| Validity | CSAT score range | **PASS** | Invalid CSAT scores: 0. |
| Validity | Resolution hours | **PASS** | Invalid resolution values: 0. |
| Validity | Reopen count | **PASS** | Negative reopen counts: 0. |
| Business Rules | SLA status calculation | **PASS** | Tickets with incorrect SLA status: 0. |
| Referential Integrity | Customer IDs | **PASS** | Tickets with invalid Customer IDs: 0. |
| Referential Integrity | Employee IDs | **PASS** | Tickets with invalid Employee IDs: 0. |
| Referential Integrity | Department / Process combinations | **PASS** | Invalid department/process combinations: 0. |

## Data Quality Dimensions

The validation framework evaluates the following data-quality dimensions:

1. **Completeness** — mandatory fields contain values.
2. **Uniqueness** — ticket identifiers are unique.
3. **Validity** — values conform to approved business rules.
4. **Referential Integrity** — relationships between tickets and master datasets are valid.
5. **Business Rule Accuracy** — SLA status agrees with the defined SLA calculation.

## Business Significance

Reliable data is required before calculating operational KPIs or making process-improvement recommendations. The automated validation process reduces the risk of drawing conclusions from incomplete, duplicated, invalid, or inconsistent records.