from fastapi import FastAPI, Request, Depends, Form, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional

from database import get_db
from models import STATUSES
import crud, schemas

app = FastAPI(
    title="IncidentDesk",
    description="Internal incident tracking system",
    version="1.0.0"
)

# Templates & static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# API ROUTES (JSON)
# =========================

@app.post("/incidents", status_code=201)
def create_incident_api(
    incident: schemas.IncidentCreate,
    conn=Depends(get_db)
):
    crud.create_incident(conn, incident)
    return {"message": "Incident logged successfully"}


@app.get("/incidents", response_model=List[schemas.IncidentOut])
def list_incidents_api(
    status: Optional[str] = Query(None),
    conn=Depends(get_db)
):
    if status and status not in STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status")

    incidents = crud.get_incidents(conn, status)
    return [dict(i) for i in incidents]


@app.get("/incidents/{incident_id}", response_model=schemas.IncidentOut)
def get_incident_api(
    incident_id: int,
    conn=Depends(get_db)
):
    incident = crud.get_incident(conn, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return dict(incident)


@app.patch("/incidents/{incident_id}")
def update_incident_api(
    incident_id: int,
    update: schemas.IncidentUpdate,
    conn=Depends(get_db)
):
    incident = crud.get_incident(conn, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    crud.update_status(conn, incident_id, update.status)
    return {"message": "Incident status updated"}

@app.get("/incidents", response_model=List[schemas.IncidentOut])
def list_incidents_api(
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    conn=Depends(get_db)
):
    incidents = crud.get_incidents(conn, status=status, severity=severity)
    return [dict(i) for i in incidents]
@app.delete("/incidents/{incident_id}", status_code=204)
def delete_incident_api(
    incident_id: int,
    conn=Depends(get_db)
):
    incident = crud.get_incident(conn, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    crud.delete_incident(conn, incident_id)

# =========================
# UI ROUTES (HTML)
# =========================
@app.get("/")
def list_incidents_ui(
    request: Request,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    conn=Depends(get_db)
):
    incidents = crud.get_incidents(conn, status=status, severity=severity)

    return templates.TemplateResponse(
        "incidents.html",
        {
            "request": request,
            "incidents": incidents,
            "current_status": status,
            "current_severity": severity,
            "statuses": ["OPEN", "IN_PROGRESS", "RESOLVED"],
            "severities": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        }
    )


@app.get("/add")
def add_incident_form(request: Request):
    return templates.TemplateResponse(
        "add_incident.html",
        {"request": request}
    )


@app.post("/add")
def add_incident_ui(
    title: str = Form(...),
    description: str = Form(...),
    severity: str = Form(...),
    conn=Depends(get_db)
):
    crud.create_incident_simple(
        conn,
        title=title,
        description=description,
        severity=severity
    )

    return RedirectResponse("/", status_code=303)
