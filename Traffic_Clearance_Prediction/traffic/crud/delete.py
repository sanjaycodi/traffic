"""
delete.py
---------
Delete a traffic record from the database.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Database"))
from SQL import get_connection


def delete_record(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM traffic_data WHERE id = ?", (record_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    print(f"Deleted {rows_affected} row(s) with id={record_id}")


if __name__ == "__main__":
    delete_record(1)
