import pandas as pd
import joblib


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(
    "app/ml/recovery_model.joblib"
)


# ============================================================
# LOAD FAILED TRANSACTIONS
# ============================================================

df = pd.read_csv(
    "data/recovery_queue.csv"
)


# ============================================================
# FEATURES USED BY THE MODEL
# ============================================================

features = [
    "amount",
    "payment_method",
    "failure_reason",
    "retry_count",
    "recovery_score"
]


X = df[features]


# ============================================================
# PREDICT RECOVERY PROBABILITY
# ============================================================

probabilities = model.predict_proba(X)


# Probability of class 1 = recovered
df["recovery_probability"] = (
    probabilities[:, 1] * 100
)


# ============================================================
# EXPECTED RECOVERY VALUE
# ============================================================

df["expected_recovery"] = (
    df["amount"] *
    (df["recovery_probability"] / 100)
)


# ============================================================
# RECOMMENDED ACTION
# ============================================================

def choose_action(row):

    probability = row["recovery_probability"]

    reason = row["failure_reason"]

    retries = row["retry_count"]

    if probability >= 75 and retries <= 1:

        return "RETRY"

    elif probability >= 50:

        return "ALTERNATE_METHOD"

    elif reason == "INSUFFICIENT_FUNDS":

        return "CUSTOMER_ACTION"

    else:

        return "DO_NOT_RETRY"


df["recommended_action"] = df.apply(
    choose_action,
    axis=1
)


# ============================================================
# SORT BY EXPECTED RECOVERY
# ============================================================

df = df.sort_values(
    by="expected_recovery",
    ascending=False
)


# ============================================================
# SAVE PREDICTIONS
# ============================================================

df.to_csv(
    "data/recovery_predictions.csv",
    index=False
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print(
    "\n===== RECOVERX RECOVERY PREDICTIONS =====\n"
)


display_columns = [
    "transaction_id",
    "amount",
    "failure_reason",
    "retry_count",
    "recovery_probability",
    "expected_recovery",
    "recommended_action"
]


print(
    df[display_columns]
    .head(15)
    .to_string(index=False)
)


print(
    "\nPredictions saved to:"
    " data/recovery_predictions.csv"
)