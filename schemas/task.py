from pydantic import BaseModel
from typing import Optional
from datetime import date

# 🟢 Input Schema: jab user new task create karta hai
class TaskCreate(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None
    completed: Optional[bool] = False

    class Config:
        from_attributes = True  # ✅ v2


# 🔵 Output Schema: jab API task ka data return karti hai
class TaskOut(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None
    completed: bool
    is_deleted: int

    class Config:
        from_attributes = True  # ✅ v2
