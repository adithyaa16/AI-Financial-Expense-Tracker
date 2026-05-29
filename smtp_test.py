import smtplib
from email.message import EmailMessage

sender = "adithyadinesh1316@gmail.com"
password = "ppqjaigldtizorug"

msg = EmailMessage()
msg["Subject"] = "SMTP Test"
msg["From"] = sender
msg["To"] = "adithyadinesh1316@gmail.com"

msg.set_content("SMTP is working!")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(sender, password)
    smtp.send_message(msg)

print("Email Sent Successfully!")