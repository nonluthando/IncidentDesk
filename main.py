from fastapi import Request, Depends, Form
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from database import get_db

from models import STATUSES
import crud, schemas

app = FastAPI(
    title="IncidentDesk",
    description="Internal incident tracking API",
    version="1.0.0"
)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/incidents", status_code=201)
def create_incident(
    incident: schemas.IncidentCreate,
    conn=Depends(get_db)
):
    crud.create_incident(conn, incident)
    return {"message": "Incident logged successfully"}

@app.get("/incidents", response_model=List[schemas.IncidentOut])
def list_incidents(
    status: Optional[str] = Query(None),
    conn=Depends(get_db)
):
    if status and status not in STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status")

    incidents = crud.get_incidents(conn, status)
    return [dict(i) for i in incidents]

@app.get("/incidents/{incident_id}", response_model=schemas.IncidentOut)
def get_incident(incident_id: int, conn=Depends(get_db)):
    incident = crud.get_incident(conn, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return dict(incident)

@app.patch("/incidents/{incident_id}")
def update_incident(
    incident_id: int,
    update: schemas.IncidentUpdate,
    conn=Depends(get_db)
):
    incident = crud.get_incident(conn, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    crud.update_status(conn, incident_id, update.status)
    return {"message": "Incident status updated"}

@app.get("/")
def ui_list_incidents(
    request: Request,
    status: Optional[str] = None,
    conn=Depends(get_db)
):
    if status and status not in STATUSES:
        status = None  # fail safely

    incidents = crud.get_incidents(conn, status)

    return templates.TemplateResponse(
        "incidents.html",
        {
            "request": request,
            "incidents": incidents,
            "current_status": status,
            "statuses": STATUSES
        }
    )

@app.post("/add")
def ui_add_incident_post(
    title: str = Form(...),
    description: str = Form(...),
    severity: str = Form(...),
    conn=Depends(get_db)
):
    class TempIncident:
        def __init__(self, title, description, severity):
            self.title = title
            self.description = description
            self.severity = severity

    crud.create_incident(
        conn,
        TempIncident(title, description, severity)
    )

    return RedirectResponse("/", status_code=303)
