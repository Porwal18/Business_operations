import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

DATA_DIR = Path("data/raw")
OUTPUT_FILE = Path("documentation/data_quality_report.md")

EXPECTED_TICKETS = 50_000
EXPECTED_COLUMNS = 22

VALID_PRIORITIES = {
    "Critical",
    "High",
    "Medium",
    "Low",
}

VALID_SLA_STATUS = {
    "Met",
    "Breached",
}

VALID_ESCALATION = {
    "Yes",
    "No",
}


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

tickets = pd.read_csv(DATA_DIR / "tickets.csv")
customers = pd.read_csv(DATA_DIR / "customers.csv")
employees = pd.read_csv(DATA_DIR / "employees.csv")
processes = pd.read_csv(DATA_DIR / "processes.csv")


# ---------------------------------------------------------
# QUALITY CHECKS
# ---------------------------------------------------------

checks = []


def add_check(category, check, result, details):
    checks.append(
        {
            "Category": category,
            "Check": check,
            "Result": result,
            "Details": details,
        }
    )


# ---------------------------------------------------------
# 1. STRUCTURE
# ---------------------------------------------------------

add_check(
    "Structure",
    "Expected ticket count",
    "PASS" if len(tickets) == EXPECTED_TICKETS else "FAIL",
    f"Found {len(tickets):,} tickets; expected {EXPECTED_TICKETS:,}.",
)

add_check(
    "Structure",
    "Expected column count",
    "PASS" if len(tickets.columns) == EXPECTED_COLUMNS else "FAIL",
    f"Found {len(tickets.columns)} columns; expected {EXPECTED_COLUMNS}.",
)


# ---------------------------------------------------------
# 2. COMPLETENESS
# ---------------------------------------------------------

missing_total = int(tickets.isna().sum().sum())

add_check(
    "Completeness",
    "Missing values",
    "PASS" if missing_total == 0 else "FAIL",
    f"Total missing values: {missing_total:,}.",
)


# ---------------------------------------------------------
# 3. UNIQUENESS
# ---------------------------------------------------------

duplicate_tickets = int(
    tickets["Ticket_ID"].duplicated().sum()
)

add_check(
    "Uniqueness",
    "Duplicate Ticket IDs",
    "PASS" if duplicate_tickets == 0 else "FAIL",
    f"Duplicate Ticket IDs: {duplicate_tickets:,}.",
)


# ---------------------------------------------------------
# 4. VALIDITY
# ---------------------------------------------------------

invalid_priority = int(
    (~tickets["Priority"].isin(VALID_PRIORITIES)).sum()
)

add_check(
    "Validity",
    "Priority values",
    "PASS" if invalid_priority == 0 else "FAIL",
    f"Invalid priority values: {invalid_priority:,}.",
)


invalid_sla = int(
    (~tickets["SLA_Status"].isin(VALID_SLA_STATUS)).sum()
)

add_check(
    "Validity",
    "SLA Status values",
    "PASS" if invalid_sla == 0 else "FAIL",
    f"Invalid SLA Status values: {invalid_sla:,}.",
)


invalid_escalation = int(
    (~tickets["Escalated"].isin(VALID_ESCALATION)).sum()
)

add_check(
    "Validity",
    "Escalation values",
    "PASS" if invalid_escalation == 0 else "FAIL",
    f"Invalid escalation values: {invalid_escalation:,}.",
)


invalid_csat = int(
    (
        (tickets["CSAT_Score"] < 1)
        | (tickets["CSAT_Score"] > 5)
    ).sum()
)

add_check(
    "Validity",
    "CSAT score range",
    "PASS" if invalid_csat == 0 else "FAIL",
    f"Invalid CSAT scores: {invalid_csat:,}.",
)


invalid_resolution = int(
    (tickets["Resolution_Hours"] <= 0).sum()
)

add_check(
    "Validity",
    "Resolution hours",
    "PASS" if invalid_resolution == 0 else "FAIL",
    f"Invalid resolution values: {invalid_resolution:,}.",
)


invalid_reopen = int(
    (tickets["Reopen_Count"] < 0).sum()
)

add_check(
    "Validity",
    "Reopen count",
    "PASS" if invalid_reopen == 0 else "FAIL",
    f"Negative reopen counts: {invalid_reopen:,}.",
)


# ---------------------------------------------------------
# 5. SLA BUSINESS RULE
# ---------------------------------------------------------

expected_sla = (
    tickets["Resolution_Hours"] > tickets["SLA_Hours"]
).map(
    {
        True: "Breached",
        False: "Met",
    }
)

sla_rule_errors = int(
    (tickets["SLA_Status"] != expected_sla).sum()
)

add_check(
    "Business Rules",
    "SLA status calculation",
    "PASS" if sla_rule_errors == 0 else "FAIL",
    f"Tickets with incorrect SLA status: {sla_rule_errors:,}.",
)


