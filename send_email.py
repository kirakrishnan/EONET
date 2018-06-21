#############################################################
# This program will prompt for the sender email address,    #
# sender password and receiver email address. Then sends    #
# the data.csv file to the receiver. After successful       #
# completion prints Email sent successfully                 #
#############################################################

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = input("enter the sender email address")#"konety.jayalakshmi@gmail.com"
pwd = input("enter the sender password")
email_send = input("enter the receiver email address")#"aravindakrishnan92@gmail.com"
subject = "Details about the wildfires, severe storms, and landslides from the past month"

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['subject'] = subject

body = "Hi Please find attached csv file with requested data"
msg.attach(MIMEText(body,'plain'))

filename = 'data.csv'
attachment = open(filename,'rb')

part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename="+filename)

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,pwd)

server.sendmail(email_user,email_send,text)
server.quit()
print("Email sent successfully")