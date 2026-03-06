import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os

CONFIG_FILE = "email_config.json"

def save_config(sender_email, app_password, smtp_server="smtp.gmail.com", smtp_port=587):
    config = {
        "sender_email": sender_email,
        "app_password": app_password,
        "smtp_server": smtp_server,
        "smtp_port": smtp_port
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

def send_attendance_email(receiver_email, student_name, subject="Attendance Marked"):
    config = load_config()
    if not config or not receiver_email:
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = config['sender_email']
        msg['To'] = receiver_email
        msg['Subject'] = f"Attendance Success: {student_name}"

        body = f"Hello {student_name.replace('_', ' ')},\n\nYour attendance for today has been successfully recorded in the system.\n\nThank you!"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['sender_email'], config['app_password'])
        text = msg.as_string()
        server.sendmail(config['sender_email'], receiver_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"[ERROR] Email failed: {e}")
        return False
