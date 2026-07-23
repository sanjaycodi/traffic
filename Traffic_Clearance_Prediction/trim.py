import sqlite3

conn = sqlite3.connect("traffic/Database/traffic.db")
cur = conn.cursor()

cur.execute("DELETE FROM traffic_data WHERE id > 50")
conn.commit()

cur.execute("SELECT COUNT(*) FROM traffic_data")
print("Remaining records:", cur.fetchone()[0])

conn.close()