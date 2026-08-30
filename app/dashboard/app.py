import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RecoverX",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

transactions = pd.read_csv("data/transactions.csv")

recovery = pd.read_csv(
    "data/recovery_recommendations.csv"
)

predictions = pd.read_csv(
    "data/recovery_predictions.csv"
)

agent_decisions = pd.read_csv(
    "data/agent_decisions.csv"
)

# Convert transaction time to datetime
transactions["transaction_time"] = pd.to_datetime(
    transactions["transaction_time"]
)


# ============================================================
# CALCULATE METRICS
# ============================================================

total_transactions = len(transactions)

successful = transactions[
    transactions["status"] == "SUCCESS"
]

failed = transactions[
    transactions["status"] == "FAILED"
]

successful_count = len(successful)
failed_count = len(failed)

total_value = transactions["amount"].sum()

revenue_at_risk = failed["amount"].sum()

success_rate = (
    successful_count / total_transactions
) * 100

failure_rate = (
    failed_count / total_transactions
) * 100


# Recovery opportunity:
# Focus on HIGH and MEDIUM priority transactions.
priority_recovery = recovery[
    recovery["priority"].isin(["HIGH", "MEDIUM"])
]

recovery_opportunity = priority_recovery["amount"].sum()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
    }

    .metric-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎯 RecoverX</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Payment Recovery Intelligence'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Transactions",
        f"{total_transactions:,}"
    )


with col2:
    st.metric(
        "Successful Payments",
        f"{successful_count:,}",
        f"{success_rate:.2f}% success"
    )


with col3:
    st.metric(
        "Revenue At Risk",
        f"₹{revenue_at_risk:,.0f}",
        f"{failure_rate:.2f}% failure rate"
    )


with col4:
    st.metric(
        "Recovery Opportunity",
        f"₹{recovery_opportunity:,.0f}",
        "High + Medium priority"
    )


# ============================================================
# PAYMENT HEALTH
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Payment Health</div>',
    unsafe_allow_html=True
)

health_col1, health_col2 = st.columns(2)


with health_col1:

    st.write("Overall payment success rate")

    st.progress(
        int(success_rate)
    )

    st.write(
        f"**{success_rate:.2f}%** of transactions succeeded."
    )


with health_col2:

    st.write("Failure rate")

    st.progress(
        int(failure_rate)
    )

    st.write(
        f"**{failure_rate:.2f}%** of transactions failed."
    )
# ============================================================
# AI RECOVERY INTELLIGENCE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🤖 AI Recovery Intelligence</div>',
    unsafe_allow_html=True
)

st.write(
    "RecoverX uses the trained prediction model to estimate "
    "the probability that a failed payment can be recovered."
)


ai_col1, ai_col2, ai_col3 = st.columns(3)


with ai_col1:

    average_probability = (
        predictions["recovery_probability"].mean()
    )

    st.metric(
        "Average Recovery Probability",
        f"{average_probability:.1f}%"
    )


with ai_col2:

    total_expected_recovery = (
        predictions["expected_recovery"].sum()
    )

    st.metric(
        "Expected Recovery Value",
        f"₹{total_expected_recovery:,.0f}"
    )


with ai_col3:

    retry_count = len(
        predictions[
            predictions["recommended_action"] == "RETRY"
        ]
    )

    st.metric(
        "Recommended Retries",
        f"{retry_count:,}"
    )


st.write("### Top Recovery Opportunities")


ai_display_columns = [
    "transaction_id",
    "amount",
    "failure_reason",
    "recovery_probability",
    "expected_recovery",
    "recommended_action"
]


top_predictions = predictions[
    ai_display_columns
].head(15).copy()


top_predictions["recovery_probability"] = (
    top_predictions["recovery_probability"]
    .round(1)
)


top_predictions["expected_recovery"] = (
    top_predictions["expected_recovery"]
    .round(2)
)


