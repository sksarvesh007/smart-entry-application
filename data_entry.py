import os
import sqlite3

def create_database():
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

def add_student(roll_number, phone_number, name):
    conn = sqlite3.connect('database/student_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO students (roll_number, phone_number, name)
                          VALUES (?, ?, ?)''', (roll_number, phone_number, name))
        print("Student information added successfully!")
    except sqlite3.IntegrityError:
        print("Roll number already exists! Please try again.")

    conn.commit()
    conn.close()

def main():
    create_database()

    while True:
        roll_number = input("Enter roll number (or 0 to exit): ")
        if roll_number == '0':
            break
        
        phone_number = input("Enter phone number: ")
        name = input("Enter name: ")

        add_student(roll_number, phone_number, name)

if __name__ == "__main__":
    main()
