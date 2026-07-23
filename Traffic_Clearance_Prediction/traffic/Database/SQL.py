"""
SQL.py
------
Handles the SQLite database connection and table schema
for the Traffic Clearance Time Prediction project.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "traffic.db")


def get_connection():
    """Return a connection object to the traffic database."""
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_table():
    """Create the traffic_data table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traffic_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_vehicles INTEGER NOT NULL,
            avg_speed REAL NOT NULL,
            road_length REAL NOT NULL,
            signal_time INTEGER NOT NULL,
            arrival_rate REAL NOT NULL,
            traffic_level TEXT,
            clearance_time REAL
        )
    """)
    conn.commit()
    conn.close()
    print("Table 'traffic_data' is ready.")


if __name__ == "__main__":
    create_table()
