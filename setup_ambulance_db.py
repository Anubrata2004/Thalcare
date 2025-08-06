import sqlite3

conn = sqlite3.connect("ambulance.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS drivers (
        driver_id TEXT PRIMARY KEY,
        name TEXT,
        phone TEXT,
        ambulance_plate TEXT,
        hospital_id TEXT,
        available TEXT
    )
''')

drivers = [
    ("D001", "Rahul Sen", "+91 9876543210", "WB26G1234", "H001", "yes"),
    ("D002", "Amit Das", "+91 9988776655", "WB06Q4567", "H002", "yes"),
    ("D003", "Nikhil Roy", "+91 8877665544", "WB04T7890", "H001", "no"),
    ("D004", "Sumit Ghosh", "+91 7788991122", "WB20P1111", "H003", "yes"),
    ("D005", "Manoj Dey", "+91 8899776655", "WB10Z9999", "H004", "yes"),
]

c.executemany("INSERT INTO drivers VALUES (?, ?, ?, ?, ?, ?)", drivers)

conn.commit()
conn.close()

print("✅ ambulance.db created and drivers added.")
