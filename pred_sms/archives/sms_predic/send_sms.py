from twilio.rest import Client

account_sid = 'sid'
auth_token = 'tok'

client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='n0',
         to='n1'
     )

# to message multiple clients
numbers_to_message = ['n1', 'n2']
for number in numbers_to_message:
    client.messages.create(
        body='Hello from mummuss Twilio number!\nThis is the ship that made the Kessel Run in fourteen parsecs?',
        from_='n0',
        to=number
    )

print("message sid: ", message.sid)
print("message status: ", message.status)
print("message: ", message)
