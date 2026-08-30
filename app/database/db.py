import sqlite3
from pathlib import Path

# Location of our database file
DB_PATH = Path("data/recoverx.db")


def get_connection():
    """Create and return a connection to the RecoverX database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Create the transactions table if it doesn't already exist."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            status TEXT NOT NULL,
            failure_reason TEXT,
            retry_count INTEGER DEFAULT 0,
            recovery_score REAL,
            priority TEXT
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("RecoverX database initialized successfully!")