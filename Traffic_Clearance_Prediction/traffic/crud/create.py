"""
create.py
---------
Insert a new traffic record into the database.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Database"))
from SQL import get_connection


def add_record(num_vehicles, avg_speed, road_length, signal_time,
               arrival_rate, traffic_level, clearance_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO traffic_data
        (num_vehicles, avg_speed, road_length, signal_time,
         arrival_rate, traffic_level, clearance_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (num_vehicles, avg_speed, road_length, signal_time,
          arrival_rate, traffic_level, clearance_time))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    print(f"Inserted record with id={new_id}")
    return new_id


if __name__ == "__main__":
    # Example usage
    add_record(
        num_vehicles=50,
        avg_speed=35.0,
        road_length=200.0,
        signal_time=45,
        arrival_rate=1.2,
        traffic_level="High",
        clearance_time=120.0
    )
