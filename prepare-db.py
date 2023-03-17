import psycopg2

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'PASSWORD'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_DB = 'postgres'

# Connect to the default "postgres" database to create the "cmdb" database
conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)

# Create the "cmdb" database if it doesn't exist
conn.autocommit = True
with conn.cursor() as cursor:
    cursor.execute(f"CREATE DATABASE {POSTGRES_DB} ENCODING 'utf8'")
print("Database created successfully")

# Close the connection to the default "postgres" database and connect to the "cmdb" database
conn.close()
conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)

# Create the "hosts" table
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

# Close the connection to the "cmdb" database
conn.close()
