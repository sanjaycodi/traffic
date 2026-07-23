"""
db_to_csv.py
------------
Exports the traffic_data table from traffic.db back into a CSV file.
Useful after CRUD operations, to get an updated dataset for training.
"""

import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Database"))
from SQL import get_connection

OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "..", "..", "clearance_export.csv")


def export_db_to_csv(output_path=OUTPUT_CSV):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM traffic_data", conn)
    conn.close()

    df.to_csv(output_path, index=False)
    print(f"Exported {len(df)} rows to {output_path}")


if __name__ == "__main__":
    export_db_to_csv()
