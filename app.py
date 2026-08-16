import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PLOTLY STYLE HELPERS
# ============================================================

def polish_chart(fig, height=430, left=90, right=90, bottom=70):
    """Consistent chart sizing, spacing and readable labels."""
    fig.update_layout(
        height=height,
        margin=dict(l=left, r=right, t=70, b=bottom),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(x=0, xanchor="left", font=dict(size=18)),
        hoverlabel=dict(font_size=13),
    )
    fig.update_xaxes(automargin=True, showgrid=True, gridcolor="rgba(255,255,255,0.12)")
    fig.update_yaxes(automargin=True, showgrid=False)
    return fig


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Business Operations Analytics",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    tickets = pd.read_csv("data/raw/tickets.csv")

    # Convert dates if available
    for col in ["Created_Date", "Closed_Date"]:
        if col in tickets.columns:
            tickets[col] = pd.to_datetime(tickets[col], errors="coerce")

    return tickets


df = load_data()

# ============================================================
# TITLE
# ============================================================

st.title("📊 Business Operations Analytics Platform")
st.caption(
    "Operational performance, SLA risk, root-cause analysis and process improvement insights"
)

st.caption(
    "Use the sidebar to filter the analysis by department, priority, SLA status, root cause and created-date range."
)

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")

filtered = df.copy()

if "Department" in df.columns:
    departments = sorted(df["Department"].dropna().unique())
    selected_departments = st.sidebar.multiselect(
        "Department",
        departments,
        default=departments
    )
    filtered = filtered[
        filtered["Department"].isin(selected_departments)
    ]

if "Priority" in df.columns:
    priorities = sorted(df["Priority"].dropna().unique())
    selected_priorities = st.sidebar.multiselect(
        "Priority",
        priorities,
        default=priorities
    )
    filtered = filtered[
        filtered["Priority"].isin(selected_priorities)
    ]

if "SLA_Status" in df.columns:
    sla_options = sorted(df["SLA_Status"].dropna().unique())
    selected_sla = st.sidebar.multiselect(
        "SLA Status",
        sla_options,
        default=sla_options
    )
    filtered = filtered[
        filtered["SLA_Status"].isin(selected_sla)
    ]

if "Root_Cause" in df.columns:
    root_causes = sorted(df["Root_Cause"].dropna().unique())
    selected_root_causes = st.sidebar.multiselect(
        "Root Cause",
        root_causes,
        default=root_causes
    )
    filtered = filtered[
        filtered["Root_Cause"].isin(selected_root_causes)
    ]


# ============================================================
# DATE RANGE FILTER
# ============================================================

# Keep the filtered population before the date restriction. This lets us compare
# the selected period with the immediately preceding period using the same
# Department / Priority / SLA / Root Cause filters.
filter_base = filtered.copy()
selected_start_date = None
selected_end_date = None

if "Created_Date" in df.columns:
    st.sidebar.divider()
    st.sidebar.subheader("📅 Date Range")

    valid_dates = df["Created_Date"].dropna()

    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        selected_dates = st.sidebar.date_input(
            "Created Date",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            start_date, end_date = selected_dates
            selected_start_date = start_date
            selected_end_date = end_date

            filtered = filtered[
                filtered["Created_Date"].dt.date.between(
                    start_date,
                    end_date
                )
            ]

st.sidebar.divider()
st.sidebar.metric("Filtered Tickets", f"{len(filtered):,}")
st.sidebar.metric("Total Dataset", f"{len(df):,}")

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_tickets = len(filtered)

if total_tickets > 0:

    if "SLA_Status" in filtered.columns:
        sla_breach_rate = (
            filtered["SLA_Status"]
            .eq("Breached")
            .mean()
            * 100
        )
        sla_met_rate = 100 - sla_breach_rate
    else:
        sla_breach_rate = 0
        sla_met_rate = 0

    avg_resolution = (
        filtered["Resolution_Hours"].mean()
        if "Resolution_Hours" in filtered.columns
        else 0
    )

    avg_csat = (
        filtered["CSAT_Score"].mean()
        if "CSAT_Score" in filtered.columns
        else 0
    )

    escalated_rate = (
        filtered["Escalated"].eq("Yes").mean() * 100
        if "Escalated" in filtered.columns
        else 0
    )

else:
    sla_breach_rate = 0
    sla_met_rate = 0
    avg_resolution = 0
    avg_csat = 0
    escalated_rate = 0

# ============================================================
# EXECUTIVE KPI CARDS
# ============================================================

st.subheader("Executive Overview")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Tickets",
    f"{total_tickets:,}"
)

