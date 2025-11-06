from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.project import Project
from schemas.project import ProjectCreate, ProjectOut

# Yeh route group "Projects" ke sab endpoints rakhta hai
router = APIRouter(prefix="/projects", tags=["Projects"])

# ✅ Common function: har response same format me bhejna
def ok(message, data=None):
    return {
        "status": "success",
        "message": message,
        "data": data
    }


# 🟢 ROUTE 1: Create a new project
@router.post("/create")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    """
    Step by step:
    1. User se project ka data milega (title, description, client_id, etc.)
    2. Us data se ek naya Project object banayenge
    3. Database me save karenge
    4. Return karenge success message aur saved project ka data
    """

    # 1️⃣ User ke input se ek project object bana lo
    project = Project(**payload.dict())

    # 2️⃣ Database me save karo
    db.add(project)
    db.commit()

    # 3️⃣ Refresh karo taake latest ID waghera mil jaye
    db.refresh(project)
    # 4️⃣ Response bhejo with created project data
    
    out = ProjectOut.model_validate(project, from_attributes=True).model_dump()
    return ok("Project created", out)
    

# 🔵 ROUTE 2: List all projects
@router.get("/list")
def list_projects(db: Session = Depends(get_db)):
    """
    Step by step:
    1. Database se sab projects laao jinka 'is_deleted = 0' hai
    2. Unko readable format me convert karo (dict)
    3. Return karo success message ke sath
    """

    # 1️⃣ Database se active projects laao
    projects = db.query(Project).filter(Project.is_deleted == 0).all()

    # 2️⃣ Har project ko simple dict me convert karo
    project_list = [ProjectOut.from_orm(p).dict() for p in projects]

    # 3️⃣ Return response
    return ok(
        "All active projects fetched successfully!",
        project_list
    )
