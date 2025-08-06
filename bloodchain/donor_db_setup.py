import sqlite3

def init_donor_db():
    conn = sqlite3.connect('donor_data.db')  # Main folder level
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            donor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_donor_db()
    print("✅ Donor database created successfully at bloodchain/donor_data.db")
