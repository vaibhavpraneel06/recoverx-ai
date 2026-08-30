import pandas as pd

from db import get_connection


def load_transactions():
    # Read our existing transaction dataset
    df = pd.read_csv("data/transactions.csv")

    # Connect to RecoverX database
    connection = get_connection()

    # Store transactions in SQLite
    df.to_sql(
        "transactions",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print(
        f"Successfully loaded {len(df)} transactions "
        "into the RecoverX database."
    )


if __name__ == "__main__":
    load_transactions()