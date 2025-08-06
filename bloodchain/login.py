from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# --- Database Paths ---
ADMIN_DB = 'admin.db'
DONOR_DB = 'donor_data.db'


# --- LOGIN ROUTE ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        org_type = request.form.get('org_type')
        admin_id = request.form.get('admin_id')

        conn = sqlite3.connect(ADMIN_DB)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admins WHERE id = ? AND org_type = ?', (admin_id, org_type))
        result = cursor.fetchone()
        conn.close()

        if result:
            return redirect(url_for('donor_register'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')


# --- DONOR REGISTER ROUTE ---
@app.route('/register_donor', methods=['GET', 'POST'])
def donor_register():
    if request.method == 'POST':
        name = request.form.get('name')
        blood_group = request.form.get('blood_group')
        gender = request.form.get('gender')
        age = request.form.get('age')
        
        donor_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DONOR_DB)
        cursor = conn.cursor()

        # Ensure table exists
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

        cursor.execute('''
            INSERT INTO donors (donor_id, name, blood_group, gender, age, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (donor_id, name, blood_group, gender, age, timestamp))
        
        conn.commit()
        conn.close()

        return f"Donor {name} registered successfully with ID {donor_id}."

    return render_template('donor_register.html')


# --- DEFAULT ROUTE ---
@app.route('/')
def index():
    return redirect(url_for('login'))


# --- MAIN ---
if __name__ == '__main__':
    app.run(debug=True)