c2.metric(
    "SLA Met",
    f"{sla_met_rate:.2f}%"
)

c3.metric(
    "SLA Breach",
    f"{sla_breach_rate:.2f}%"
)

c4.metric(
    "Avg Resolution (hrs)",
    f"{avg_resolution:.2f} hrs"
)

c5.metric(
    "Avg CSAT",
    f"{avg_csat:.2f}/5"
)

# ============================================================
# KPI PERIOD COMPARISON
# ============================================================

if (
    selected_start_date is not None
    and selected_end_date is not None
    and "Created_Date" in filter_base.columns
):
    period_days = (selected_end_date - selected_start_date).days + 1
    previous_end_date = selected_start_date - pd.Timedelta(days=1)
    previous_start_date = previous_end_date - pd.Timedelta(days=period_days - 1)

    previous_filtered = filter_base[
        filter_base["Created_Date"].dt.date.between(
            previous_start_date,
            previous_end_date
        )
    ]

    def calculate_kpis(data):
        if data.empty:
            return {
                "tickets": 0,
                "breach": None,
                "resolution": None,
                "csat": None,
            }

        breach = (
            data["SLA_Status"].eq("Breached").mean() * 100
            if "SLA_Status" in data.columns else None
        )
        resolution = (
            data["Resolution_Hours"].mean()
            if "Resolution_Hours" in data.columns else None
        )
        csat = (
            data["CSAT_Score"].mean()
            if "CSAT_Score" in data.columns else None
        )

        return {
            "tickets": len(data),
            "breach": breach,
            "resolution": resolution,
            "csat": csat,
        }

    current_kpis = calculate_kpis(filtered)
    previous_kpis = calculate_kpis(previous_filtered)

    st.subheader("📈 Period-over-Period Performance")
    st.caption(
        f"Current: {selected_start_date} to {selected_end_date}  |  "
        f"Previous: {previous_start_date} to {previous_end_date}"
    )

    def delta_value(current, previous, suffix="", inverse=False, decimals=2):
        if current is None or previous is None or previous == 0:
            return None
        change = current - previous
        # Streamlit colors negative deltas red by default. For breach rate and
        # resolution time, a decrease is operationally positive.
        if inverse:
            return f"{change:+.{decimals}f}{suffix}"
        return f"{change:+.{decimals}f}{suffix}"

    pc1, pc2, pc3, pc4 = st.columns(4)

    pc1.metric(
        "Tickets",
        f"{current_kpis['tickets']:,}",
        delta=(
            current_kpis['tickets'] - previous_kpis['tickets']
            if previous_kpis['tickets'] else None
        ),
    )

    pc2.metric(
        "SLA Breach",
        f"{current_kpis['breach']:.2f}%" if current_kpis['breach'] is not None else "N/A",
        delta=delta_value(current_kpis['breach'], previous_kpis['breach'], "%")
        if current_kpis['breach'] is not None and previous_kpis['breach'] is not None
        else None,
        delta_color="inverse",
    )

    pc3.metric(
        "Avg Resolution",
        f"{current_kpis['resolution']:.2f} hrs" if current_kpis['resolution'] is not None else "N/A",
        delta=delta_value(current_kpis['resolution'], previous_kpis['resolution'], " hrs")
        if current_kpis['resolution'] is not None and previous_kpis['resolution'] is not None
        else None,
        delta_color="inverse",
    )

    pc4.metric(
        "Avg CSAT",
        f"{current_kpis['csat']:.2f}/5" if current_kpis['csat'] is not None else "N/A",
        delta=delta_value(current_kpis['csat'], previous_kpis['csat'])
        if current_kpis['csat'] is not None and previous_kpis['csat'] is not None
        else None,
    )

    if previous_filtered.empty:
        st.info("ℹ️ No tickets were found in the immediately preceding comparison period.")
    else:
        if current_kpis["breach"] is not None and previous_kpis["breach"] is not None:
            breach_change = current_kpis["breach"] - previous_kpis["breach"]
            if breach_change < 0:
                st.success(
                    f"📉 **SLA improvement:** breach rate decreased by "
                    f"{abs(breach_change):.2f} percentage points versus the previous period."
                )
            elif breach_change > 0:
                st.warning(
                    f"📈 **SLA deterioration:** breach rate increased by "
                    f"{breach_change:.2f} percentage points versus the previous period."
                )
            else:
                st.info("➡️ **SLA stable:** breach rate is unchanged versus the previous period.")

# ============================================================
# PERFORMANCE TREND ANALYSIS
# ============================================================

