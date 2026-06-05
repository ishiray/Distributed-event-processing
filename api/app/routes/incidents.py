from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..redis_client import redis_client

from ..database import SessionLocal
from .. import crud, schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/incidents", response_model=schemas.IncidentResponse)
def create_incident(
    incident: schemas.IncidentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_incident(db, incident)


@router.get("/incidents")
def list_incidents(db: Session = Depends(get_db)):
    return crud.get_incidents(db)


@router.get("/incidents/{incident_id}")
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = crud.get_incident(db, incident_id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident

@router.get("/incidents/{incident_id}/status")
def get_incident_status(incident_id: int):
    status = redis_client.get(f"incident:{incident_id}")

    if not status:
        return {
            "incident_id": incident_id,
            "status": "not_processed"
        }

    return {
        "incident_id": incident_id,
        "status": status
    }