# main.py
# ────────────────────────────────────────────────────────────────
# PURPOSE:
#   Ye app ka main entry point hai.
#   - FastAPI instance create karta hai
#   - Static files aur templates mount karta hai
#   - Routers include karta hai (API + UI)
#   - Startup event pe DB connection check karta hai
# ────────────────────────────────────────────────────────────────

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from database import engine
from routers import background_task, projects, tasks, invoices, frontend, client, emailer    # import routers

# 1️⃣ FastAPI app initialize karte hain
app = FastAPI(title="Freelance Tracker")

# 2️⃣ Static directory mount karna (images, CSS, JS ke liye)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3️⃣ Template engine setup (Jinja2)
templates = Jinja2Templates(directory="templates")
app.state.templates = templates  # store in app.state for use in routers

# 4️⃣ Routers include (API + UI routes)
app.include_router(frontend.router)   # /ui/projects (HTML frontend)
app.include_router(client.router)     # /clients/... (JSON + HTML view)
app.include_router(projects.router)   # /projects/... (JSON API)
app.include_router(tasks.router)      # /tasks/... (JSON API)
app.include_router(background_task.router)  # /send-notification/...
app.include_router(emailer.router)
# app.include_router(invoices.router) # optional enable later

# 5️⃣ App startup pe database test karte hain (for early failure detection)
@app.on_event("startup")
def startup_event():
    print("🔍 Checking database connection...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            if result == 1:
                print("✅ Database connection successful!")
            else:
                print("⚠️ Database responded unexpectedly.")
    except OperationalError as e:
        print("❌ Database connection failed!")
        print("Error details:", e)
        raise e
