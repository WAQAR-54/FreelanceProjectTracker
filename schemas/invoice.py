from pydantic import BaseModel                                        # ← Pydantic BaseModel (schemas ke liye)
from typing import Optional                                           # ← Optional fields ke type hints
from datetime import date                                             # ← Date fields (issued_date, due_date) ke liye

class InvoiceCreate(BaseModel):                                       # ← Input schema: user jab invoice create karega to ye structure validate hoga
    project_id: int                                                   # ← Kis project ke liye invoice hai (required)
    amount: float                                                     # ← Amount as float for input; DB me Numeric store hoga
    issued_date: date                                                 # ← Invoice issue date (required)
    due_date: Optional[date] = None                                   # ← Due date (optional)
    paid_status: Optional[str] = "unpaid"                             # ← Optional status with default "unpaid"

    class Config:                                                     # ← Pydantic v2 config block
        from_attributes = True                                        # ← v2 replacement for orm_mode=True (ORM objects se read allowed)

class InvoiceOut(BaseModel):                                          # ← Output schema: API response me yeh shape jayega
    id: int                                                           # ← DB generated primary key
    project_id: int                                                   # ← Linked project id
    amount: float                                                     # ← Amount (as float for response convenience)
    issued_date: date                                                 # ← Issue date
    due_date: Optional[date] = None                                   # ← Optional due date
    paid_status: str                                                  # ← Current status (paid/unpaid/overdue…)
    is_deleted: int                                                   # ← Soft delete indicator (0/1)

    class Config:                                                     # ← Pydantic v2 config
        from_attributes = True                                        # ← ORM objects → schema mapping enable
