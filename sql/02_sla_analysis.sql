-- =========================================================
-- SLA PERFORMANCE ANALYSIS
-- Business Operations Analytics
-- =========================================================

-- ---------------------------------------------------------
-- 1. OVERALL SLA PERFORMANCE
-- ---------------------------------------------------------

SELECT
    COUNT(*) AS total_tickets,

    SUM(
        CASE
            WHEN SLA_Status = 'Met' THEN 1
            ELSE 0
        END
    ) AS sla_met_tickets,

    SUM(
        CASE
            WHEN SLA_Status = 'Breached' THEN 1
            ELSE 0
        END
    ) AS sla_breached_tickets,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN SLA_Status = 'Breached' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS sla_breach_rate_pct

FROM read_csv_auto('data/raw/tickets.csv');


-- ---------------------------------------------------------
-- 2. SLA PERFORMANCE BY DEPARTMENT
-- ---------------------------------------------------------

SELECT
    Department,

    COUNT(*) AS total_tickets,

    ROUND(
        AVG(Resolution_Hours),
        2
    ) AS avg_resolution_hours,

    ROUND(
        100.0 * AVG(
            CASE
                WHEN SLA_Status = 'Breached'
                THEN 1
                ELSE 0
            END
        ),
        2
    ) AS sla_breach_rate_pct,

    ROUND(
        AVG(CSAT_Score),
        2
    ) AS avg_csat

FROM read_csv_auto('data/raw/tickets.csv')

GROUP BY Department

ORDER BY sla_breach_rate_pct DESC;


-- ---------------------------------------------------------
-- 3. SLA PERFORMANCE BY PROCESS
-- ---------------------------------------------------------

SELECT
    Department,
    Process,

    COUNT(*) AS total_tickets,

    ROUND(
        AVG(Resolution_Hours),
        2
    ) AS avg_resolution_hours,

    ROUND(
        100.0 * AVG(
            CASE
                WHEN SLA_Status = 'Breached'
                THEN 1
                ELSE 0
            END
        ),
        2
    ) AS sla_breach_rate_pct,

    ROUND(
        AVG(CSAT_Score),
        2
    ) AS avg_csat

FROM read_csv_auto('data/raw/tickets.csv')

GROUP BY
    Department,
    Process

HAVING COUNT(*) >= 500

ORDER BY sla_breach_rate_pct DESC;


-- ---------------------------------------------------------
-- 4. SLA PERFORMANCE BY PRIORITY
-- ---------------------------------------------------------

SELECT
    Priority,

    COUNT(*) AS total_tickets,

    ROUND(
        AVG(SLA_Hours),
        2
    ) AS target_sla_hours,

    ROUND(
        AVG(Resolution_Hours),
        2
    ) AS avg_resolution_hours,

    ROUND(
        100.0 * AVG(
            CASE
                WHEN SLA_Status = 'Breached'
                THEN 1
                ELSE 0
            END
        ),
        2
    ) AS sla_breach_rate_pct

FROM read_csv_auto('data/raw/tickets.csv')

GROUP BY Priority

ORDER BY
    CASE Priority
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
    END;


-- ---------------------------------------------------------
-- 5. SLA PERFORMANCE BY WORKLOAD
-- ---------------------------------------------------------

SELECT
    Workload_Level,

    COUNT(*) AS total_tickets,

    ROUND(
        AVG(Resolution_Hours),
        2
    ) AS avg_resolution_hours,

    ROUND(
        100.0 * AVG(
            CASE
                WHEN SLA_Status = 'Breached'
                THEN 1
                ELSE 0
            END
        ),
        2
    ) AS sla_breach_rate_pct

FROM read_csv_auto('data/raw/tickets.csv')

GROUP BY Workload_Level

ORDER BY sla_breach_rate_pct DESC;


-- ---------------------------------------------------------
-- 6. WORST PERFORMING PROCESSES
-- ---------------------------------------------------------

SELECT
    Department,
    Process,

    COUNT(*) AS ticket_volume,

    ROUND(
        AVG(Resolution_Hours),
        2
    ) AS avg_resolution_hours,

    ROUND(
        100.0 * AVG(
            CASE
                WHEN SLA_Status = 'Breached'
                THEN 1
                ELSE 0
            END
        ),
        2
    ) AS sla_breach_rate_pct,

    ROUND(
        AVG(CSAT_Score),
        2
    ) AS avg_csat

FROM read_csv_auto('data/raw/tickets.csv')

GROUP BY
    Department,
    Process

HAVING COUNT(*) >= 500

ORDER BY
    sla_breach_rate_pct DESC

LIMIT 10;