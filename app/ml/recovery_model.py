import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/recovery_queue.csv")


# ============================================================
# 2. CREATE A SIMULATED RECOVERY OUTCOME
# ============================================================
#
# IMPORTANT:
# Our current dataset does not contain real recovery outcomes.
# Therefore, this is synthetic training data for our prototype.
#

def simulate_recovery(row):

    probability = 0.50

    # Temporary failures are generally better candidates
    if row["failure_reason"] == "TIMEOUT":
        probability += 0.20

    elif row["failure_reason"] == "NETWORK_ERROR":
        probability += 0.15

    elif row["failure_reason"] == "BANK_DECLINE":
        probability += 0.05

    elif row["failure_reason"] == "INSUFFICIENT_FUNDS":
        probability -= 0.15

    elif row["failure_reason"] == "LIMIT_EXCEEDED":
        probability -= 0.10

    # Fewer previous retries = better opportunity
    probability -= row["retry_count"] * 0.08

    # Keep probability between 0 and 1
    probability = max(
        0.05,
        min(probability, 0.95)
    )

    # Convert probability into a simulated outcome
    import random

    return int(
        random.random() < probability
    )


df["recovered"] = df.apply(
    simulate_recovery,
    axis=1
)


# ============================================================
# 3. SELECT FEATURES
# ============================================================

features = [
    "amount",
    "payment_method",
    "failure_reason",
    "retry_count",
    "recovery_score"
]

X = df[features]

y = df["recovered"]


# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# 5. PREPROCESSING
# ============================================================

categorical_features = [
    "payment_method",
    "failure_reason"
]

numeric_features = [
    "amount",
    "retry_count",
    "recovery_score"
]


preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


# ============================================================
# 6. MACHINE LEARNING MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    class_weight="balanced"
)


pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)


# ============================================================
# 7. TRAIN
# ============================================================

pipeline.fit(
    X_train,
    y_train
)


# ============================================================
# 8. EVALUATE
# ============================================================

predictions = pipeline.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n===== RECOVERX ML MODEL =====\n")

print(
    f"Training samples: {len(X_train)}"
)

print(
    f"Testing samples: {len(X_test)}"
)

print(
    f"Model accuracy on simulated data: "
    f"{accuracy * 100:.2f}%"
)


# ============================================================
# 9. SAVE MODEL
# ============================================================

joblib.dump(
    pipeline,
    "app/ml/recovery_model.joblib"
)

print(
    "\nModel saved to:"
    " app/ml/recovery_model.joblib"
)