# routers/client.py (or routers/clients.py)
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models.client import Client

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/view/{client_id}")
def view_client_page(client_id: int, request: Request, db: Session = Depends(get_db)):
    """
    HTML page: show a single client's full details.
    URL: /clients/view/<id>
    """
    obj = db.query(Client).filter(Client.id == client_id, Client.is_deleted == 0).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")

    # Render the new template
    return request.app.state.templates.TemplateResponse(
        "client_detail.html",
        {
            "request": request,
            "client": {
                "id": obj.id,
                "name": obj.name,
                "email": obj.email,
                "phone": obj.phone,
                "company_name": obj.company_name,
                "address": obj.address,
            },
        }
    )
