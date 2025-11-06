from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.task import Task
from schemas.task import TaskCreate, TaskOut

# Yeh router "Tasks" ke liye saare endpoints handle karega
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# ✅ Common helper function for same response structure
def make_response(message, data=None):
    return {
        "status": "success",
        "message": message,
        "data": data
    }

# 🟢 Route 1: Create a new task
@router.post("/create")
def create_task(request: TaskCreate, db: Session = Depends(get_db)):
    """
    Step by step:
    1. User se task ka data aayega (project_id, title, due_date, etc.)
    2. Us data se ek naya Task object banayenge
    3. Database me save karenge
    4. Success message aur saved task ka data return karenge
    """

    # 1️⃣ Naya task object bana lo user ke input se
    new_task = Task(**request.dict())

    # 2️⃣ Database me save karo
    db.add(new_task)
    db.commit()

    # 3️⃣ Refresh taake latest ID mil jaye
    db.refresh(new_task)

    # 4️⃣ Return success message aur task data
    return make_response(
        "New task created successfully!",
        TaskOut.from_orm(new_task).dict()
    )


# 🔵 Route 2: List all active tasks
@router.get("/list")
def list_tasks(db: Session = Depends(get_db)):
    """
    Step by step:
    1. Database se sab tasks laao jinka 'is_deleted = 0' hai
    2. Unko readable dict me convert karo
    3. Return karo success message ke sath
    """

    # 1️⃣ Active tasks laao
    tasks = db.query(Task).filter(Task.is_deleted == 0).all()

    # 2️⃣ Har task ko dict me convert karo
    task_list = [TaskOut.from_orm(t).dict() for t in tasks]

    # 3️⃣ Return success response
    return make_response(
        "All active tasks fetched successfully!",
        task_list
    )
