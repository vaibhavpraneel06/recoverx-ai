import pandas as pd
import joblib
import sys
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT / "app" / "policies")
)

from recovery_policy import decide_recovery_action


# ============================================================
# LOAD ML MODEL
# ============================================================

MODEL_PATH = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "recovery_model.joblib"
)

model = joblib.load(MODEL_PATH)


# ============================================================
# LOAD TRANSACTIONS
# ============================================================

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "recovery_queue.csv"
)


# ============================================================
# GENERATE AI DECISION
# ============================================================

def analyze_transaction(row):

    features = pd.DataFrame([{
        "amount": row["amount"],
        "payment_method": row["payment_method"],
        "failure_reason": row["failure_reason"],
        "retry_count": row["retry_count"],
        "recovery_score": row["recovery_score"]
    }])

    # --------------------------------------------------------
    # ML prediction
    # --------------------------------------------------------

    probability = (
        model.predict_proba(features)[0][1]
        * 100
    )

    # --------------------------------------------------------
    # Expected recovery
    # --------------------------------------------------------

    expected_recovery = (
        row["amount"]
        * probability
        / 100
    )

    # --------------------------------------------------------
    # Policy decision
    # --------------------------------------------------------

    decision = decide_recovery_action(
        probability=probability,
        failure_reason=row["failure_reason"],
        retry_count=row["retry_count"],
        amount=row["amount"]
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {
        "transaction_id": row["transaction_id"],
        "amount": row["amount"],
        "payment_method": row["payment_method"],
        "failure_reason": row["failure_reason"],
        "retry_count": row["retry_count"],
        "recovery_probability": round(
            probability,
            2
        ),
        "expected_recovery": round(
            expected_recovery,
            2
        ),
        "action": decision["action"],
        "reason": decision["reason"]
    }


# ============================================================
# ANALYZE ALL TRANSACTIONS
# ============================================================

def run_recovery_agent():

    df = pd.read_csv(DATA_PATH)

    results = []

    for _, row in df.iterrows():

        result = analyze_transaction(row)

        results.append(result)

    results_df = pd.DataFrame(results)

    output_path = (
        PROJECT_ROOT
        / "data"
        / "agent_decisions.csv"
    )

    results_df.to_csv(
        output_path,
        index=False
    )

    return results_df


# ============================================================
# RUN AGENT
# ============================================================

if __name__ == "__main__":

    results = run_recovery_agent()

    print(
        "\n===== RECOVERX RECOVERY AGENT =====\n"
    )

    for _, row in results.head(10).iterrows():

        print("--------------------------------------------")

        print(
            f"Transaction: "
            f"{row['transaction_id']}"
        )

        print(
            f"Amount: "
            f"₹{row['amount']:,.2f}"
        )

        print(
            f"Failure: "
            f"{row['failure_reason']}"
        )

        print(
            f"Recovery Probability: "
            f"{row['recovery_probability']}%"
        )

        print(
            f"Expected Recovery: "
            f"₹{row['expected_recovery']:,.2f}"
        )

        print(
            f"Decision: "
            f"{row['action']}"
        )

        print(
            f"Reason: "
            f"{row['reason']}"
        )

    print("--------------------------------------------")

    print(
        "\nAgent decisions saved to:"
        " data/agent_decisions.csv"
    )