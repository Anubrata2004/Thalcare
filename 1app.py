from flask import Flask, render_template_string, request, redirect
import sqlite3
import uuid
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def insert_patient(data):
    conn = sqlite3.connect('thalcare.db')
    c = conn.cursor()
    c.execute('INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def insert_donor(data):
    conn = sqlite3.connect('thalcare.db')
    c = conn.cursor()
    c.execute('INSERT INTO donors VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def insert_hospital(data):
    conn = sqlite3.connect('thalcare.db')
    c = conn.cursor()
    c.execute('INSERT INTO hospitals VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '''<h2>Welcome to ThalCare Registration</h2>
    <ul>
        <li><a href="/register/patient">Register as Patient</a></li>
        <li><a href="/register/donor">Register as Donor</a></li>
        <li><a href="/register/hospital">Register as Hospital</a></li>
        <li><a href="/view">View All Data</a></li>
    </ul>'''

@app.route('/register/patient', methods=['GET', 'POST'])
def reg_patient():
    if request.method == 'POST':
        uid = str(uuid.uuid4())
        data = (
            uid,
            request.form['name'],
            request.form['email'],
            request.form['password'],
            request.form['phone'],
            request.form['dob'],
            request.form['blood_group'],
            request.form['location'],
            'patient',
            request.form['last_required'],
            request.form['next_required']
        )
        insert_patient(data)
        return f'<h3>Patient Registered! Unique ID: {uid}</h3><a href="/">Back</a>'
    return render_template_string(open('register_patient.html').read())

@app.route('/register/donor', methods=['GET', 'POST'])
def reg_donor():
    if request.method == 'POST':
        uid = str(uuid.uuid4())
        data = (
            uid,
            request.form['name'],
            request.form['email'],
            request.form['password'],
            request.form['blood_group'],
            request.form['last_donation'],
            request.form['diseases'],
            request.form.get('availability', 'no'),
            'donor',
            request.form['location'],
            request.form['phone']
        )
        insert_donor(data)
        return f'<h3>Donor Registered! Unique ID: {uid}</h3><a href="/">Back</a>'
    return render_template_string(open('register_donor.html').read())

@app.route('/register/hospital', methods=['GET', 'POST'])
def reg_hospital():
    if request.method == 'POST':
        uid = str(uuid.uuid4())
        data = (
            uid,
            request.form['name'],
            request.form['email'],
            request.form['password'],
            request.form['license_id'],
            'hospital',
            request.form['location']
        )
        insert_hospital(data)
        return f'<h3>Hospital Registered! Unique ID: {uid}</h3><a href="/">Back</a>'
    return render_template_string(open('register_hospital.html').read())

@app.route('/view')
def view_data():
    conn = sqlite3.connect('thalcare.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patients')
    patients = c.fetchall()
    c.execute('SELECT * FROM donors')
    donors = c.fetchall()
    c.execute('SELECT * FROM hospitals')
    hospitals = c.fetchall()
    conn.close()
    return render_template_string(open('view_data.html').read(), patients=patients, donors=donors, hospitals=hospitals)


@app.route('/book_ambulance/<hospital_id>')
def book_ambulance(hospital_id):
    # Fetch hospital name
    conn1 = sqlite3.connect('hospitals.db')
    c1 = conn1.cursor()
    c1.execute("SELECT name FROM hospitals WHERE id = ?", (hospital_id,))
    hospital = c1.fetchone()
    conn1.close()

    # Fetch available drivers
    conn2 = sqlite3.connect('ambulance.db')
    c2 = conn2.cursor()
    c2.execute("SELECT name, phone, ambulance_plate FROM drivers WHERE hospital_id = ? AND available = 'yes'", (hospital_id,))
    drivers = c2.fetchall()
    conn2.close()

    return render_template('booking_page.html', hospital=hospital[0], drivers=drivers)

if __name__ == '__main__':
    app.run(debug=True)
