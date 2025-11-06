# database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Apni DB URL yahan set karein
# Agar XAMPP/MariaDB custom port (e.g., 3307) hai to port update kar dein.
DB_URL = "mysql+pymysql://root:@localhost:3306/freelance_project_tracker"

engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Optional: simple connectivity check at startup (import in main.py & call) ---
def check_connection():
    print(f"🔗 Using DB URL: {engine.url}")
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ Database connection successful!")
