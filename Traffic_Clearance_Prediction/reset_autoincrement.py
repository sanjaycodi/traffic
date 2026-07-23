import sqlite3

conn = sqlite3.connect("traffic/Database/traffic.db")
cur = conn.cursor()

# Reset the autoincrement counter to match current max id (50)
cur.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM traffic_data) WHERE name = 'traffic_data'")
conn.commit()

cur.execute("SELECT seq FROM sqlite_sequence WHERE name = 'traffic_data'")
print("Autoincrement counter reset to:", cur.fetchone())

conn.close()