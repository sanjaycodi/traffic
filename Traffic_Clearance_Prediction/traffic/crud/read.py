"""
read.py
-------
Fetch/query traffic records from the database.
"""

import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Database"))
from SQL import get_connection


def get_all_records():
    """Return all records as a pandas DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM traffic_data", conn)
    conn.close()
    return df


def get_record_by_id(record_id):
    """Return a single record by its id."""
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM traffic_data WHERE id = ?", conn, params=(record_id,)
    )
    conn.close()
    return df


def get_records_by_level(traffic_level):
    """Return all records matching a given traffic level (Low/Medium/High)."""
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM traffic_data WHERE traffic_level = ?", conn, params=(traffic_level,)
    )
    conn.close()
    return df


if __name__ == "__main__":
    print(get_all_records().head())
