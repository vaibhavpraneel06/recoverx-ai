import pandas as pd
import random
from datetime import datetime, timedelta


# Number of transactions we want to generate
NUM_TRANSACTIONS = 5000

# Possible payment methods
PAYMENT_METHODS = ["UPI", "CARD", "NETBANKING", "WALLET"]

# Possible transaction statuses
STATUSES = ["SUCCESS", "FAILED"]

# Possible failure reasons
FAILURE_REASONS = [
    "BANK_DECLINE",
    "INSUFFICIENT_FUNDS",
    "TIMEOUT",
    "NETWORK_ERROR",
    "LIMIT_EXCEEDED"
]


transactions = []

start_time = datetime.now() - timedelta(days=30)


for i in range(NUM_TRANSACTIONS):

    transaction_id = f"TXN{100000 + i}"
    customer_id = f"CUST{random.randint(1000, 9999)}"

    amount = round(random.uniform(100, 50000), 2)

    payment_method = random.choice(PAYMENT_METHODS)

    transaction_time = start_time + timedelta(
        minutes=random.randint(0, 30 * 24 * 60)
    )

    # Randomly decide whether payment succeeds
    status = random.choices(
        STATUSES,
        weights=[85, 15]
    )[0]

    if status == "FAILED":
        failure_reason = random.choice(FAILURE_REASONS)
    else:
        failure_reason = None

    retry_count = random.randint(0, 3)

    transactions.append({
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "amount": amount,
        "payment_method": payment_method,
        "status": status,
        "failure_reason": failure_reason,
        "transaction_time": transaction_time,
        "retry_count": retry_count
    })


# Convert the list into a DataFrame
df = pd.DataFrame(transactions)

# Save the data
output_file = "data/transactions.csv"

df.to_csv(output_file, index=False)

print(f"Generated {NUM_TRANSACTIONS} transactions.")
print(f"Saved to: {output_file}")

print("\nFirst 5 transactions:")
print(df.head())