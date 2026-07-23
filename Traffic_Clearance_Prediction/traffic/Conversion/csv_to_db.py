"""
csv_to_db.py
------------
Loads clearance_train.csv into the traffic.db SQLite database.
"""

import sys
import os
import pandas as pd

# allow imports from traffic/Database
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Database"))
from SQL import get_connection, create_table

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "clearance_train.csv")


def load_csv_to_db(csv_path=CSV_PATH):
    create_table()  # ensure table (with id column) exists
    conn = get_connection()
    cursor = conn.cursor()

    # Only load the CSV once — skip if the table already has data,
    # so re-running main.py doesn't duplicate rows or wipe the id column.
    cursor.execute("SELECT COUNT(*) FROM traffic_data")
    existing_rows = cursor.fetchone()[0]

    if existing_rows > 0:
        print(f"traffic_data already has {existing_rows} rows — skipping CSV import.")
        conn.close()
        return

    df = pd.read_csv(csv_path)
    # append (not replace) so the id column defined in create_table() is kept
    df.to_sql("traffic_data", conn, if_exists="append", index=False)

    conn.close()
    print(f"Loaded {len(df)} rows from {csv_path} into traffic.db")


if __name__ == "__main__":
    load_csv_to_db()