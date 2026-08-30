from db import get_connection


def get_total_transactions():
    """Return the total number of transactions."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    result = cursor.fetchone()[0]

    connection.close()

    return result


def get_failed_transactions():
    """Return all failed transactions."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE status = 'FAILED'
        ORDER BY amount DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_high_value_failures(min_amount=20000):
    """Return failed transactions above a given amount."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE status = 'FAILED'
        AND amount >= ?
        ORDER BY amount DESC
    """, (min_amount,))

    results = cursor.fetchall()

    connection.close()

    return results


def get_failure_count():
    """Return the number of failed transactions."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE status = 'FAILED'
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result


if __name__ == "__main__":

    total = get_total_transactions()

    failures = get_failure_count()

    high_value = get_high_value_failures()

    print("\n===== RECOVERX DATABASE =====\n")

    print(
        f"Total transactions: {total}"
    )

    print(
        f"Failed transactions: {failures}"
    )

    print(
        f"High-value failures: {len(high_value)}"
    )