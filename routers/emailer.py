from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib, ssl
from email.message import EmailMessage
import os

router = APIRouter(prefix="/email", tags=["Email"])

# ---- Config (env vars recommended) ----
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.zoho.com")      # or "smtppro.zoho.com"
SMTP_PORT   = int(os.getenv("SMTP_PORT", "465"))             # 465=SSL, 587=STARTTLS
USERNAME    = os.getenv("SMTP_USERNAME", "you@yourdomain.com")
PASSWORD    = os.getenv("SMTP_PASSWORD", "your_app_password")
SENDER      = os.getenv("SENDER_EMAIL", USERNAME)

class EmailRequest(BaseModel):
    receiver: EmailStr
    subject: str = "Hello"
    body: str = "Test"

def send_email_now(receiver: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = SENDER
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    ctx = ssl.create_default_context()

    # Choose SSL (465) or STARTTLS (587) automatically based on port
    if SMTP_PORT == 465:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ctx) as s:
            s.login(USERNAME, PASSWORD)
            s.send_message(msg)
    else:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as s:
            s.ehlo()
            s.starttls(context=ctx)
            s.ehlo()
            s.login(USERNAME, PASSWORD)
            s.send_message(msg)

@router.post("/send")
async def send_email_api(payload: EmailRequest, background_tasks: BackgroundTasks):
    try:
        # Run in background so API responds immediately
        background_tasks.add_task(
            send_email_now, payload.receiver, payload.subject, payload.body
        )
        return {
            "status": "scheduled",
            "to": payload.receiver,
            "via": f"{SMTP_SERVER}:{SMTP_PORT}",
        }
    except Exception as e:
        # If scheduling itself fails
        raise HTTPException(status_code=500, detail=f"Failed to schedule email: {e}")

@router.get("/health")
async def email_health():
    return {"smtp_server": SMTP_SERVER, "port": SMTP_PORT, "sender": SENDER}
