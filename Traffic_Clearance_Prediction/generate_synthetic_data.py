import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "traffic", "Database"))
from SQL import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("SELECT MAX(id) FROM traffic_data")
max_id = cur.fetchone()[0]
print("Current max id in traffic_data:", max_id)

cur.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'traffic_data'", (max_id,))
conn.commit()

cur.execute("SELECT seq FROM sqlite_sequence WHERE name = 'traffic_data'")
print("Autoincrement counter is now:", cur.fetchone())

conn.close()