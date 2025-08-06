from flask import Flask, render_template, request
import sqlite3
import uuid

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
        id TEXT PRIMARY KEY,
        org_type TEXT,
        contact TEXT,
        email TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    org_type = request.form['org_type']
    contact = request.form['contact']
    email = request.form['email']
    admin_id = str(uuid.uuid4())[:8]  # short unique ID

    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admins (id, org_type, contact, email) VALUES (?, ?, ?, ?)",
                   (admin_id, org_type, contact, email))
    conn.commit()
    conn.close()

    return f"✅ Registered Successfully!<br>🆔 Admin ID: <strong>{admin_id}</strong>"

if __name__ == '__main__':
    app.run(debug=True)
