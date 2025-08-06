import sqlite3

# Connect to emergency.db (creates it if it doesn't exist)
conn = sqlite3.connect('emergency.db')
c = conn.cursor()

# Create emergency_requests table
c.execute('''
CREATE TABLE IF NOT EXISTS emergency_requests (
    id TEXT PRIMARY KEY,
    name TEXT,
    blood_group TEXT,
    location TEXT,
    urgency_level TEXT,
    contact TEXT,
    request_time TEXT,
    fulfilled TEXT
)
''')

# Commit and close
conn.commit()
conn.close()

print("✅ Emergency database and 'emergency_requests' table created.")
