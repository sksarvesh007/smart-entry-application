# SMART ENTRY EXIT APPLICATION

This project is designed to detect roll numbers from live video feed, capture the frame with the best quality containing the roll number, and then send a WhatsApp notification to the corresponding student with their information using the student database.

## INSTALLATION

1. Open your terminal or command prompt.
2. Navigate to your project directory.
3. Run the following code in the terminal/command prompt

   ```
   pip install -r requirements.txt
   ```

## SETUP YOUR TWILIO

* Create a Twilio account if you don't have one already.
* Obtain your Account SID, Auth Token, and Twilio phone number.
* Create a `.env` file in the project directory.
* Add the following lines to the `.env` file and replace the placeholders with your Twilio credentials:

  ```
  TWILIO_ACCOUNT_SID=your_account_sid
  TWILIO_AUTH_TOKEN=your_auth_token
  TWILIO_PHONE_NUMBER=your_twilio_phone_number
  ```
