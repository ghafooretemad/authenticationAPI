from fastapi import APIRouter, Depends, HTTPException
from .. import dependencies
from sqlalchemy.orm import Session
from typing import Annotated
from . import repository, schemas
from .. import database
from . import models
models.Base.metadata.create_all(bind=database.engine)

router = APIRouter()

@router.get("/users/", tags=["users"])
async def getUsers(db:Session = Depends(dependencies.get_db), params: dependencies.CommonQueryParams = Depends(dependencies.CommonQueryParams)):
    return repository.get_users(db, params)

@router.post("/user", response_model=schemas.UserDetails)
async def createUser(user:schemas.CreateUser, profile:schemas.Profile, db:Session = Depends(dependencies.get_db)):
    user_in_db = repository.get_user_by_email(db, user.email)
    if(user_in_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    profile_in_db = repository.create_profile(db = db, profile_obj=profile)
    return repository.create_user(db = db, user_obj = user, profile_id=profile_in_db.id, department_id=None)
