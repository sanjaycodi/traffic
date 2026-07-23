"""
update.py
---------
Update an existing traffic record in the database.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Database"))
from SQL import get_connection


def update_record(record_id, **fields):
    """
    Update fields of a record by id.
    Example: update_record(3, avg_speed=40.0, clearance_time=110.0)
    """
    if not fields:
        print("No fields provided to update.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    set_clause = ", ".join(f"{key} = ?" for key in fields.keys())
    values = list(fields.values()) + [record_id]

    cursor.execute(f"UPDATE traffic_data SET {set_clause} WHERE id = ?", values)
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    print(f"Updated {rows_affected} row(s) with id={record_id}")


if __name__ == "__main__":
    # Example usage
    update_record(1, avg_speed=42.5, clearance_time=115.0)
