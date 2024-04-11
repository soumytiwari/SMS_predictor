import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import mysql.connector

app = Flask(__name__)

# MySQL database connection
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# Twilio webhook endpoint
@app.route('/sms', methods=['POST'])
def sms_reply():
    # Get the incoming SMS message data
    sender = request.form.get('From')
    message_body = request.form.get('Body')

    # Store the SMS message in the database
    cursor = db.cursor()

    # Check if the phone number exists in the phone_table
    check_phone_query = "SELECT p_id, u_id FROM phone_table WHERE p_no = %s"
    cursor.execute(check_phone_query, (sender,))
    result = cursor.fetchone()

    if result:
        # Phone number exists, get the p_id and u_id
        p_id, u_id = result
    else:
        # Phone number doesn't exist, insert a new record into phone_table
        insert_phone_query = "INSERT INTO phone_table (p_no) VALUES (%s)"
        cursor.execute(insert_phone_query, (sender,))
        p_id = cursor.lastrowid
        u_id = None

    # Insert the message into the message_table
    insert_message_query = "INSERT INTO message_table (p_id, m_txt) VALUES (%s, %s)"
    cursor.execute(insert_message_query, (p_id, message_body))
    m_id = cursor.lastrowid

    # Commit the changes and close the cursor
    db.commit()
    cursor.close()

    # Respond to the SMS with a simple message
    resp = MessagingResponse()
    resp.message("Thank you for your message!")

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)