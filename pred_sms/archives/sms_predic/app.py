import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import mysql.connector

class MyApp(Flask):

    def index(self):
        return 'Hello, World'
        
    def sms_reply(self):
        if request.method == 'POST':
            # Handle POST requests (incoming SMS messages)
            # Get the incoming SMS message data
            sender = request.form.get('From')
            message_body = request.form.get('Body')

            # Store the SMS message in the database
            cursor = self.db.cursor()

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
            self.db.commit()
            cursor.close()

            # Respond to the SMS with a simple message
            resp = MessagingResponse()
            resp.message("Thank you for your message!")

            return str(resp)
        else:
            # Handle GET requests
            return 'This is the SMS endpoint'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MySQL database connection
        self.db = mydb = mysql.connector.connect(
            host="",
            user="",
            password="",
            database=""
        )

        # Root URL handler
        # self.add_url_rule('/', view_func=self.index, methods=['GET'])
        self.route('/', methods=['GET'])(self.index)

        # Twilio webhook endpoint
        self.add_url_rule('/sms', view_func=self.sms_reply, methods=['GET', 'POST'])


app = MyApp(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

# GET POST PUT DELETE