import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "traffic", "Database"))
from SQL import get_connection

conn = get_connection()
cur = conn.cursor()

# 1. Check current state
cur.execute("SELECT COUNT(*), MIN(id), MAX(id) FROM traffic_data")
print("Before fix -> count, min_id, max_id:", cur.fetchone())

# 2. Create a fresh table with the same structure (no id values carried over)
cur.execute("""
    CREATE TABLE traffic_data_new (
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

# 3. Copy rows over in id order — new table assigns fresh sequential ids (1, 2, 3...)
cur.execute("""
    INSERT INTO traffic_data_new
        (num_vehicles, avg_speed, road_length, signal_time, arrival_rate, traffic_level, clearance_time)
    SELECT num_vehicles, avg_speed, road_length, signal_time, arrival_rate, traffic_level, clearance_time
    FROM traffic_data
    ORDER BY id
""")

# 4. Swap tables
cur.execute("DROP TABLE traffic_data")
cur.execute("ALTER TABLE traffic_data_new RENAME TO traffic_data")
conn.commit()

# 5. Confirm
cur.execute("SELECT COUNT(*), MIN(id), MAX(id) FROM traffic_data")
print("After fix -> count, min_id, max_id:", cur.fetchone())

conn.close()