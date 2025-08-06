from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

# HTML template to display table data
template = '''
<!DOCTYPE html>
<html>
<head>
    <title>View Admins</title>
    <style>
        body {
            font-family: "Segoe UI", sans-serif;
            background: #f9f9f9;
            padding: 40px;
        }
        table {
            width: 90%;
            margin: auto;
            border-collapse: collapse;
            background: #fff;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 12px 18px;
            border: 1px solid #ddd;
            text-align: center;
        }
        th {
            background-color: #007bff;
            color: white;
        }
        tr:hover {
            background-color: #f2f2f2;
        }
        h2 {
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
    <h2>Registered Admins</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Organization Type</th>
            <th>Contact</th>
            <th>Email</th>
            
        </tr>
        {% for row in rows %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/view')
def view_data():
    conn = sqlite3.connect('admin.db')
    c = conn.cursor()
    c.execute('SELECT * FROM admins')
    rows = c.fetchall()
    conn.close()
    return render_template_string(template, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
