# routers/frontend.py
# ─────────────────────────────────────────────────────────────────────────────
# PURPOSE:
#   Ye router HTML page render karta hai (Jinja2 template) jo projects ki list
#   dikhata hai sath me client ka naam, status steps, dates, budget, etc.
#
# HIGH-LEVEL FLOW:
#   1) Database se Project + Client ko ek hi query me JOIN karke fetch karte hain
#   2) Raw DB rows ko simple Python dicts me map karte hain (template-friendly)
#   3) Jinja template 'projects_list.html' ko data ke sath render kar dete hain
#
# REQUIREMENTS:
#   - main.py me Jinja2Templates configured ho aur app.state.templates set ho
#   - templates/ folder me 'projects_list.html' file maujood ho
#   - models/ me Project & Client models defined hon (is_deleted, status etc.)
#   - database.py me get_db (Session dependency) defined ho
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, Request   # APIRouter: routes group karne ke liye
                                                  # Depends: DB session inject karne ke liye
                                                  # Request: template render ke liye required

from sqlalchemy.orm import Session                # SQLAlchemy Session type (type hints + clarity)
from database import get_db                       # get_db: per-request DB session provide karta hai
from models.project import Project                # ORM model: projects table
from models.client import Client                  # ORM model: clients table
from sqlalchemy import select, join               # select: Pythonic SELECT; join: SQL JOIN build karne ke liye

# Router instance:
#  - prefix="/ui" ka matlab: is file ke sare endpoints /ui se start honge
#  - tags=["Frontend"] sirf Swagger docs me grouping/labeling ke liye
router = APIRouter(prefix="/ui", tags=["Frontend"])


@router.get("/projects")
def projects_page(
    request: Request,               # Jinja templates ko FastAPI me render karne ke liye 'request' pass karna zaroori hota hai
    db: Session = Depends(get_db),  # DB session auto-injected; with/close handling automatically hota hai dependency se
):
    """
    Endpoint: GET /ui/projects

    Step-by-step summary (quick):
      1) Project + Client ko explicit JOIN ke zariye ek hi query me load karna
      2) Result rows ko clean dicts me map karna (None handling, status normalize)
      3) TemplateResponse se 'projects_list.html' render karna (data pass karke)

    Kyun JOIN?
      - Taa-ke N+1 (lazy loading) issue na aaye aur single query me dono tables se data mil jaye
      - Performance aur clarity dono improve hoti hai
    """

    # ─────────────────────────────────────────────────────────────────────────
    # 1) Explicit JOIN: Project ⟶ Client
    #    SQL equivalent: FROM projects JOIN clients ON clients.id = projects.client_id
    #    Note: Filter soft-deleted rows later .where(...) me handle ho raha.
    # ─────────────────────────────────────────────────────────────────────────
    j = join(Project, Client, Client.id == Project.client_id)

    # SELECT list me wahi columns pick karo jo page par chahiye:
    #  - Project ke basic fields (id, title, description, start/end/status/budget, client_id)
    #  - Client ka name as "client_name" label (template me readable key name)
    rows = db.execute(
        select(
            Project.id,
            Project.title,
            Project.description,
            Project.client_id,
            Project.start_date,
            Project.end_date,
            Project.status,
            Project.budget,
            Client.name.label("client_name"),
        )
        .select_from(j)                                    # FROM projects JOIN clients ...
        .where(Project.is_deleted == 0,                    # sirf active projects
               Client.is_deleted == 0)                     # sirf active clients
        .order_by(Project.id.desc())                       # latest projects pehle
    ).all()                                                # query execute + tamam rows lao

    # ─────────────────────────────────────────────────────────────────────────
    # 2) Rows ko template-friendly dicts me map karo
    #    Why dicts? Jinja me dictionaries aur lists handle karna straight-forward hota hai
    #    Normalize:
    #      - description None ho to "", taa-ke template me "None" print na ho
    #      - status lower-case me aur default "planned" rakho agar NULL ho
    # ─────────────────────────────────────────────────────────────────────────
    projects = []  # final list jo template ko jayegi
    for r in rows:
        projects.append({
            "id": r.id,                                            # project primary key
            "title": r.title,                                      # project title
            "description": r.description or "",                    # None ko empty string
            "client_id": r.client_id,                              # foreign key to client
            "client_name": r.client_name,                          # joined client ka naam (label ki wajah se)
            "start_date": r.start_date,                            # project start date (ya None)
            "end_date": r.end_date,                                # project end date (ya None)
            "status": (r.status or "planned").lower(),             # normalize to lower; None -> "planned"
            "budget": r.budget,                                    # numeric amount (ya None)
        })

    # ─────────────────────────────────────────────────────────────────────────
    # 3) Template render karna:
    #    - "projects_list.html" templates/ folder me hona chahiye
    #    - "request" key Jinja2Templates ke liye mandatory hai
    #    - projects list pass karein
    #    - status_steps list pass karein (UI me teen dots/steps show karne ke liye)
    # ─────────────────────────────────────────────────────────────────────────
    return request.app.state.templates.TemplateResponse(
        "projects_list.html",            # Jinja template filename
        {
            "request": request,          # required by Jinja2 in FastAPI
            "projects": projects,        # table/list ke liye main data
            # Legend / UI ke liye status steps order (template me helpful)
            "status_steps": ["ongoing", "on_hold", "completed"],
        }
    )

# ─────────────────────────────────────────────────────────────────────────────
# NOTES:
#  - Agar aapko serial number chahiye (1,2,3...) to template me Jinja ka loop.index use kar sakte hain.
#  - Client name ko hyperlink bana ke modal/drawer me client detail dikhani ho:
#       * Frontend JS me fetch('/clients/get/{client_id}') call karein
#       * routers/clients.py me ek GET detail endpoint hona chahiye jo JSON return kare
#  - Pagination/Search chahiye ho to is router ka advanced version bana ke query params handle karein
#    (e.g., q=, status=, page=, size=) — ya ek nayi router file (e.g., /dashboard) me implement karein.
# ─────────────────────────────────────────────────────────────────────────────
