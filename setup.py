import subprocess
import psycopg2
import os

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = ''  # Leave this empty for now
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_DB = 'postgres'

# Prompt user to enter the password
POSTGRES_PASSWORD = input("Please enter a PostgreSQL password: ")

# Update the password in the cmdb_app.py file
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

# Install PostgreSQL and psycopg2 using apt-get and pip
def install_dependencies():
    subprocess.run(['sudo', 'apt-get', 'update', '-y'])
    subprocess.run(['sudo', 'apt-get', 'install', 'postgresql', '-y'])
    subprocess.run(['sudo', 'apt-get', 'install', 'python3-psycopg2', '-y'])

# Connect to the default "postgres" database to create the "cmdb" database
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

# Connect to the "cmdb" database and create the "hosts" table
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

# Call the functions to install dependencies, create the database, and create the table
if __name__ == "__main__":
    install_dependencies()
    create_database()
    create_table()
    update_cmdb_app_password(POSTGRES_PASSWORD)
