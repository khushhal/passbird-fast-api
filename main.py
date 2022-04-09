import random
import string
from typing import List

from fastapi import FastAPI, Depends, Request, HTTPException
from pydantic.tools import lru_cache
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

import config
from app import models
from app.database import SessionLocal
from app.schemas import ApplicationPostSchema, ApplicationListSchema, ApplicationDetailSchema

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_token(req: Request):
    token = req.headers["Authorization"]
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return True


def get_application_code(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


@lru_cache()
def get_settings():
    return config.Settings()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/application/", response_model=List[ApplicationListSchema])
async def list_applications(rq: Request, db: Session = Depends(get_db), is_authorized: bool = Depends(verify_token)):
    if is_authorized:
        return db.query(models.Application).filter_by(user_id=rq.headers.get('Authorization')).all()


@app.get("/api/v1/application/{application_id}/", response_model=ApplicationDetailSchema)
async def get_application(application_id, rq: Request, db: Session = Depends(get_db),
                          is_authorized: bool = Depends(verify_token)):
    if is_authorized:
        return db.query(models.Application).filter_by(
            user_id=rq.headers.get('Authorization'), application_id=application_id
        ).one_or_none()


@app.post("/api/v1/application/", response_model=ApplicationListSchema)
async def create_application(rq: Request, application_item: ApplicationPostSchema, db: Session = Depends(get_db),
                             is_authorized: bool = Depends(verify_token)):
    if is_authorized:
        new_application = models.Application(**{
            'user_id': rq.headers.get('Authorization'),
            'application_id': get_application_code(16),
            'application_secret': get_application_code(32),
            **application_item.dict(),
        })
        db.add(new_application)
        db.commit()
        return new_application
