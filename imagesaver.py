import cv2
import pytesseract
from PIL import Image
import numpy as np
import os
from twilio.rest import Client
from datetime import datetime
import os
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Twilio Account SID and Auth Token
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
RECIPIENT_PHONE_NUMBER = os.environ.get('RECIPIENT_PHONE_NUMBER')

# Verify that environment variables are set
if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, RECIPIENT_PHONE_NUMBER]):
    raise ValueError("Please set all required environment variables.")

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def rollnofinder(image):
    myconfig = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(Image.fromarray(image), config=myconfig)
    words = text.split()
    rollno = ""
    for word in words:
        # Check if word matches the roll number format
        if len(word) == 10 and word.startswith('BT') and word[2:4].isdigit() and word[4:7] in ['CSD', 'CSE', 'CSA', 'ECE', 'CSH'] and word[7:].isdigit():
            rollno = word
            break  # Exit loop once a potential roll number is found

    return rollno

# Use webcam
cap = cv2.VideoCapture(1)

# Capture frames for a certain duration
frame_count = 0
best_frame = None
best_rollno = ""

while True:  # Capture frames for a certain duration
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Check if frame is successfully captured
    if not ret:
        print("Failed to capture frame")
        break
    
    # Preprocess the captured frame
    processed_frame = preprocess_image(frame)
    cv2.imshow('frame', frame)
    
    # Find roll number
    rollno = rollnofinder(processed_frame)
    
    # Consider the frame if it contains a non-empty roll number
    if rollno:
        best_frame = frame
        best_rollno = rollno
        # Close the camera as soon as a roll number is detected
        break
    
    # Increment frame count
    frame_count += 1
    
    # Check for 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Print the detected roll number from the best frame
if best_rollno:
    print("Detected Roll Number:", best_rollno)
else:
    print("Roll number not detected")

# Save the best frame to the images folder as image.jpg
if best_frame is not None:
    cv2.imwrite('images/image.jpg', best_frame)
    cv2.imshow('Best Frame', best_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Send WhatsApp message with the image attachment
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Get the current time
    time_of_exit = datetime.now().strftime("%H:%M:%S")

    # Message to include in the WhatsApp message
    message_body = f"Roll Number: {best_rollno}\nTime of Exit: {time_of_exit}"
# Get the full path to the image file
    image_path = os.path.join(os.getcwd(), 'bus-tt', 'image.jpg')

    # Send WhatsApp message with image attachment
    message = client.messages.create(
        body=message_body,
        # media_url=['https://postimg.cc/wyHmdB60'],
        from_=TWILIO_PHONE_NUMBER,
        to=RECIPIENT_PHONE_NUMBER,
        # Use the full path to the image file
    )
    print("WhatsApp message sent with image attachment to", RECIPIENT_PHONE_NUMBER)

# Release the camera
cap.release()
