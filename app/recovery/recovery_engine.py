import pandas as pd


def calculate_recovery_score(row):
    """
    Calculate a recovery priority score from 0 to 100.
    Higher score = higher recovery priority.
    """

    score = 0

    # Higher transaction value gets higher priority
    if row["amount"] >= 20000:
        score += 40
    elif row["amount"] >= 10000:
        score += 30
    elif row["amount"] >= 5000:
        score += 20
    else:
        score += 10

    # Failure reason
    if row["failure_reason"] == "TIMEOUT":
        score += 25

    elif row["failure_reason"] == "NETWORK_ERROR":
        score += 20

    elif row["failure_reason"] == "BANK_DECLINE":
        score += 15

    elif row["failure_reason"] == "LIMIT_EXCEEDED":
        score += 10

    elif row["failure_reason"] == "INSUFFICIENT_FUNDS":
        score += 5

    # Fewer previous retries = better recovery opportunity
    if row["retry_count"] == 0:
        score += 20

    elif row["retry_count"] == 1:
        score += 15

    elif row["retry_count"] == 2:
        score += 10

    else:
        score += 5

    return min(score, 100)


def assign_priority(score):

    if score >= 70:
        return "HIGH"

    elif score >= 45:
        return "MEDIUM"

    else:
        return "LOW"


def generate_recovery_queue():

    df = pd.read_csv("data/transactions.csv")

    # Only failed payments need recovery
    failed = df[df["status"] == "FAILED"].copy()

    # Calculate recovery score
    failed["recovery_score"] = failed.apply(
        calculate_recovery_score,
        axis=1
    )

    # Assign priority
    failed["priority"] = failed["recovery_score"].apply(
        assign_priority
    )

    # Sort highest priority first
    failed = failed.sort_values(
        by="recovery_score",
        ascending=False
    )

    # Save recovery queue
    failed.to_csv(
        "data/recovery_queue.csv",
        index=False
    )

    return failed


if __name__ == "__main__":

    recovery_queue = generate_recovery_queue()

    print("\n===== RECOVERX RECOVERY QUEUE =====\n")

    print(
        recovery_queue[
            [
                "transaction_id",
                "amount",
                "payment_method",
                "failure_reason",
                "retry_count",
                "recovery_score",
                "priority"
            ]
        ].head(20).to_string(index=False)
    )

    print("\n===== PRIORITY SUMMARY =====\n")

    print(
        recovery_queue["priority"]
        .value_counts()
    )