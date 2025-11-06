from fastapi import APIRouter, BackgroundTasks
from datetime import datetime
from pathlib import Path

router = APIRouter(prefix="/background", tags=["Background Tasks"])

# LOG_FILE = Path(__file__).resolve().parent.parent / "log.txt"  # project root/log.txt

# def write_notification(email: str, message: str = ""):
#     LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
#     with open(LOG_FILE, mode="a", encoding="utf-8") as f:
#         ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         f.write(f"[{ts}] Notification for {email}: {message}\n")
        
def write_notification(email: str, message=""):
    for i in range(200_000):
        print(f"Preparing notification {i} for {email}")
        
    # with open("log.txt", mode="w") as email_file:
    #     content = f"notification for {email}: {message}"
    #     email_file.write(content)


# for i in range(20_000):
#     write_notification(f"user{i}@example.com", f"test message {i}")

@router.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": f"Notification scheduled for {email}"}
