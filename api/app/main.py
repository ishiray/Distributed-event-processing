from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from tenacity import retry, stop_after_attempt, wait_fixed

from .database import Base, engine
from .routes import incidents

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(2)
)
def init_db():
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        print("Database connected successfully")
    except OperationalError as e:
        print("Database not ready yet...")
        raise e


init_db()

app = FastAPI(title="IncidentFlow")

app.include_router(incidents.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}