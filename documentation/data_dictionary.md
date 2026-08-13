# Data Dictionary

## 1. Purpose

This document defines the business meaning, data type, and analytical purpose of the fields used in the GlobalServe Business Operations Analytics project.

The primary dataset contains 50,000 operational service tickets across 8 departments and 20 business processes.

---

## 2. Ticket Dataset

Source:

`data/raw/tickets.csv`

| Field | Data Type | Business Definition | Example | Analytical Use |
|---|---|---|---|---|
| Ticket_ID | String | Unique identifier assigned to each operational ticket | TKT00001 | Ticket-level tracking |
| Created_Date | DateTime | Date and time when the ticket was created | 2025-07-27 14:36 | Volume and trend analysis |
| Closed_Date | DateTime | Date and time when the ticket was closed | 2025-07-31 11:18 | Resolution analysis |
| Customer_ID | String | Unique identifier of the customer associated with the ticket | CUST0123 | Customer-level analysis |
| Region | String | Geographic region associated with the customer | APAC | Regional performance |
| Country | String | Customer's country | India | Country-level analysis |
| Department | String | Operational department responsible for processing the ticket | Finance Operations | Department performance |
| Process | String | Specific business process handling the ticket | Payment Processing | Process-level performance |
| Category | String | Business category of the request | Payment Issue | Issue classification |
| Priority | String | Business priority assigned to the ticket | High | SLA and workload analysis |
| Assigned_Team | String | Team responsible for processing the ticket | Team A | Team performance |
| Assigned_Employee | String | Employee responsible for the ticket | EMP023 | Employee workload analysis |
| Workload_Level | String | Operational workload level at the time of ticket creation | High | Workload impact analysis |
| Root_Cause | String | Primary reason contributing to the operational issue or delay | Manual Process | Root-cause analysis |
| SLA_Hours | Integer | Target resolution time defined by the ticket priority | 24 | SLA calculation |
| Assignment_Delay_Hours | Decimal | Time taken before the ticket was assigned for processing | 3.5 | Process-delay analysis |
| Resolution_Hours | Decimal | Total time taken to resolve the ticket | 31.5 | Productivity and SLA analysis |
| SLA_Status | String | Indicates whether the ticket was resolved within the defined SLA | Breached | SLA KPI |
| Escalated | String | Indicates whether the ticket was escalated | Yes | Escalation analysis |
| Reopen_Count | Integer | Number of times a ticket was reopened after resolution | 2 | Quality and process analysis |
| CSAT_Score | Integer | Customer satisfaction score associated with the ticket | 4 | Customer experience analysis |
| Status | String | Final operational status of the ticket | Closed | Operational reporting |

---

## 3. Derived Business Metrics

The following metrics can be calculated from the ticket-level data.

### SLA Compliance Rate

Percentage of tickets resolved within the defined SLA.

```text
SLA Compliance Rate =
Tickets Meeting SLA / Total Tickets × 100