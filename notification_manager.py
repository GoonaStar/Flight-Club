from twilio.rest import Client
import smtplib
import os

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = "+15415834773"
TWILIO_VERIFIED_NUMBER = os.environ.get("MY_NUMBER")

MY_EMAIL = "thibtiger92@gmail.com"
class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)

    def send_emails(self, email_address, message, flight_link, name):
        emoji = "✈️"
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password="ursule92")
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=email_address,
                                msg=f"Subject: Low price alert {emoji.encode('utf-8')} \n\n Dear {name},\n{message}\n {flight_link}")
