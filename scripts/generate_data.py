import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

fake = Faker()
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NUM_TICKETS = 50000
NUM_CUSTOMERS = 500
NUM_EMPLOYEES = 100

# ---------------------------------------------------------
# BUSINESS MASTER DATA
# ---------------------------------------------------------

departments = {
    "Finance Operations": [
        "Invoice Processing",
        "Payment Processing",
        "Accounts Reconciliation",
    ],
    "HR Operations": [
        "Employee Records",
        "Payroll Support",
        "Benefits Administration",
    ],
    "IT Support": [
        "Access Management",
        "Hardware Support",
        "Application Support",
    ],
    "Procurement": [
        "Purchase Order Processing",
        "Vendor Management",
    ],
    "Customer Service": [
        "Customer Query",
        "Complaint Management",
        "Account Support",
    ],
    "Data Operations": [
        "Data Validation",
        "Data Maintenance",
        "Reporting Support",
    ],
    "Compliance": [
        "Compliance Review",
        "Documentation Review",
    ],
    "Order Management": [
        "Order Processing",
        "Order Exception Management",
    ],
}

regions = {
    "APAC": ["India", "Singapore", "Australia"],
    "EMEA": ["United Kingdom", "Germany", "France"],
    "North America": ["United States", "Canada"],
    "LATAM": ["Brazil", "Mexico"],
}

priorities = ["Critical", "High", "Medium", "Low"]

categories = [
    "General Query",
    "Payment Issue",
    "Data Issue",
    "Access Issue",
    "Documentation Issue",
    "Processing Delay",
    "System Issue",
    "Customer Complaint",
    "Vendor Issue",
    "Compliance Issue",
]

root_causes = [
    "High Workload",
    "Manual Process",
    "Incorrect Information",
    "System Issue",
    "Insufficient Staffing",
    "Approval Delay",
    "Training Gap",
    "External Dependency",
    "Process Complexity",
    "Other",
]

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def choose_priority():
    return random.choices(
        priorities,
        weights=[5, 20, 45, 30],
        k=1,
    )[0]


def get_sla_hours(priority):
    return {
        "Critical": 8,
        "High": 24,
        "Medium": 48,
        "Low": 72,
    }[priority]


def choose_root_cause(priority, workload_level):
    if workload_level == "High":
        return random.choices(
            root_causes,
            weights=[35, 20, 5, 5, 15, 5, 3, 5, 5, 2],
            k=1,
        )[0]

    if priority in ["Critical", "High"]:
        return random.choices(
            root_causes,
            weights=[15, 15, 8, 15, 12, 10, 5, 8, 10, 2],
            k=1,
        )[0]

    return random.choice(root_causes)


# ---------------------------------------------------------
# CREATE DEPARTMENTS
# ---------------------------------------------------------

department_rows = []

for i, (department, processes) in enumerate(departments.items(), start=1):
    department_rows.append(
        {
            "Department_ID": f"DEPT{i:03d}",
            "Department": department,
            "Number_of_Processes": len(processes),
        }
    )

departments_df = pd.DataFrame(department_rows)

# ---------------------------------------------------------
# CREATE PROCESSES
# ---------------------------------------------------------

process_rows = []
process_counter = 1

for department, process_list in departments.items():
    for process in process_list:
        process_rows.append(
            {
                "Process_ID": f"PROC{process_counter:03d}",
                "Department": department,
                "Process": process,
            }
        )
        process_counter += 1

processes_df = pd.DataFrame(process_rows)

# ---------------------------------------------------------
# CREATE CUSTOMERS
# ---------------------------------------------------------

customer_rows = []

for i in range(1, NUM_CUSTOMERS + 1):
    region = random.choice(list(regions.keys()))
    country = random.choice(regions[region])

    customer_rows.append(
        {
            "Customer_ID": f"CUST{i:04d}",
            "Customer_Name": fake.company(),
            "Industry": random.choice(
                [
                    "Technology",
                    "Healthcare",
                    "Banking",
                    "Retail",
                    "Manufacturing",
                    "Telecommunications",
                    "FMCG",
                    "Professional Services",
                ]
            ),
            "Region": region,
            "Country": country,
            "Customer_Tier": random.choice(
                ["Strategic", "Premium", "Standard"]
            ),
        }
    )

customers_df = pd.DataFrame(customer_rows)

# ---------------------------------------------------------
# CREATE EMPLOYEES
# ---------------------------------------------------------

employee_rows = []
department_list = list(departments.keys())

for i in range(1, NUM_EMPLOYEES + 1):
    department = random.choice(department_list)

    employee_rows.append(
        {
            "Employee_ID": f"EMP{i:03d}",
            "Employee_Name": fake.name(),
            "Department": department,
            "Experience_Years": round(random.uniform(0.5, 12), 1),
            "Team": f"Team {random.choice(['A', 'B', 'C', 'D'])}",
            "Location": random.choice(
                [
                    "India",
                    "United Kingdom",
                    "United States",
                    "Singapore",
                    "Australia",
                ]
            ),
        }
    )

employees_df = pd.DataFrame(employee_rows)

# ---------------------------------------------------------
# GENERATE TICKETS
# ---------------------------------------------------------

ticket_rows = []

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
days_difference = (end_date - start_date).days

process_complexity_factor = {
    "Payment Processing": 1.15,
    "Purchase Order Processing": 1.20,
    "Compliance Review": 1.25,
    "Documentation Review": 1.18,
    "Order Exception Management": 1.30,
    "Application Support": 1.10,
    "Vendor Management": 1.12,
}

