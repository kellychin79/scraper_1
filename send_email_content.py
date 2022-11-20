# https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/
# https://realpython.com/python-send-email/
# https://stackoverflow.com/questions/38275467/send-table-as-an-email-body-not-attachment-in-python
from tabulate import tabulate
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
mailingList = ['YYY@gmail.com', "ZZZ@gmail.com"]

for i in range(0, len(mailingList)):
    receiver_email = mailingList[i]

    # sends the message in the typical plain text and html multipart/alternative format.
    text = """
    Hello, Friend.

    Here is your data:

    {table}

    Cheers,

    Kelly"""

    html = """
    <html><body><p>Hello, Friend.</p>
    <p>Here is your data:</p>
    {table}
    <p>Cheers,</p>
    <p>Kelly</p>
    </body></html>
    """

    # Open the file
    with open(filename, "r") as f:
        raw_data = f.readlines()
        data = []
        for i in raw_data: 
            if '300*300*300mm,Dragon High Flow,United States,$899.00' in i:
                d = (i+', **Your Target').split(',')
                data.append(d)
                target_price = d[3]
            else:
                data.append((i+', ').split(','))

    text = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
    html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))
    
    subject = today.strftime("%m/%d/%Y") +' - 300mm Dragon High Flow from US' + target_price

    # Create a multipart message and set headers
    msg = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html,'html')])
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Log in to server using secure context and send email
    # creates SMTP session 
    server = smtplib.SMTP(smtp_server, port)

    # start TLS for security
    server.starttls()

    # Authentication
    server.login(sender_email, password)    

    # sending the mail
    server.sendmail(sender_email, receiver_email, msg.as_string())

    # terminating the session
    server.quit()