if not filtered.empty and "Created_Date" in filtered.columns:
    st.subheader("📊 Performance Trends")

    trend_df = filtered.dropna(subset=["Created_Date"]).copy()
    trend_days = (
        (selected_end_date - selected_start_date).days + 1
        if selected_start_date is not None and selected_end_date is not None
        else 0
    )

    if trend_days <= 31:
        trend_df["Trend_Period"] = trend_df["Created_Date"].dt.floor("D")
        period_label = "Daily"
    elif trend_days <= 180:
        trend_df["Trend_Period"] = trend_df["Created_Date"].dt.to_period("W").dt.start_time
        period_label = "Weekly"
    else:
        trend_df["Trend_Period"] = trend_df["Created_Date"].dt.to_period("M").dt.start_time
        period_label = "Monthly"

    trend_agg = (
        trend_df.groupby("Trend_Period")
        .agg(
            Tickets=("Trend_Period", "size"),
            SLA_Breach_Rate=(
                "SLA_Status",
                lambda x: (x == "Breached").mean() * 100
            ) if "SLA_Status" in trend_df.columns else ("Trend_Period", "size"),
            Avg_Resolution=(
                "Resolution_Hours", "mean"
            ) if "Resolution_Hours" in trend_df.columns else ("Trend_Period", "size"),
            Avg_CSAT=(
                "CSAT_Score", "mean"
            ) if "CSAT_Score" in trend_df.columns else ("Trend_Period", "size"),
        )
        .reset_index()
        .sort_values("Trend_Period")
    )

    trend_agg["SLA_Breach_Rate"] = trend_agg["SLA_Breach_Rate"].round(2)
    trend_agg["Avg_Resolution"] = trend_agg["Avg_Resolution"].round(2)
    trend_agg["Avg_CSAT"] = trend_agg["Avg_CSAT"].round(2)

    t1, t2 = st.columns(2)

    with t1:
        fig = px.line(
            trend_agg,
            x="Trend_Period",
            y="SLA_Breach_Rate",
            markers=True,
            text="SLA_Breach_Rate",
            title=f"SLA Breach Rate — {period_label}",
        )
        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="top center",
            cliponaxis=False,
        )
        fig.update_yaxes(title="SLA Breach Rate (%)")
        fig.update_xaxes(title=period_label)
        polish_chart(fig, height=430, left=80, right=70)
        st.plotly_chart(fig, width="stretch")

    with t2:
        fig = px.line(
            trend_agg,
            x="Trend_Period",
            y="Avg_Resolution",
            markers=True,
            text="Avg_Resolution",
            title=f"Average Resolution Time — {period_label}",
        )
        fig.update_traces(
            texttemplate="%{text:.2f} hrs",
            textposition="top center",
            cliponaxis=False,
        )
        fig.update_yaxes(title="Average Resolution (hrs)")
        fig.update_xaxes(title=period_label)
        polish_chart(fig, height=430, left=80, right=70)
        st.plotly_chart(fig, width="stretch")

    fig = px.bar(
        trend_agg,
        x="Trend_Period",
        y="Tickets",
        text="Tickets",
        title=f"Ticket Volume — {period_label}",
    )
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
    )
    fig.update_yaxes(title="Tickets")
    fig.update_xaxes(title=period_label)
    polish_chart(fig, height=400, left=70, right=70)
    st.plotly_chart(fig, width="stretch")

st.divider()

# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.subheader("💡 Key Business Insights")

insight_cols = st.columns(3)

# Highest breach department
if "Department" in filtered.columns and "SLA_Status" in filtered.columns:
    dept_breach = (
        filtered.groupby("Department")
        .agg(
            Tickets=("SLA_Status", "size"),
            Breach_Rate=(
                "SLA_Status",
                lambda x: (x == "Breached").mean() * 100
            )
        )
        .sort_values("Breach_Rate", ascending=False)
    )

    if len(dept_breach) > 0:
        worst_dept = dept_breach.index[0]
        worst_dept_rate = dept_breach.iloc[0]["Breach_Rate"]

        insight_cols[0].warning(
            f"🚨 **Highest SLA Risk**\n\n"
            f"{worst_dept} has the highest breach rate "
            f"at **{worst_dept_rate:.2f}%**."
        )

# Highest root cause
if "Root_Cause" in filtered.columns:

    root_counts = filtered["Root_Cause"].value_counts()

    if len(root_counts) > 0:

        max_root_count = root_counts.max()

        top_roots = root_counts[
            root_counts == max_root_count
        ].index.tolist()

        top_root_text = ", ".join(top_roots)

        insight_cols[1].info(
            f"🔎 **Top Root Cause**\n\n"
            f"**{top_root_text}** accounts for "
            f"**{max_root_count:,} tickets**."
        )

    else:

        insight_cols[1].info(
            "🔎 **Top Root Cause**\n\n"
            "No root-cause data is available for the current filters."
        )

