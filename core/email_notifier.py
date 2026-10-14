import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(subject, body, to_email):
    # إعدادات خادم البريد (يمكن ضبط المتغيرات البيئية لاحقاً)
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SENDER_EMAIL", "")
    sender_password = os.getenv("SENDER_PASSWORD", "")

    if not sender_email or not sender_password:
        print(f"[*] [Simulated Email Alert to {to_email}]: {subject} - {body}")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"[*] Email alert successfully sent to {to_email}")
        return True
    except Exception as e:
        print(f"[!] Failed to send email alert: {e}")
        return False

if __name__ == "__main__":
    print("==================================================================")
    print("      AD ASTRA - EMAIL NOTIFIER MODULE                           ")
    print("      Owner: Abdallah Ben Belgacem                                 ")
    print("==================================================================")
    send_email_alert(
        "Ad Astra Autonomous Core - System Alert",
        "Hello Abdallah, your core infrastructure is operating successfully and logging transactions securely.",
        "abdallah.ben.belgacem@example.com"
    )
