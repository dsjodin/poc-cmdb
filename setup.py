# This script installs and configures a PostgreSQL database for use with a the example application.
# The script creates a new database called "cmdb" and a new table called "hosts" with the required columns.
# It also prompts the user to enter a PostgreSQL password and updates the password in the cmdb_app.py file.

# 1. Open a terminal window and navigate to the directory where the script is saved.
# 2. Run the script by typing "python3 setup.py" and pressing Enter.
# 3. When prompted, enter a PostgreSQL password and press Enter.
# 4. Wait for the script to complete. The script will install PostgreSQL and psycopg2, create a new database called "cmdb", create a new table called "hosts", and update the password in the cmdb_app.py file.

import subprocess
import psycopg2
import os

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = None
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_DB = 'postgres'

def prompt_for_password():
    global POSTGRES_PASSWORD
    while not POSTGRES_PASSWORD:
        POSTGRES_PASSWORD = input("Please enter a password for the PostgreSQL user: ")
    print("Password set.")

def update_cmdb_app_password(password):
    cmdb_app_file = 'cmdb_app.py'
    if os.path.isfile(cmdb_app_file):
        with open(cmdb_app_file, 'r') as file:
            content = file.read()
        content = content.replace("POSTGRES_PASSWORD = 'PASSWORD'", f"POSTGRES_PASSWORD = '{password}'")
        with open(cmdb_app_file, 'w') as file:
            file.write(content)
        print("Updated password in cmdb_app.py")
    else:
        print("cmdb_app.py not found in the current directory")

def install_dependencies():
    subprocess.run(['sudo', 'apt-get', 'update', '-y'])
    subprocess.run(['sudo', 'apt-get', 'install', 'postgresql', '-y'])
    subprocess.run(['sudo', 'apt-get', 'install', 'python3-pip', '-y'])
    subprocess.run(['sudo', 'apt-get', 'install', 'python3-psycopg2', '-y'])

def create_database():
    conn = psycopg2.connect(
        dbname='postgres',
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE {POSTGRES_DB} ENCODING 'utf8'")
    print("Database created successfully")
    conn.close()

def create_table():
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE hosts (
                id SERIAL PRIMARY KEY,
                hostname VARCHAR(255) NOT NULL,
                ip_address VARCHAR(255) NOT NULL,
                owner VARCHAR(255) NOT NULL,
                time_of_creation TIMESTAMP NOT NULL DEFAULT NOW(),
                deployment VARCHAR(255) NOT NULL
            );
        """)
    print("Table created successfully")
    conn.close()

if __name__ == "__main__":
    prompt_for_password()
    install_dependencies()
    create_database()
    create_table()
    update_cmdb_app_password(POSTGRES_PASSWORD)

