import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_user(receiver_email, subject, body):
    # Replace these variables with your actual email credentials and details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "shubham.kothari432@gmail.com"
    sender_password = "bhtfwfcluuenamia"
    html_content = body
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # HTML Content
        message.attach(MIMEText(html_content, "html"))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)