for i in range(1, NUM_TICKETS + 1):

    created_date = start_date + timedelta(
        days=random.randint(0, days_difference),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )

    customer = customers_df.iloc[
        random.randint(0, len(customers_df) - 1)
    ]

    department = random.choice(department_list)
    process = random.choice(departments[department])
    priority = choose_priority()
    sla_hours = get_sla_hours(priority)

    month = created_date.month

    if month in [3, 6, 9, 12]:
        workload_level = random.choices(
            ["Low", "Medium", "High"],
            weights=[15, 35, 50],
            k=1,
        )[0]
    else:
        workload_level = random.choices(
            ["Low", "Medium", "High"],
            weights=[30, 50, 20],
            k=1,
        )[0]

    root_cause = choose_root_cause(priority, workload_level)

    base_resolution = {
        "Critical": 5,
        "High": 14,
        "Medium": 28,
        "Low": 45,
    }[priority]

    workload_factor = {
        "Low": 0.85,
        "Medium": 1.00,
        "High": 1.25,
    }[workload_level]

    root_cause_factor = {
        "High Workload": 1.20,
        "Manual Process": 1.15,
        "Incorrect Information": 1.05,
        "System Issue": 1.25,
        "Insufficient Staffing": 1.20,
        "Approval Delay": 1.15,
        "Training Gap": 1.10,
        "External Dependency": 1.20,
        "Process Complexity": 1.15,
        "Other": 1.00,
    }[root_cause]

    variation = np.random.normal(1.0, 0.12)

    resolution_hours = (
        base_resolution
        * workload_factor
        * root_cause_factor
        * variation
    )

    resolution_hours = max(1, round(resolution_hours, 1))

    if root_cause == "Manual Process":
        assignment_delay = round(np.random.uniform(1, 5), 1)
    else:
        assignment_delay = round(np.random.uniform(0.25, 2), 1)

    resolution_hours += assignment_delay

    resolution_hours *= process_complexity_factor.get(process, 1.00)
    resolution_hours = round(resolution_hours, 1)

    sla_status = (
        "Breached"
        if resolution_hours > sla_hours
        else "Met"
    )

    if sla_status == "Breached":
        escalation_probability = 0.65
    elif priority == "Critical":
        escalation_probability = 0.40
    else:
        escalation_probability = 0.10

    escalated = (
        "Yes"
        if random.random() < escalation_probability
        else "No"
    )

    reopen_probability = 0.20 if sla_status == "Breached" else 0.08

    if random.random() < reopen_probability:
        reopen_count = random.randint(1, 3)
    else:
        reopen_count = 0

    if sla_status == "Breached":
        csat = random.choices(
            [1, 2, 3, 4, 5],
            weights=[10, 25, 40, 20, 5],
            k=1,
        )[0]
    else:
        csat = random.choices(
            [1, 2, 3, 4, 5],
            weights=[2, 5, 18, 40, 35],
            k=1,
        )[0]

    if escalated == "Yes" and random.random() < 0.25:
        status = "Escalated"
    elif reopen_count > 0:
        status = "Reopened"
    else:
        status = random.choice(["Resolved", "Closed"])

    department_employees = employees_df[
        employees_df["Department"] == department
    ]

    employee = department_employees.iloc[
        random.randint(0, len(department_employees) - 1)
    ]

    closed_date = created_date + timedelta(hours=resolution_hours)

    ticket_rows.append(
        {
            "Ticket_ID": f"TKT{i:05d}",
            "Created_Date": created_date,
            "Closed_Date": closed_date,
            "Customer_ID": customer["Customer_ID"],
            "Region": customer["Region"],
            "Country": customer["Country"],
            "Department": department,
            "Process": process,
            "Category": random.choice(categories),
            "Priority": priority,
            "Assigned_Team": employee["Team"],
            "Assigned_Employee": employee["Employee_ID"],
            "Workload_Level": workload_level,
            "Root_Cause": root_cause,
            "SLA_Hours": sla_hours,
            "Assignment_Delay_Hours": assignment_delay,
            "Resolution_Hours": resolution_hours,
            "SLA_Status": sla_status,
            "Escalated": escalated,
            "Reopen_Count": reopen_count,
            "CSAT_Score": csat,
            "Status": status,
        }
    )

# ---------------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------------

tickets_df = pd.DataFrame(ticket_rows)

tickets_df["Created_Date"] = pd.to_datetime(tickets_df["Created_Date"])
tickets_df["Closed_Date"] = pd.to_datetime(tickets_df["Closed_Date"])

# ---------------------------------------------------------
# SAVE FILES
# ---------------------------------------------------------

customers_df.to_csv(
    f"{OUTPUT_DIR}/customers.csv",
    index=False,
)

employees_df.to_csv(
    f"{OUTPUT_DIR}/employees.csv",
    index=False,
)

departments_df.to_csv(
    f"{OUTPUT_DIR}/departments.csv",
    index=False,
)

processes_df.to_csv(
    f"{OUTPUT_DIR}/processes.csv",
    index=False,
)

tickets_df.to_csv(
    f"{OUTPUT_DIR}/tickets.csv",
    index=False,
)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("GLOBAL SERVE DATA GENERATION COMPLETE")
print("=" * 60)

print(f"\nCustomers   : {len(customers_df):,}")
print(f"Employees   : {len(employees_df):,}")
print(f"Departments : {len(departments_df):,}")
print(f"Processes   : {len(processes_df):,}")
print(f"Tickets     : {len(tickets_df):,}")

print("\nSLA Performance:")
print(
    tickets_df["SLA_Status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nAverage Resolution Hours:")
print(round(tickets_df["Resolution_Hours"].mean(), 2))

print("\nAverage CSAT:")
print(round(tickets_df["CSAT_Score"].mean(), 2))

print("\nFiles created in:")
print(OUTPUT_DIR)

print("=" * 60)