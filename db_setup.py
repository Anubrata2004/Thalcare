import sqlite3

conn = sqlite3.connect('thalcare.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    password TEXT,
    phone TEXT,
    dob TEXT,
    blood_group TEXT,
    location TEXT,
    role TEXT,
    last_required TEXT,
    next_required TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS donors (
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    password TEXT,
    blood_group TEXT,
    last_donation TEXT,
    diseases TEXT,
    availability TEXT,
    role TEXT,
    location TEXT,
    phone TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS hospitals (
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    password TEXT,
    license_id TEXT,
    role TEXT,
    location TEXT
)
''')

conn.commit()
conn.close()
print("Database and tables created successfully.")
