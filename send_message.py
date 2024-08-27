from twilio.rest import Client

account_sid = 'ACf3543a8ed2c3e7310ccd5623e22f6f3a'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+13344909970',
  to='+918077702252'
)

print(message.sid)



