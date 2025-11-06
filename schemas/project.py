from pydantic import BaseModel
from typing import Optional
from datetime import date

# Yeh class input validation ke liye use hoti hai jab user project create karta hai
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    client_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = "planned"
    budget: Optional[int] = None

    class Config:
        from_attributes = True


# Yeh class output ke liye use hoti hai jab API response bhejti hai
class ProjectOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    client_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    budget: Optional[int] = None
    is_deleted: int

    class Config:
     from_attributes = True
