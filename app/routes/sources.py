from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/sources", tags=["Job Sources"])


@router.get("/", response_model=List[schemas.JobSourceResponse])
def get_job_sources(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.JobSource).offset(skip).limit(limit).all()


@router.get("/active", response_model=List[schemas.JobSourceResponse])
def get_active_job_sources(db: Session = Depends(get_db)):
    return db.query(models.JobSource).filter(
        models.JobSource.is_active == True,
        models.JobSource.is_freelance == False
    ).all()