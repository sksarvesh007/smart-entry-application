import cv2
import pytesseract
from PIL import Image
import numpy as np
import os
from twilio.rest import Client
from datetime import datetime
import sqlite3
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

# Load face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load college logo detection model (You need to replace 'logo_detection_model_path' with the actual path of your logo detection model)
logo_detection_model_path = 'logo_detection_model_path' 

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def detect_face(image):
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(faces) > 0

def detect_logo(image):
    # Logic to detect the college logo using a pre-trained model
    # Load and apply your logo detection model here
    # You can use any pre-trained logo detection model or train your own
    # Placeholder logic:
    # logo_detected = detect_logo_with_model(image, logo_detection_model_path)
    logo_detected = True  # Placeholder logic, replace with actual detection
    return logo_detected

def rollnofinder(image):
    myconfig = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(Image.fromarray(image), config=myconfig)
    words = text.split()
    rollno = ""
    for word in words:
        if len(word) == 10 and word.startswith('BT') and word[2:4].isdigit() and word[4:7] in ['CSD', 'CSE', 'CSA', 'ECE', 'CSH', 'ECI'] and word[7:].isdigit():
            rollno = word
            break  
    return rollno

def get_student_info(roll_number):
    conn = sqlite3.connect('database/student_database.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT phone_number, name FROM students WHERE roll_number = ?''', (roll_number,))
    student_info = cursor.fetchone()
    print(student_info)
    conn.close()

    return student_info

cap = cv2.VideoCapture(1)

frame_count = 0
best_frame = None
best_rollno = ""

while True: 
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture frame")
        break
    
    processed_frame = preprocess_image(frame)
    cv2.imshow('frame', frame)
    
    rollno = rollnofinder(processed_frame)
    face_detected = detect_face(processed_frame)
    logo_detected = detect_logo(processed_frame)
    
    if rollno and face_detected and logo_detected:
        best_frame = frame
        best_rollno = rollno
        break
    
    frame_count += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
if best_rollno:
    print("Detected Roll Number:", best_rollno)
else:
    print("Roll number not detected")

if best_frame is not None:
    cv2.imwrite('images/image.jpg', best_frame)
    cv2.imshow('Best Frame', best_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    student_info = get_student_info(best_rollno)
    if student_info:
        student_phone_number, student_name = student_info

        time_of_exit = datetime.now().strftime("%H:%M:%S")

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message_body = f"Hello {student_name} , your roll no :  {best_rollno}  , Time of exit :  {time_of_exit}."
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=student_phone_number
        )
        print("WhatsApp message sent to", student_phone_number)
    else:
        print("Student information not found in the database.")

cap.release()