st.dataframe(
    top_predictions,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# DAILY TRANSACTION TREND
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Transaction Activity</div>',
    unsafe_allow_html=True
)

daily_transactions = (
    transactions
    .set_index("transaction_time")
    .resample("D")
    .size()
)

st.line_chart(
    daily_transactions,
    use_container_width=True
)


# ============================================================
# PAYMENT METHOD ANALYSIS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Payment Method Health</div>',
    unsafe_allow_html=True
)

method_data = (
    transactions
    .groupby(["payment_method", "status"])
    .size()
    .unstack(fill_value=0)
)

if "SUCCESS" not in method_data.columns:
    method_data["SUCCESS"] = 0

if "FAILED" not in method_data.columns:
    method_data["FAILED"] = 0


method_data["total"] = (
    method_data["SUCCESS"] +
    method_data["FAILED"]
)

method_data["success_rate"] = (
    method_data["SUCCESS"] /
    method_data["total"]
) * 100


method_display = method_data[
    ["SUCCESS", "FAILED", "success_rate"]
].copy()

method_display["success_rate"] = (
    method_display["success_rate"]
    .round(2)
)


st.dataframe(
    method_display,
    use_container_width=True
)


# ============================================================
# RECOVERY COMMAND CENTER
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🎯 Recovery Command Center</div>',
    unsafe_allow_html=True
)

st.write(
    "RecoverX prioritizes failed transactions based on "
    "transaction value, failure type and previous retry attempts."
)


# ============================================================
# FILTERS
# ============================================================

filter_col1, filter_col2, filter_col3 = st.columns(3)


with filter_col1:

    selected_priority = st.selectbox(
        "Priority",
        ["ALL", "HIGH", "MEDIUM", "LOW"]
    )


with filter_col2:

    selected_method = st.selectbox(
        "Payment Method",
        ["ALL"] +
        sorted(
            recovery["payment_method"]
            .dropna()
            .unique()
            .tolist()
        )
    )


with filter_col3:

    search_transaction = st.text_input(
        "Search Transaction ID"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = recovery.copy()


if selected_priority != "ALL":

    filtered = filtered[
        filtered["priority"] == selected_priority
    ]


if selected_method != "ALL":

    filtered = filtered[
        filtered["payment_method"] == selected_method
    ]


if search_transaction:

    filtered = filtered[
        filtered["transaction_id"]
        .astype(str)
        .str.contains(
            search_transaction,
            case=False,
            na=False
        )
    ]


# ============================================================
# RECOVERY TABLE
# ============================================================

display_columns = [
    "transaction_id",
    "amount",
    "payment_method",
    "failure_reason",
    "retry_count",
    "recovery_score",
    "priority"
]


st.dataframe(
    filtered[display_columns].head(50),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# TRANSACTION INVESTIGATION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🔎 Investigate a Recovery</div>',
    unsafe_allow_html=True
)


if len(filtered) > 0:

    transaction_options = (
        filtered["transaction_id"]
        .tolist()
    )

    selected_transaction = st.selectbox(
        "Select a failed transaction",
        transaction_options
    )

    selected_row = filtered[
        filtered["transaction_id"]
        == selected_transaction
    ].iloc[0]


    info1, info2, info3, info4 = st.columns(4)


    with info1:
        st.metric(
            "Transaction",
            selected_row["transaction_id"]
        )


    with info2:
        st.metric(
            "Amount",
            f"₹{selected_row['amount']:,.2f}"
        )


    with info3:
        st.metric(
            "Recovery Score",
            selected_row["recovery_score"]
        )


    with info4:
        st.metric(
            "Priority",
            selected_row["priority"]
        )


    st.write("### 🤖 RecoverX Recommendation")

    st.info(
        selected_row["recommendation"]
    )


else:

    st.warning(
        "No transactions match the selected filters."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "RecoverX — Payment Recovery Intelligence Prototype"
)