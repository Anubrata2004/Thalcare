import sqlite3

# Connect to the hospitals.db
conn = sqlite3.connect("hospitals.db")
c = conn.cursor()

# Fetch column names
c.execute("PRAGMA table_info(hospitals)")
columns = [col[1] for col in c.fetchall()]

# Fetch all rows
c.execute("SELECT * FROM hospitals")
rows = c.fetchall()

# Print header
print(" | ".join(columns))
print("-" * 80)

# Print each row
for row in rows:
    print(" | ".join(str(cell) for cell in row))

conn.close()
