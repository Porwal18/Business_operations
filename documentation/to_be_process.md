# TO-BE Process Design

## 1. Objective

The objective of the TO-BE process is to improve operational service-request management by reducing assignment delays, SLA breaches, unnecessary escalations, manual processing, and ticket rework.

The proposed future-state process is based on the findings from the SLA, Root Cause, and GAP analyses.

---

# 2. Current-State Problem

The current process has several operational weaknesses:

- Assignment delays increase SLA breach risk.
- High workload contributes to poor SLA performance.
- Manual processes increase resolution time.
- Escalated tickets have significantly higher breach rates.
- Reopened tickets have lower CSAT and higher resolution time.
- Management has limited proactive visibility into SLA risk.

---

# 3. TO-BE Process Overview

The proposed future-state process is:

Customer Request
        |
        v
Ticket Created
        |
        v
Automatic Classification
        |
        v
Priority & SLA Determination
        |
        v
Workload-Based Assignment
        |
        v
SLA Risk Monitoring
        |
        +--------------------+
        |                    |
     Low Risk             High Risk
        |                    |
        v                    v
Normal Processing      Priority Queue
        |                    |
        |                    v
        |              Escalation Trigger
        |                    |
        +---------+----------+
                  |
                  v
            Ticket Resolution
                  |
                  v
          Quality Validation
                  |
            +-----+-----+
            |           |
          Pass         Fail
            |           |
            v           v
          Close       Rework
            |           |
            |           +-----> Resolution
            |
            v
       Customer Feedback
            |
            v
       KPI Monitoring

---

# 4. TO-BE Process Steps

## Step 1 — Ticket Creation

A customer or internal stakeholder submits a service request.

The system captures:

- Ticket ID
- Customer
- Department
- Process
- Request type
- Description
- Creation date
- Region
- Business impact

---

## Step 2 — Automatic Classification

The ticket is automatically classified using predefined business rules.

Classification includes:

- Department
- Process
- Priority
- Root-cause category where applicable
- SLA category

This reduces manual classification effort.

---

## Step 3 — Priority and SLA Determination

The system determines the applicable SLA based on ticket priority.

Example:

| Priority | Target SLA |
|---|---:|
| Critical | 8 hours |
| High | 24 hours |
| Medium | 48 hours |
| Low | 72 hours |

The SLA clock begins when the ticket is created.

---

## Step 4 — Workload-Based Assignment

Tickets are assigned using:

- Employee availability
- Current workload
- Skill/process alignment
- Ticket priority
- SLA remaining time

The assignment engine should prioritize employees with sufficient capacity.

### Business Rule

If the preferred employee/team exceeds the defined workload threshold, the ticket should be routed to the next eligible resource.

---

# 5. SLA Risk Monitoring

The system continuously calculates SLA risk.

### Risk Levels

| Risk | Condition | Action |
|---|---|---|
| Green | More than 50% SLA time remaining | Normal processing |
| Amber | 25–50% SLA time remaining | Team notification |
| Red | Less than 25% SLA time remaining | Priority handling |
| Breached | SLA exceeded | Immediate escalation |

---

# 6. Escalation Framework

Escalation should be rule-based.

### Level 1

Triggered when:

- SLA reaches Red status
- Assignment delay exceeds threshold
- Ticket is Critical priority

Action:

- Notify process owner
- Move ticket to priority queue

### Level 2

Triggered when:

- SLA is breached
- Customer impact is high
- Ticket remains unresolved after Level 1 escalation

Action:

- Notify process manager
- Assign escalation owner
- Create recovery plan

### Level 3

Triggered for:

- Repeated SLA breaches
- High-value customer impact
- Systemic process issues

Action:

- Management review
- Root-cause investigation
- Corrective action plan

---

# 7. Resolution Process

The assigned employee investigates and resolves the request.

The resolution process should use:

- Standard operating procedures
- Knowledge articles
- Process-specific checklists
- Resolution templates
- Required documentation

---

# 8. Closure Quality Gate

Before a ticket can be closed, the system should validate:

1. Customer requirement addressed
2. Resolution completed
3. Required documentation attached
4. Dependencies resolved
5. Resolution notes completed
6. Customer confirmation obtained where applicable

If validation fails, the ticket returns to the resolution stage.

---

# 9. Reopen Prevention

If a customer reopens a ticket, the system should capture the reason.

Possible categories:

- Incorrect resolution
- Incomplete resolution
- Missing information
- New requirement
- Technical issue
- Process issue

Reopen trends should be reviewed monthly.

---

# 10. Root Cause Feedback Loop

Closed tickets should contribute to operational analytics.

The system should track:

- Root cause
- Process
- Department
- SLA status
- Resolution time
- Assignment delay
- Escalation
- Reopen count
- CSAT

This creates a continuous improvement feedback loop.

---

# 11. Business Rules

## BR-01 — Priority

Critical tickets must receive the highest processing priority.

## BR-02 — Assignment

Tickets must be assigned based on workload and process capability.

## BR-03 — SLA Monitoring

Tickets approaching SLA breach must automatically receive increased priority.

## BR-04 — Escalation

Tickets exceeding SLA thresholds must trigger escalation.

## BR-05 — Closure

Tickets cannot be closed unless mandatory resolution information is completed.

## BR-06 — Reopen

Reopened tickets must capture a standardized reopen reason.

## BR-07 — Root Cause

Tickets must contain a root-cause category before final closure where applicable.

---

# 12. Key Performance Indicators

The future-state process should measure:

- SLA breach rate
- Average resolution time
- Average assignment delay
- Escalation rate
- Reopen rate
- First-time resolution rate
- CSAT
- Workload distribution
- Critical-ticket breach rate

---

# 13. Expected Benefits

The TO-BE process is expected to:

- Reduce assignment delays
- Reduce SLA breaches
- Improve workload balancing
- Reduce manual processing
- Reduce unnecessary escalations
- Improve first-time resolution
- Reduce ticket reopening
- Improve CSAT
- Improve management visibility

---

# 14. Business Analyst Deliverables

The TO-BE design will support the following project deliverables:

1. Business Requirements Document
2. Functional Requirements
3. Process Flow
4. Business Rules
5. KPI Framework
6. GAP Analysis
7. UAT Test Cases
8. Operational Dashboard

---

# 15. Conclusion

The proposed TO-BE process introduces a proactive operating model where tickets are automatically classified, intelligently assigned, continuously monitored for SLA risk, escalated using defined rules, and validated before closure.

This approach directly addresses the major gaps identified in the operational analysis and establishes a structured continuous-improvement framework.

