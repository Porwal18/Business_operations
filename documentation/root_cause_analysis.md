# Root Cause Analysis

## 1. Objective

The objective of this analysis is to identify the operational drivers contributing to SLA breaches, prolonged resolution times, escalations, ticket reopenings, and reduced customer satisfaction.

The analysis evaluates root causes, assignment delays, escalation behavior, reopening patterns, departments, and processes.

---

## 2. Key Findings

### Finding 1 — High Workload is the primary operational driver

High Workload represents the largest root-cause category with 9,302 tickets.

It has:

- Average resolution time: 42.39 hours
- SLA breach rate: 28.70%
- Average CSAT: 3.69

Manual Process is the second-highest risk category with a 26.42% SLA breach rate.

### Finding 2 — Assignment delay increases SLA risk

SLA breach rates increase as assignment delay increases:

| Assignment Delay | SLA Breach Rate |
|---|---:|
| Under 1 Hour | 12.47% |
| 1–3 Hours | 16.54% |
| 3–6 Hours | 30.59% |

Tickets assigned within 3–6 hours have approximately 2.5 times the SLA breach rate of tickets assigned within one hour.

This indicates that reducing assignment latency should be a key process improvement priority.

### Finding 3 — Escalated tickets represent a high-risk population

Escalated tickets show significantly worse operational outcomes:

| Metric | Non-Escalated | Escalated |
|---|---:|---:|
| Avg Resolution | 38.17 hrs | 43.26 hrs |
| SLA Breach | 6.92% | 53.56% |
| Avg CSAT | 3.93 | 3.39 |

Escalated tickets have more than seven times the SLA breach rate of non-escalated tickets.

Escalation should therefore be treated as a high-risk operational indicator.

### Finding 4 — Reopened tickets have poorer outcomes

Tickets reopened multiple times show:

- Average resolution: 41.97 hours
- SLA breach rate: 33.24%
- CSAT: 3.61

Tickets that were not reopened show:

- Average resolution: 38.91 hours
- SLA breach rate: 14.31%
- CSAT: 3.84

This suggests that repeat handling and rework contribute to longer resolution cycles and reduced customer satisfaction.

---

## 3. Highest-Risk Process Areas

### Priority 1 — Order Management / Order Exception Management / High Workload

- Ticket volume: 612
- Average resolution: 52.23 hours
- SLA breach rate: 66.50%
- CSAT: 3.26

This is the highest-risk process/root-cause combination identified in the analysis.

### Priority 2 — Order Management / Order Exception Management / Manual Process

- Ticket volume: 409
- Average resolution: 47.93 hours
- SLA breach rate: 60.39%
- CSAT: 3.31

The high breach rate indicates that manual handling and exception management are major operational constraints.

### Priority 3 — Compliance / Compliance Review / High Workload

- Ticket volume: 562
- Average resolution: 47.52 hours
- SLA breach rate: 57.47%
- CSAT: 3.42

Workload pressure appears to significantly affect compliance review performance.

---

## 4. Root Cause Prioritization

| Root Cause | Priority | Reason |
|---|---|---|
| High Workload | Critical | Highest volume and highest overall breach rate |
| Manual Process | Critical | High breach rate and assignment delay |
| Insufficient Staffing | High | Significant volume and resolution impact |
| System Issue | Medium | Moderate breach rate and resolution impact |
| External Dependency | Medium | High resolution time for breached tickets |
| Process Complexity | Medium | Significant resolution effort |
| Approval Delay | Medium | Contributes to extended resolution |
| Incorrect Information | Low/Medium | Lower overall breach rate |
| Training Gap | Low/Medium | Limited volume but high resolution for breached cases |

---

## 5. Business Impact

The analysis indicates that SLA performance is influenced by multiple operational factors rather than a single issue.

The major business impacts are:

1. Increased SLA breaches
2. Longer ticket resolution cycles
3. Higher escalation volumes
4. Increased ticket rework and reopening
5. Lower customer satisfaction
6. Higher operational workload
7. Reduced process efficiency

---

## 6. Recommended Improvement Areas

### 1. Introduce workload-based ticket routing

Prioritize automatic assignment of tickets based on:

- Current team workload
- Ticket priority
- SLA target
- Process complexity
- Employee capacity

### 2. Reduce manual processing

Identify high-volume manual activities within Order Exception Management and Compliance Review.

Potential improvements include:

- Workflow automation
- Standardized templates
- Rule-based routing
- Automated validation
- Exception queues

### 3. Introduce SLA-risk alerts

Create an early-warning mechanism based on:

- Assignment delay
- Priority
- Remaining SLA time
- Current workload
- Escalation status

### 4. Establish escalation triggers

Escalation should be triggered using defined business rules rather than relying only on manual intervention.

### 5. Reduce ticket reopening

Perform root-cause analysis on reopened tickets and improve:

- First-time resolution
- Resolution validation
- Knowledge documentation
- Quality checks

---

## 7. Business Analyst Recommendation

The analysis suggests that the organization should prioritize improvements in:

**Order Management → Order Exception Management**

with particular focus on:

**High Workload + Manual Processing + Assignment Delay**

The recommended future-state process should introduce workload-based assignment, SLA-risk monitoring, standardized exception handling, and clearer escalation triggers.

---

## 8. Expected Outcomes

The proposed improvements are expected to target:

- Lower SLA breach rate
- Faster assignment
- Reduced resolution time
- Lower escalation volume
- Fewer reopened tickets
- Improved CSAT
- Better workload distribution
- Greater process standardization

---

## 9. Conclusion

The analysis demonstrates that operational performance is driven by the interaction of workload, process design, assignment delays, and exception handling.

The highest-priority improvement opportunity is Order Exception Management, where high workload and manual processing are associated with exceptionally high SLA breach rates and lower CSAT.

The next phase of the project will translate these findings into a GAP Analysis and TO-BE process design.
