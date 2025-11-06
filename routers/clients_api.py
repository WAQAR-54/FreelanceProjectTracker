from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.client import Client
from schemas.client import ClientCreate, ClientOut

# Yeh route group hai jisme sab clients ke related APIs hongi
router = APIRouter(prefix="/clients", tags=["Clients"])

# ✅ Common function: har response same format me bhejna
def make_response(message, data=None):
    return {
        "status": "success",
        "message": message,
        "data": data
    }


# 🟢 ROUTE 1: Create (naya client add karna)
@router.post("/create")
def create_client(request: ClientCreate, db: Session = Depends(get_db)):
    """
    Step by step:
    1. User se new client ka data aayega (name, email, phone etc.)
    2. Us data se ek naya Client object banayenge
    3. Database me save karenge
    4. Return karenge success message aur saved client ka data
    """

    # 1️⃣ User ke input se ek client object bana lo
    new_client = Client(**request.dict())

    # 2️⃣ Database me add karo
    db.add(new_client)
    db.commit()

    # 3️⃣ Refresh karo taake latest id waghera mil jaye
    db.refresh(new_client)

    # 4️⃣ Return karo success message aur client ka data
    return make_response(
        "New client created successfully!",
        ClientOut.from_orm(new_client).dict()
    )


# 🔵 ROUTE 2: List (sab clients dikhana)
@router.get("/list")
def list_clients(db: Session = Depends(get_db)):
    """
    Step by step:
    1. Database se sab clients laao jinka 'is_deleted = 0' hai
    2. Unko readable format (dict) me convert karo
    3. Return karo ek success message aur list of clients
    """

    # 1️⃣ Database se clients lo (jo delete nahi hue)
    clients = db.query(Client).filter(Client.is_deleted == 0).all()

    # 2️⃣ Har client ko schema (ClientOut) ke through dict me badlo
    client_list = [ClientOut.from_orm(c).dict() for c in clients]

    # 3️⃣ Return response
    return make_response(
        "All active clients fetched successfully!",
        client_list
    )
