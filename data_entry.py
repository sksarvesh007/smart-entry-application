import os
import sqlite3

def create_database():
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

def add_student(roll_number, phone_number, name):
    # Connect to SQLite database
    conn = sqlite3.connect('database/student_database.db')
    cursor = conn.cursor()

    try:
        # Insert student information into the database
        cursor.execute('''INSERT INTO students (roll_number, phone_number, name)
                          VALUES (?, ?, ?)''', (roll_number, phone_number, name))
        print("Student information added successfully!")
    except sqlite3.IntegrityError:
        print("Roll number already exists! Please try again.")

    # Commit changes and close connection
    conn.commit()
    conn.close()

def main():
    create_database()

    while True:
        # Get input from user
        roll_number = input("Enter roll number (or 0 to exit): ")
        if roll_number == '0':
            break
        
        phone_number = input("Enter phone number: ")
        name = input("Enter name: ")

        # Add student information to the database
        add_student(roll_number, phone_number, name)

if __name__ == "__main__":
    main()
