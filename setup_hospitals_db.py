import sqlite3

# Connect to hospitals.db (will create if not exists)
conn = sqlite3.connect("hospitals.db")
c = conn.cursor()

# Drop the table if it already exists (for clean re-runs)
c.execute("DROP TABLE IF EXISTS hospitals")

# Create the hospitals table
c.execute('''
CREATE TABLE hospitals (
    id TEXT PRIMARY KEY,
    name TEXT,
    latitude REAL,
    longitude REAL,
    phone TEXT,
    distance TEXT,
    ambulance_status TEXT
)
''')

# Hardcoded hospital data near Ruby Hospital, Kolkata
hospitals = [
    ("H001", "Ruby General Hospital", 22.5206, 88.4037, "+91 33 6601 1800", "9m", "yes"),
    ("H002", "Desun Hospital", 22.5190, 88.4042, "+91 90517 15171", "120m", "yes"),
    ("H003", "Genesis Hospital", 22.5170, 88.4055, "+91 33 4022 4242", "400m", "no"),
    ("H004", "Fortis Hospital, Anandapur", 22.5140, 88.4070, "+91 98730 31410", "800m", "yes"),
    ("H005", "Cosmos Hospital", 22.5100, 88.4100, "+91 33 2416 1084", "2.3 km", "no")
]

# Insert the data
c.executemany("INSERT INTO hospitals VALUES (?, ?, ?, ?, ?, ?, ?)", hospitals)

# Commit and close
conn.commit()
conn.close()

print("✅ hospitals.db created and populated successfully.")
