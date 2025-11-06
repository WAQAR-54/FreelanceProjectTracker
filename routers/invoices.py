from fastapi import APIRouter, Depends                              # ← FastAPI router & dependency system import
from sqlalchemy.orm import Session                                   # ← SQLAlchemy session type (for type hints)
from database import get_db                                          # ← DB session dependency factory (database.py se)
from models.invoice import Invoice                                   # ← Our Invoice SQLAlchemy model
from schemas.invoice import InvoiceCreate, InvoiceOut                 # ← Pydantic schemas (input + output)

router = APIRouter(prefix="/invoices", tags=["Invoices"])             # ← Is file ke saare endpoints ka URL prefix & docs grouping

def ok(message: str, data=None):                                      # ← Helper function: responses uniform banane ke liye
    return {"status": "success", "message": message, "data": data}    # ← Consistent JSON response shape

@router.post("/create")                                               # ← HTTP POST route: /invoices/create
def create_invoice(payload: InvoiceCreate,                            # ← Request body validate hoga against InvoiceCreate schema
                   db: Session = Depends(get_db)):                    # ← DB session FastAPI dependency se milti hai
    """
    Step-by-step:
    1) Client se invoice data (project_id, amount, issued_date, ...) receive karo
    2) Us data se Invoice model object banao
    3) DB me save (add + commit)
    4) DB se fresh object reload (refresh) for generated fields (like id)
    5) Pydantic v2 ke safe tarike se serialize karke JSON response bhejo
    """

    invoice = Invoice(**payload.dict())                               # ← Pydantic model se plain dict nikaal ke SQLAlchemy model banaya
    db.add(invoice)                                                   # ← New invoice ko current session me add kiya
    db.commit()                                                       # ← Transaction commit — row ab database me persist ho gayi
    db.refresh(invoice)                                               # ← Refresh — auto-generated fields (id) wapas object me aa jayengi

    out = InvoiceOut.model_validate(                                  # ← Pydantic v2: ORM object ko schema me convert karo
        invoice,                                                      # ← Source: SQLAlchemy Invoice object
        from_attributes=True                                          # ← Important: v2 me from_orm ke badlay ye flag lagta hai
    ).model_dump()                                                    # ← dict banakar response-ready structure bana do

    return ok("Invoice created successfully", out)                    # ← Uniform success response with data

@router.get("/list")                                                  # ← HTTP GET route: /invoices/list
def list_invoices(db: Session = Depends(get_db)):                     # ← DB session injection
    """
    Step-by-step:
    1) Sare non-deleted invoices load karo (is_deleted = 0)
    2) Har SQLAlchemy object ko Pydantic v2 ke through safe dict me map karo
    3) List ko ek uniform response me return karo
    """

    items = db.query(Invoice).filter(Invoice.is_deleted == 0).all()   # ← Simple SELECT * FROM invoices WHERE is_deleted = 0
    data = [                                                          # ← Python list comprehension for serialization
        InvoiceOut.model_validate(i, from_attributes=True).model_dump()  # ← v2-safe serialization per item
        for i in items                                                # ← Iterate all loaded Invoice rows
    ]

    return ok("Invoices fetched successfully", data)                   # ← Uniform success response with list payload
