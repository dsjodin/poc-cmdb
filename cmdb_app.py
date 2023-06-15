# This script creates a Flask application that connects to a PostgreSQL database and provides an interface for
# users to view, add, and delete host information from the "hosts" table.
# The application has several routes, including:

# The add_host route ("/api/hosts"): accepts a POST request with host information and adds it to the "hosts" table
# in the database

# The delete_host route ("/api/hosts/string:hostname"): accepts a DELETE request with a hostname parameter and deletes
# the corresponding host information from the "hosts" table in the database

# The list_hosts route ("/api/hosts"): returns a JSON object containing a list of all hosts in the "hosts" table in
# the database

# Ensure that the PostgreSQL database has been configured using 'setup.py'.
# Open a terminal window and navigate to the directory where the script is saved.
# Run the script by typing "python3 cmdb_app.py" and pressing Enter.
# Wait for the Flask application to start. The application will run on port 5000 by default.
# Open a web browser and navigate to "http://localhost:5000/" to view the host information table.

from flask import Flask, render_template_string, request, jsonify
import psycopg2
import os

POSTGRES_USER = os.environ["PSQL_USR"]
POSTGRES_PASSWORD = os.environ["PSQL_PWD"]
POSTGRES_HOST = os.environ["PSQL_HOST"]
POSTGRES_PORT = os.environ["PSQL_PORT"]
POSTGRES_DB = os.environ["PSQL_DB"]
VRA_FQDN = os.environ["VRA_FQDN"]

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )

@app.route("/")
def home():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Get the list of hosts
    cursor.execute("SELECT * FROM hosts;")
    hosts = cursor.fetchall()

    cursor.close()
    connection.close()

    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Host Information Table from Database</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                color: #212529;
            }
            header {
                background-color: #007bff;
                padding: 20px;
                text-align: center;
                color: #fff;
                font-size: 24px;
            }
            main {
                padding: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                padding: 10px;
                text-align: left;
                border: 1px solid #ccc;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <header>
            Host Information Table
        </header>
        <main>
            <table>
                <thead>
                    <tr>
                        <th>Hostname</th>
                        <th>IP Address</th>
                        <th>Owner</th>
                        <th>Time of Creation</th>
                        <th>Deployment</th>
                    </tr>
                </thead>
                <tbody>
                    {% for host in hosts %}
                        <tr>
                            <td>{{ host[1] }}</td>
                            <td>{{ host[2] }}</td>
                            <td>{{ host[3] }}</td>
                            <td>{{ host[4] }}</td>
                            <td><a href="https://{{ VRA_FQDN }}/catalog/#/workload/deployment/{{ host[5] }}" target="_blank">{{ host[5] }}</a></td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </main>
    </body>
    </html>
    '''

    return render_template_string(html_template, hosts=hosts)

@app.route("/api/hosts", methods=["POST"])
def add_host():
    data = request.get_json()

    hostname = data.get("hostname")
    ip_address = data.get("ip_address")  
    owner = data.get("owner")
    time_of_creation = data.get("time_of_creation")
    deployment = data.get("deployment")

    if not all([hostname, ip_address, owner, time_of_creation, deployment]):
        return jsonify({"error": "Missing or invalid data"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO hosts (hostname, ip_address, owner, time_of_creation, deployment)
        VALUES (%s, %s, %s, %s, %s);
    """, (hostname, ip_address, owner, time_of_creation, deployment))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Host added successfully"}), 201


# ...

@app.route("/api/hosts/<string:hostname>", methods=["DELETE"])
def delete_host(hostname):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM hosts WHERE hostname=%s;", (hostname,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Host deleted successfully"}), 200

# ...

@app.route("/api/hosts", methods=["GET"])
def list_hosts():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM hosts;")
    hosts = cursor.fetchall()
    cursor.close()
    connection.close()

    host_list = []
    for host in hosts:
        host_list.append({
            "id": host[0],
            "hostname": host[1],
            "ip_address": host[2],
            "owner": host[3],
            "time_of_creation": host[4],
            "deployment": host[5]
        })

    return jsonify(host_list)

# ...

if __name__ == '__main__':
    app.run(host='0.0.0.0')

