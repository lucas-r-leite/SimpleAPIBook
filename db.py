from dotenv import load_dotenv
import os
import sys
import mariadb

load_dotenv()

# Database configuration
DATABASE_HOST = "0.0.0.0"  # Replace with the IP of your MariaDB container
DATABASE_USER = os.getenv("DB_USER")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_DB = os.getenv("DB_NAME")


# Connect to MariaDB
try:
    conn = mariadb.connect(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=3306,  # MariaDB default port
        database=DATABASE_DB,
    )
    cursor = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

# Define the Books table creation SQL query
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    author VARCHAR(30) NOT NULL
)
"""

# Execute the table creation query
try:
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    print("Books table created successfully.")
except mariadb.Error as e:
    print(f"Error creating Books table: {e}")
conn.rollback()