# Escalation
insight_cols[2].success(
    f"📈 **Escalation Rate**\n\n"
    f"Approximately **{escalated_rate:.2f}%** "
    f"of filtered tickets were escalated."
)

# ============================================================
# SLA PERFORMANCE
# ============================================================

st.header("🚨 SLA Performance")

col1, col2 = st.columns(2)

with col1:

    if "SLA_Status" in filtered.columns:

        sla_counts = (
            filtered["SLA_Status"]
            .value_counts()
            .reset_index()
        )

        sla_counts.columns = ["SLA_Status", "Tickets"]

        fig = px.pie(
            sla_counts,
            names="SLA_Status",
            values="Tickets",
            hole=0.55,
            title="SLA Compliance"
        )

        fig.update_traces(
            textinfo="percent",
            texttemplate="%{percent:.1%}",
            hovertemplate="%{label}: %{value:,} tickets (%{percent:.2%})<extra></extra>",
        )
        fig.update_layout(
            legend_title="SLA Status",
            height=430,
            margin=dict(l=20, r=20, t=70, b=20),
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

with col2:

    if "Priority" in filtered.columns and "SLA_Status" in filtered.columns:

        priority_sla = (
            filtered.groupby("Priority")
            .agg(
                Tickets=("SLA_Status", "size"),
                Breach_Rate=(
                    "SLA_Status",
                    lambda x: (x == "Breached").mean() * 100
                )
            )
            .reset_index()
        )

        fig = px.bar(
            priority_sla,
            x="Priority",
            y="Breach_Rate",
            text="Breach_Rate",
            title="SLA Breach Rate by Priority"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            cliponaxis=False,
        )
        fig.update_yaxes(title="SLA Breach Rate (%)", automargin=True)
        fig.update_layout(
            height=430,
            margin=dict(l=80, r=90, t=70, b=70),
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

# ============================================================
# ROOT CAUSE ANALYSIS
# ============================================================

st.header("🔍 Root Cause Analysis")

col1, col2 = st.columns(2)

if "Root_Cause" in filtered.columns:

    root_analysis = (
        filtered.groupby("Root_Cause")
        .agg(
            Tickets=("Root_Cause", "size"),
            Avg_Resolution=("Resolution_Hours", "mean"),
            SLA_Breach_Rate=("SLA_Status", lambda x: (x == "Breached").mean() * 100)
        )
        .reset_index()
    )

    root_analysis["Avg_Resolution"] = root_analysis[
        "Avg_Resolution"
    ].round(2)

    all_breached = (
        "SLA_Status" in filtered.columns
        and not filtered.empty
        and filtered["SLA_Status"].eq("Breached").all()
    )

    if all_breached:
        root_metric = "Tickets"
        root_metric_title = "Breached Tickets by Root Cause"
        root_x_title = "Breached Tickets"
    else:
        root_metric = "SLA_Breach_Rate"
        root_metric_title = "SLA Breach Rate by Root Cause"
        root_x_title = "SLA Breach Rate (%)"

    with col1:

        fig = px.bar(
            root_analysis.sort_values(
                root_metric,
                ascending=True
            ),
            x=root_metric,
            y="Root_Cause",
            orientation="h",
            text=root_metric,
            title=root_metric_title
        )

        if root_metric == "Tickets":
            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                cliponaxis=False,
            )
        else:
            fig.update_traces(
                texttemplate="%{text:.2f}%",
                textposition="outside",
                cliponaxis=False,
            )

        fig.update_xaxes(title=root_x_title, automargin=True)
        fig.update_layout(
            height=max(430, 55 * len(root_analysis)),
            margin=dict(l=180, r=110, t=70, b=70),
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with col2:

        fig = px.bar(
            root_analysis.sort_values(
                "Avg_Resolution",
                ascending=True
            ),
            x="Avg_Resolution",
            y="Root_Cause",
            orientation="h",
            text="Avg_Resolution",
            title="Average Resolution Time by Root Cause"
        )

        fig.update_traces(
            texttemplate="%{text:.2f} hrs",
            textposition="outside",
            cliponaxis=False,
        )
        fig.update_xaxes(title="Average Resolution (hrs)", automargin=True)
        fig.update_layout(
            height=max(430, 55 * len(root_analysis)),
            margin=dict(l=180, r=120, t=70, b=70),
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.dataframe(
        root_analysis.sort_values(
            "SLA_Breach_Rate",
            ascending=False
        ),
        width="stretch",
        hide_index=True
    )

# ============================================================
# DEPARTMENT ANALYSIS
# ============================================================

st.header("🏢 Department Performance")

if "Department" in filtered.columns:

    dept_analysis = (
        filtered.groupby("Department")
        .agg(
            Tickets=("Department", "size"),
            Avg_Resolution=("Resolution_Hours", "mean"),
            Avg_CSAT=("CSAT_Score", "mean")
            if "CSAT_Score" in filtered.columns
            else ("Department", "size"),
            SLA_Breach_Rate=(
                "SLA_Status",
                lambda x: (x == "Breached").mean() * 100
            )
            if "SLA_Status" in filtered.columns
            else ("Department", "size")
        )
        .reset_index()
    )

    dept_analysis["Avg_Resolution"] = dept_analysis[
        "Avg_Resolution"
    ].round(2)

    dept_analysis["Avg_CSAT"] = dept_analysis[
        "Avg_CSAT"
    ].round(2)

    dept_analysis["SLA_Breach_Rate"] = dept_analysis[
        "SLA_Breach_Rate"
    ].round(2)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            dept_analysis.sort_values(
                "SLA_Breach_Rate",
                ascending=True
            ),
            x="SLA_Breach_Rate",
            y="Department",
            orientation="h",
            text="SLA_Breach_Rate",
            title="SLA Breach Rate by Department"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            cliponaxis=False,
        )
        fig.update_layout(
            height=430,
            margin=dict(l=150, r=100, t=70, b=70),
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with col2:

        fig = px.scatter(
            dept_analysis,
            x="Avg_Resolution",
            y="SLA_Breach_Rate",
            size="Tickets",
            hover_name="Department",
            text="Department",
            title="Resolution Time vs SLA Breach Rate"
        )
        fig.update_traces(textposition="top center", cliponaxis=False)
        fig.update_xaxes(title="Average Resolution (hrs)")
        fig.update_yaxes(title="SLA Breach Rate (%)")
        fig.update_layout(height=430, margin=dict(l=80, r=80, t=70, b=70))

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.dataframe(
        dept_analysis.sort_values(
            "SLA_Breach_Rate",
            ascending=False
        ),
        width="stretch",
        hide_index=True
    )

# ============================================================
# PROCESS PERFORMANCE
# ============================================================

st.markdown("---")
st.header("⚙️ Process Performance")

if "Process" in filtered.columns:

    process_summary = (
        filtered.groupby("Process")
        .agg(
            Tickets=("Process", "size"),
            Avg_Resolution=("Resolution_Hours", "mean"),
            SLA_Breach_Rate=(
                "SLA_Status",
                lambda x: (x == "Breached").mean() * 100
            ) if "SLA_Status" in filtered.columns else ("Process", "size"),
            Avg_CSAT=(
                "CSAT_Score", "mean"
            ) if "CSAT_Score" in filtered.columns else ("Process", "size")
        )
        .reset_index()
    )

    process_summary["Avg_Resolution"] = process_summary["Avg_Resolution"].round(2)
    process_summary["SLA_Breach_Rate"] = process_summary["SLA_Breach_Rate"].round(2)
    process_summary["Avg_CSAT"] = process_summary["Avg_CSAT"].round(2)

    if not process_summary.empty:
        max_breach = process_summary["SLA_Breach_Rate"].max()
        max_resolution = process_summary["Avg_Resolution"].max()

        highest_risk_processes = process_summary[
            process_summary["SLA_Breach_Rate"] == max_breach
        ]
        highest_resolution_processes = process_summary[
            process_summary["Avg_Resolution"] == max_resolution
        ]

        insight_col1, insight_col2 = st.columns(2)

        with insight_col1:
            risk_process_names = ", ".join(highest_risk_processes["Process"].astype(str))
            st.info(
                f"🚨 **Highest SLA Risk:** {risk_process_names} has the "
                f"highest SLA breach rate at **{max_breach:.2f}%**."
            )

        with insight_col2:
            resolution_process_names = ", ".join(highest_resolution_processes["Process"].astype(str))
            st.warning(
                f"⏱️ **Longest Resolution:** {resolution_process_names} has the "
                f"highest average resolution time at **{max_resolution:.2f} hrs**."
            )

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                process_summary.sort_values("SLA_Breach_Rate", ascending=True),
                x="SLA_Breach_Rate",
                y="Process",
                orientation="h",
                text="SLA_Breach_Rate",
                title="SLA Breach Rate by Process"
            )
            fig.update_traces(
                texttemplate="%{text:.2f}%",
                textposition="outside",
                cliponaxis=False
            )
            fig.update_layout(
                xaxis_title="SLA Breach Rate (%)",
                yaxis_title="Process",
                height=max(430, 55 * len(process_summary)),
                margin=dict(l=180, r=110, t=70, b=70)
            )
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                process_summary.sort_values("Avg_Resolution", ascending=True),
                x="Avg_Resolution",
                y="Process",
                orientation="h",
                text="Avg_Resolution",
                title="Average Resolution Time by Process"
            )
            fig.update_traces(
                texttemplate="%{text:.2f} hrs",
                textposition="outside",
                cliponaxis=False
            )
            fig.update_layout(
                xaxis_title="Average Resolution (hrs)",
                yaxis_title="Process",
                height=max(430, 55 * len(process_summary)),
                margin=dict(l=180, r=120, t=70, b=70)
            )
            st.plotly_chart(fig, width="stretch")

        st.subheader("📋 Process Performance Summary")
        process_display = process_summary.sort_values(
            "SLA_Breach_Rate", ascending=False
        ).copy()
        st.dataframe(
            process_display,
            width="stretch",
            hide_index=True,
            column_config={
                "Tickets": st.column_config.NumberColumn("Tickets", format="%d"),
                "Avg_Resolution": st.column_config.NumberColumn("Avg Resolution (hrs)", format="%.2f"),
                "SLA_Breach_Rate": st.column_config.NumberColumn("SLA Breach Rate (%)", format="%.2f"),
                "Avg_CSAT": st.column_config.NumberColumn("Avg CSAT", format="%.2f"),
            },
        )

        st.subheader("🔎 Department & Process Risk Detail")
        process_detail = (
            filtered.groupby(["Department", "Process"])
            .agg(
                Tickets=("Process", "size"),
                Avg_Assignment_Delay=(
                    "Assignment_Delay_Hours", "mean"
                ) if "Assignment_Delay_Hours" in filtered.columns else ("Process", "size"),
                Avg_Resolution=("Resolution_Hours", "mean"),
                SLA_Breach_Rate=(
                    "SLA_Status",
                    lambda x: (x == "Breached").mean() * 100
                ) if "SLA_Status" in filtered.columns else ("Process", "size"),
                Avg_CSAT=(
                    "CSAT_Score", "mean"
                ) if "CSAT_Score" in filtered.columns else ("Process", "size")
            )
            .reset_index()
        )

        for col in ["Avg_Assignment_Delay", "Avg_Resolution", "SLA_Breach_Rate", "Avg_CSAT"]:
            if col in process_detail.columns:
                process_detail[col] = process_detail[col].round(2)

        st.dataframe(
            process_detail.sort_values("SLA_Breach_Rate", ascending=False).head(20),
            width="stretch",
            hide_index=True,
            column_config={
                "Tickets": st.column_config.NumberColumn("Tickets", format="%d"),
                "Avg_Assignment_Delay": st.column_config.NumberColumn("Avg Assignment Delay (hrs)", format="%.2f"),
                "Avg_Resolution": st.column_config.NumberColumn("Avg Resolution (hrs)", format="%.2f"),
                "SLA_Breach_Rate": st.column_config.NumberColumn("SLA Breach Rate (%)", format="%.2f"),
                "Avg_CSAT": st.column_config.NumberColumn("Avg CSAT", format="%.2f"),
            },
        )

else:
    st.info(
        "ℹ️ **Process Insights:** No process-level data is available for the current filters."
    )


# ASSIGNMENT DELAY
# ============================================================

st.header("⏱️ Assignment Delay Analysis")

if (
    "Assignment_Delay_Hours" in filtered.columns
    and "SLA_Status" in filtered.columns
):

    delay_analysis = (
        filtered.assign(
            Delay_Band=pd.cut(
                filtered["Assignment_Delay_Hours"],
                bins=[-1, 1, 3, float("inf")],
                labels=[
                    "Under 1 Hour",
                    "1–3 Hours",
                    "3+ Hours"
                ]
            )
        )
        .groupby("Delay_Band", observed=True)
        .agg(
            Tickets=("Ticket_ID", "size")
            if "Ticket_ID" in filtered.columns
            else ("SLA_Status", "size"),
            Avg_Resolution=("Resolution_Hours", "mean"),
            SLA_Breach_Rate=(
                "SLA_Status",
                lambda x: (x == "Breached").mean() * 100
            )
        )
        .reset_index()
    )

    delay_analysis["Avg_Resolution"] = delay_analysis[
        "Avg_Resolution"
    ].round(2)

    delay_analysis["SLA_Breach_Rate"] = delay_analysis[
        "SLA_Breach_Rate"
    ].round(2)

    st.dataframe(
        delay_analysis,
        width="stretch",
        hide_index=True,
        column_config={
            "Tickets": st.column_config.NumberColumn("Tickets", format="%d"),
            "Avg_Resolution": st.column_config.NumberColumn("Avg Resolution (hrs)", format="%.2f"),
            "SLA_Breach_Rate": st.column_config.NumberColumn("SLA Breach Rate (%)", format="%.2f"),
        },
    )

    fig = px.bar(
        delay_analysis,
        x="Delay_Band",
        y="SLA_Breach_Rate",
        text="SLA_Breach_Rate",
        title="Assignment Delay vs SLA Breach Rate"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        xaxis_title="Assignment Delay Band",
        yaxis_title="SLA Breach Rate (%)",
        height=460,
        margin=dict(l=80, r=100, t=70, b=80)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# ACTIONABLE RECOMMENDATIONS
# ============================================================

st.header("🎯 Actionable Recommendations")
st.caption(
    "Management actions generated dynamically from the currently filtered ticket population."
)

if not filtered.empty:

    recommendation_rows = []

    # Overall SLA opportunity
    breach_count = int(
        filtered["SLA_Status"].eq("Breached").sum()
    ) if "SLA_Status" in filtered.columns else 0

    if "SLA_Status" in filtered.columns:
        illustrative_10pp = int(round(len(filtered) * 0.10))
        recommendation_rows.append({
            "Priority": "P1",
            "Focus Area": "SLA Performance",
            "Finding": f"{breach_count:,} filtered tickets breached SLA ({sla_breach_rate:.2f}%).",
            "Recommended Action": "Run a weekly SLA recovery review focused on the highest-volume and highest-breach segments.",
            "Expected Impact": f"Illustrative opportunity: a 10-point breach-rate reduction would improve SLA compliance for ~{illustrative_10pp:,} tickets."
        })

    # Root-cause recommendation
    if "Root_Cause" in filtered.columns and "SLA_Status" in filtered.columns:
        rc = (
            filtered.groupby("Root_Cause")
            .agg(
                Tickets=("Root_Cause", "size"),
                Breach_Rate=("SLA_Status", lambda x: (x == "Breached").mean() * 100),
                Avg_Resolution=("Resolution_Hours", "mean"),
            )
            .reset_index()
            .sort_values(["Breach_Rate", "Tickets"], ascending=[False, False])
        )

        if not rc.empty:
            top_rc = rc.iloc[0]
            recommendation_rows.append({
                "Priority": "P1",
                "Focus Area": f"Root Cause: {top_rc['Root_Cause']}",
                "Finding": (
                    f"{int(top_rc['Tickets']):,} tickets; "
                    f"{top_rc['Breach_Rate']:.2f}% SLA breach rate; "
                    f"{top_rc['Avg_Resolution']:.2f} hrs average resolution."
                ),
                "Recommended Action": (
                    "Perform a root-cause deep dive, identify the highest-volume failure points, "
                    "and introduce a targeted corrective-action plan with an owner and due date."
                ),
                "Expected Impact": "Reduce repeat failures and improve both SLA compliance and resolution time."
            })

    # Assignment delay recommendation
    if "Assignment_Delay_Hours" in filtered.columns and "SLA_Status" in filtered.columns:
        delay = (
            filtered.assign(
                Delay_Band=pd.cut(
                    filtered["Assignment_Delay_Hours"],
                    bins=[-1, 1, 3, float("inf")],
                    labels=["Under 1 Hour", "1–3 Hours", "3+ Hours"]
                )
            )
            .groupby("Delay_Band", observed=True)
            .agg(
                Tickets=("SLA_Status", "size"),
                Breach_Rate=("SLA_Status", lambda x: (x == "Breached").mean() * 100)
            )
            .reset_index()
        )

        if not delay.empty:
            worst_delay = delay.sort_values("Breach_Rate", ascending=False).iloc[0]
            recommendation_rows.append({
                "Priority": "P1" if str(worst_delay["Delay_Band"]) == "3+ Hours" else "P2",
                "Focus Area": "Assignment Delay",
                "Finding": (
                    f"{worst_delay['Delay_Band']}: {int(worst_delay['Tickets']):,} tickets "
                    f"with {worst_delay['Breach_Rate']:.2f}% SLA breach rate."
                ),
                "Recommended Action": (
                    "Introduce assignment-age alerts and an operational queue for unassigned tickets; "
                    "set an escalation trigger before the SLA risk window."
                ),
                "Expected Impact": "Earlier ownership reduces avoidable waiting time and downstream SLA breaches."
            })

    # Priority recommendation
    if "Priority" in filtered.columns and "SLA_Status" in filtered.columns:
        priority = (
            filtered.groupby("Priority")
            .agg(
                Tickets=("SLA_Status", "size"),
                Breach_Rate=("SLA_Status", lambda x: (x == "Breached").mean() * 100)
            )
            .reset_index()
            .sort_values("Breach_Rate", ascending=False)
        )

        if not priority.empty:
            top_priority = priority.iloc[0]
            recommendation_rows.append({
                "Priority": "P1" if str(top_priority["Priority"]) == "Critical" else "P2",
                "Focus Area": f"Priority: {top_priority['Priority']}",
                "Finding": (
                    f"{int(top_priority['Tickets']):,} tickets with "
                    f"{top_priority['Breach_Rate']:.2f}% SLA breach rate."
                ),
                "Recommended Action": (
                    "Create a priority-specific triage queue and review capacity, routing and "
                    "escalation rules for this workload."
                ),
                "Expected Impact": "Focuses operational capacity where SLA exposure is highest."
            })

    # CSAT recommendation
    if "CSAT_Score" in filtered.columns:
        low_csat = filtered["CSAT_Score"].mean()
        if low_csat < 3.5:
            recommendation_rows.append({
                "Priority": "P2",
                "Focus Area": "Customer Experience",
                "Finding": f"Average CSAT is {low_csat:.2f}/5.",
                "Recommended Action": (
                    "Review low-CSAT tickets against resolution time, root cause and escalation status "
                    "to identify recurring customer pain points."
                ),
                "Expected Impact": "Targeted service improvements can improve customer experience without treating all tickets equally."
            })

    # Escalation recommendation
    if "Escalated" in filtered.columns:
        escalated_count = int(filtered["Escalated"].eq("Yes").sum())
        if escalated_rate > 20:
            recommendation_rows.append({
                "Priority": "P2",
                "Focus Area": "Escalations",
                "Finding": f"{escalated_count:,} tickets were escalated ({escalated_rate:.2f}%).",
                "Recommended Action": (
                    "Separate preventable escalations from genuine complexity and address the "
                    "top recurring drivers through process, training or routing changes."
                ),
                "Expected Impact": "Lower avoidable escalation volume and reduce management intervention."
            })

    if recommendation_rows:
        recommendations_df = pd.DataFrame(recommendation_rows)

        st.dataframe(
            recommendations_df,
            width="stretch",
            hide_index=True,
            column_config={
                "Priority": st.column_config.TextColumn("Priority"),
                "Focus Area": st.column_config.TextColumn("Focus Area"),
                "Finding": st.column_config.TextColumn("Evidence"),
                "Recommended Action": st.column_config.TextColumn("Recommended Action"),
                "Expected Impact": st.column_config.TextColumn("Expected Impact"),
            },
        )

        st.subheader("📌 Management Takeaway")

        if "SLA_Status" in filtered.columns:
            st.info(
                f"**Current situation:** {sla_breach_rate:.2f}% of the filtered workload is "
                f"breaching SLA, with an average resolution time of {avg_resolution:.2f} hours. "
                "The recommended approach is to attack the highest-risk root cause and assignment "
                "delay first, then monitor the effect on SLA and customer experience."
            )

else:
    st.info(
        "No filtered tickets are available. Select at least one value in the filters "
        "to generate recommendations."
    )


# ============================================================
# TICKET EXPLORER
# ============================================================

st.header("🎫 Ticket Explorer")

search = st.text_input(
    "Search Ticket ID, Department, Process or Root Cause"
)

ticket_view = filtered.copy()

if search:

    search_mask = pd.Series(
        False,
        index=ticket_view.index
    )

    for col in [
        "Ticket_ID",
        "Department",
        "Process",
        "Root_Cause"
    ]:

        if col in ticket_view.columns:

            search_mask |= (
                ticket_view[col]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            )

    ticket_view = ticket_view[search_mask]

st.write(
    f"Showing **{len(ticket_view):,}** tickets"
)

st.dataframe(
    ticket_view.head(500),
    width="stretch",
    hide_index=True
)

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Business Operations Analytics Platform | "
    "Built using Python, Pandas, Streamlit, Plotly and SQL"
)
