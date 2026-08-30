import pandas as pd


def load_transactions():
    """
    Load transaction data from the CSV file.
    """

    file_path = "data/transactions.csv"

    df = pd.read_csv(file_path)

    return df


def calculate_metrics(df):
    """
    Calculate important payment metrics.
    """

    total_transactions = len(df)

    successful_transactions = len(
        df[df["status"] == "SUCCESS"]
    )

    failed_transactions = len(
        df[df["status"] == "FAILED"]
    )

    total_amount = df["amount"].sum()

    failed_amount = df.loc[
        df["status"] == "FAILED",
        "amount"
    ].sum()

    success_rate = (
        successful_transactions / total_transactions
    ) * 100

    failure_rate = (
        failed_transactions / total_transactions
    ) * 100

    return {
        "total_transactions": total_transactions,
        "successful_transactions": successful_transactions,
        "failed_transactions": failed_transactions,
        "total_amount": round(total_amount, 2),
        "revenue_at_risk": round(failed_amount, 2),
        "success_rate": round(success_rate, 2),
        "failure_rate": round(failure_rate, 2)
    }


def payment_method_analysis(df):
    """
    Analyze success and failure rates
    for each payment method.
    """

    analysis = (
        df.groupby(["payment_method", "status"])
        .size()
        .unstack(fill_value=0)
    )

    return analysis


if __name__ == "__main__":

    transactions = load_transactions()

    metrics = calculate_metrics(transactions)

    print("\n===== RECOVERX PAYMENT ANALYTICS =====\n")

    print(f"Total Transactions: {metrics['total_transactions']}")

    print(
        f"Successful Transactions: "
        f"{metrics['successful_transactions']}"
    )

    print(
        f"Failed Transactions: "
        f"{metrics['failed_transactions']}"
    )

    print(
        f"Total Transaction Value: "
        f"₹{metrics['total_amount']:,.2f}"
    )

    print(
        f"Revenue At Risk: "
        f"₹{metrics['revenue_at_risk']:,.2f}"
    )

    print(
        f"Success Rate: "
        f"{metrics['success_rate']}%"
    )

    print(
        f"Failure Rate: "
        f"{metrics['failure_rate']}%"
    )

    print("\n===== PAYMENT METHOD ANALYSIS =====\n")

    print(payment_method_analysis(transactions))