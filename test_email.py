import smtplib, ssl
from email.message import EmailMessage

SMTP_SERVER = "smtp.zoho.com"      # or "smtppro.zoho.com" for paid org
SMTP_PORT   = 465                  # 465=SSL, or use 587 with STARTTLS
USERNAME    = "info@webhostera.pk" # full email
PASSWORD    = "H8cCdibZCNLR"  # app-specific if 2FA is on




def send_email(receiver, subject, body):
    msg = EmailMessage()
    msg["From"] = USERNAME
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    ctx = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ctx) as s:
            s.login(USERNAME, PASSWORD)
            s.send_message(msg)
        print(f"✅ Email successfully sent to {receiver}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    send_email(
        "waqarazeem54@gmail.com",
        "Python File SMTP Test",
        "Hello from Python via Zoho SMTP!"
    )