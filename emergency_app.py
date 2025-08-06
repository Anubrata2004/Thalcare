from flask import Flask, request, jsonify
import sqlite3
import uuid
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import json

app = Flask(__name__)

# --------------------- Setup Emergency DB ---------------------
def setup_emergency_db():
    conn = sqlite3.connect("emergency.db")
    c = conn.cursor()
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
    conn.commit()
    conn.close()

setup_emergency_db()

# --------------------- Emergency Request Page ---------------------
@app.route('/emergency_request')
def emergency_form():
    with open("emergency_request.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route('/submit_emergency', methods=["POST"])
def submit_emergency():
    name = request.form['name']
    contact = request.form['contact']
    blood_group = request.form['blood_group']
    location = request.form['location']
    urgency_level = request.form['urgency_level']

    unique_id = str(uuid.uuid4())[:8]
    request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("emergency.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO emergency_requests (id, name, blood_group, location, urgency_level, contact, request_time, fulfilled)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (unique_id, name, blood_group, location, urgency_level, contact, request_time, "no"))
    conn.commit()
    conn.close()

    return f"<h2>Request submitted!</h2><p>Tracking ID: <strong>{unique_id}</strong></p>"

# --------------------- View Emergency Requests ---------------------
@app.route('/view_emergency')
def view_emergency():
    conn = sqlite3.connect("emergency.db")
    c = conn.cursor()
    c.execute("SELECT * FROM emergency_requests")
    data = c.fetchall()
    conn.close()

    rows_html = ""
    for row in data:
        rows_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"

    with open("view_emergency.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    return html_template.replace("{{rows}}", rows_html)

# --------------------- Hospital Map Page ---------------------
@app.route('/hospital_map')
def hospital_map():
    with open("hospital_map.html", "r", encoding="utf-8") as f:
        return f.read()

# --------------------- Get Hospitals ---------------------
@app.route('/get_hospitals')
def get_hospitals():
    conn = sqlite3.connect("hospitals.db")
    c = conn.cursor()
    c.execute("SELECT * FROM hospitals")
    rows = c.fetchall()
    conn.close()

    hospitals = []
    for row in rows:
        hospitals.append({
            "id": row[0],
            "name": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "phone": row[4],
            "distance": row[5],
            "ambulance_status": row[6]
        })

    return json.dumps(hospitals)

# --------------------- Get Drivers ---------------------
@app.route('/get_drivers/<hospital_id>')
def get_drivers(hospital_id):
    conn = sqlite3.connect("ambulance.db")
    c = conn.cursor()
    c.execute("SELECT name, phone, ambulance_plate FROM drivers WHERE hospital_id = ? AND available = 'yes'", (hospital_id,))
    drivers = c.fetchall()
    conn.close()

    return jsonify({
        "drivers": [
            {"name": d[0], "phone": d[1], "plate": d[2]}
            for d in drivers
        ]
    })



# --------------------- Notify Donors ---------------------
import smtplib
from email.mime.text import MIMEText

@app.route('/notify_donors', methods=['POST'])
def notify_donors():
    # Step 1: Get the latest emergency request
    conn1 = sqlite3.connect('emergency.db')
    c1 = conn1.cursor()
    c1.execute("SELECT blood_group, contact FROM emergency_requests ORDER BY request_time DESC LIMIT 1")
    result = c1.fetchone()
    conn1.close()

    if not result:
        return "No emergency requests found."

    blood_group, contact = result

    # Step 2: Fetch matching donors
    conn2 = sqlite3.connect('thalcare.db')
    c2 = conn2.cursor()
    c2.execute("SELECT email FROM donors WHERE blood_group = ? AND availability = 'yes'", (blood_group,))
    donor_emails = c2.fetchall()
    conn2.close()

    # Step 3: Email each donor
    sender_email = "anubratamondal475@gmail.com"
    app_password = "sjta erxd cols rykt"  # App password

    subject = "🚨 Urgent Blood Needed"
    body = f"A patient needs {blood_group} blood urgently.\nIf you are available, please call {contact} immediately."

    for email_tuple in donor_emails:
        recipient = email_tuple[0]

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, app_password)
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")

    return "Emails successfully sent to matching donors"
# --------------------- Start App ---------------------
if __name__ == '__main__':
    print("Routes:")
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(port=5001, debug=True)
app.run(debug=False)