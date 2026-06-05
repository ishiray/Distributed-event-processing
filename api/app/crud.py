from sqlalchemy.orm import Session
from . import models, schemas
from .kafka.producer import publish_incident_created


def create_incident(db: Session, incident: schemas.IncidentCreate):
    db_incident = models.Incident(**incident.model_dump())

    db.add(db_incident)
    db.commit()
    publish_incident_created({
        "incident_id": db_incident.id,
        "service_name": db_incident.service_name,
        "severity": db_incident.severity
    })
    db.refresh(db_incident)

    return db_incident


def get_incidents(db: Session):
    return db.query(models.Incident).all()


def get_incident(db: Session, incident_id: int):
    return (
        db.query(models.Incident)
        .filter(models.Incident.id == incident_id)
        .first()
    )