import os
import sqlite3
database_dir = 'database'
if not os.path.exists(database_dir):
    os.makedirs(database_dir)

database_path = os.path.join(database_dir, 'student_database.db')

conn = sqlite3.connect(database_path)

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    roll_number TEXT PRIMARY KEY,
                    phone_number TEXT,
                    name TEXT
                )''')

conn.commit()
conn.close()
