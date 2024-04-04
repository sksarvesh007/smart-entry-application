import os
import sqlite3

# Create a directory named 'database' if it doesn't exist
database_dir = 'database'
if not os.path.exists(database_dir):
    os.makedirs(database_dir)

# Path to the SQLite database file
database_path = os.path.join(database_dir, 'student_database.db')

# Connect to SQLite database (or create if not exists)
conn = sqlite3.connect(database_path)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store student information
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    roll_number TEXT PRIMARY KEY,
                    phone_number TEXT,
                    name TEXT
                )''')

# Commit changes and close connection
conn.commit()
conn.close()
