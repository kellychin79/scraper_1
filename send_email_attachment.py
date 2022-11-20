# https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/
# https://realpython.com/python-send-email/

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
today = datetime.date.today()

filename = 'results.txt' # In same directory as script
port = 587  # For starttls
smtp_server ='smtp.gmail.com'
sender_email = 'XXX@gmail.com'
password = 'APP PASSWORD' # app password generated through Google Account > Security > App passwords > Other 
mailingList = ['YYY@gmail.com', 'ZZZ@gmail.com']
subject = today.strftime("%m/%d/%Y")+' - 3D Printer Pricing'

for i in range(0, len(mailingList)):
    receiver_email = mailingList[i]

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # string to store the body of the mail
    body = "The requested pricing data is attached."

    # Add body to email
    msg.attach(MIMEText(body, 'plain'))

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part 
    part.add_header(
            'Content-Disposition', 
            'attachment; filename= %s' % filename
        )

    # Add attachment to message and convert message to string
    msg.attach(part)
    text = msg.as_string()

    # Log in to server using secure context and send email
    # creates SMTP session 
    server = smtplib.SMTP(smtp_server, port)

    # start TLS for security
    server.starttls()

    # Authentication
    server.login(sender_email, password)    

    # sending the mail
    server.sendmail(sender_email, receiver_email, text)

    # terminating the session
    server.quit()
