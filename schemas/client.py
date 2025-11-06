from pydantic import BaseModel
from typing import Optional

# Input schema (create/update me validate hota hai)
class ClientCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    address: Optional[str] = None

    class Config:
        # Pydantic v2: SQLAlchemy object se fields read karne ki ijazat
        from_attributes = True

# Output schema (API response me use)
class ClientOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    address: Optional[str] = None
    is_deleted: int

    class Config:
        from_attributes = True