# ---------------------------------------------------------
# 6. REFERENTIAL INTEGRITY
# ---------------------------------------------------------

valid_customer_ids = set(customers["Customer_ID"])

invalid_customers = int(
    (~tickets["Customer_ID"].isin(valid_customer_ids)).sum()
)

add_check(
    "Referential Integrity",
    "Customer IDs",
    "PASS" if invalid_customers == 0 else "FAIL",
    f"Tickets with invalid Customer IDs: {invalid_customers:,}.",
)


valid_employee_ids = set(employees["Employee_ID"])

invalid_employees = int(
    (~tickets["Assigned_Employee"].isin(valid_employee_ids)).sum()
)

add_check(
    "Referential Integrity",
    "Employee IDs",
    "PASS" if invalid_employees == 0 else "FAIL",
    f"Tickets with invalid Employee IDs: {invalid_employees:,}.",
)


# ---------------------------------------------------------
# 7. PROCESS INTEGRITY
# ---------------------------------------------------------

valid_process_pairs = set(
    zip(
        processes["Department"],
        processes["Process"],
    )
)

ticket_process_pairs = list(
    zip(
        tickets["Department"],
        tickets["Process"],
    )
)

invalid_processes = sum(
    pair not in valid_process_pairs
    for pair in ticket_process_pairs
)

add_check(
    "Referential Integrity",
    "Department / Process combinations",
    "PASS" if invalid_processes == 0 else "FAIL",
    f"Invalid department/process combinations: {invalid_processes:,}.",
)


# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------

results_df = pd.DataFrame(checks)

total_checks = len(results_df)
passed_checks = int(
    (results_df["Result"] == "PASS").sum()
)
failed_checks = total_checks - passed_checks

quality_score = round(
    passed_checks / total_checks * 100,
    2,
)


# ---------------------------------------------------------
# CREATE MARKDOWN REPORT
# ---------------------------------------------------------

report = []

report.append("# Data Quality Report")
report.append("")
report.append(
    "Automated validation report for the GlobalServe "
    "Business Operations Analytics dataset."
)
report.append("")

report.append("## Executive Summary")
report.append("")

report.append(
    f"- **Ticket Records:** {len(tickets):,}"
)
report.append(
    f"- **Columns:** {len(tickets.columns)}"
)
report.append(
    f"- **Quality Checks:** {total_checks}"
)
report.append(
    f"- **Checks Passed:** {passed_checks}"
)
report.append(
    f"- **Checks Failed:** {failed_checks}"
)
report.append(
    f"- **Data Quality Score:** {quality_score}%"
)
report.append("")

if failed_checks == 0:
    report.append(
        "### Overall Result: PASS"
    )
    report.append("")
    report.append(
        "All defined data-quality and business-rule checks "
        "passed successfully."
    )
else:
    report.append(
        "### Overall Result: REVIEW REQUIRED"
    )
    report.append("")
    report.append(
        "One or more data-quality checks failed and "
        "should be investigated before production use."
    )

report.append("")
report.append("## Validation Results")
report.append("")

report.append(
    "| Category | Check | Result | Details |"
)
report.append(
    "|---|---|---|---|"
)

for _, row in results_df.iterrows():
    report.append(
        f"| {row['Category']} | "
        f"{row['Check']} | "
        f"**{row['Result']}** | "
        f"{row['Details']} |"
    )

report.append("")
report.append("## Data Quality Dimensions")
report.append("")
report.append(
    "The validation framework evaluates the following "
    "data-quality dimensions:"
)
report.append("")
report.append(
    "1. **Completeness** — mandatory fields contain values."
)
report.append(
    "2. **Uniqueness** — ticket identifiers are unique."
)
report.append(
    "3. **Validity** — values conform to approved business rules."
)
report.append(
    "4. **Referential Integrity** — relationships between "
    "tickets and master datasets are valid."
)
report.append(
    "5. **Business Rule Accuracy** — SLA status agrees "
    "with the defined SLA calculation."
)

report.append("")
report.append("## Business Significance")
report.append("")
report.append(
    "Reliable data is required before calculating operational "
    "KPIs or making process-improvement recommendations. "
    "The automated validation process reduces the risk of "
    "drawing conclusions from incomplete, duplicated, invalid, "
    "or inconsistent records."
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE.write_text(
    "\n".join(report),
    encoding="utf-8",
)

print("=" * 60)
print("DATA QUALITY VALIDATION COMPLETE")
print("=" * 60)
print(f"Total checks : {total_checks}")
print(f"Passed       : {passed_checks}")
print(f"Failed       : {failed_checks}")
print(f"Quality score: {quality_score}%")
print(f"\nReport created: {OUTPUT_FILE}")