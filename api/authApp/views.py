from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import CommonQueryParams, get_db
from api.authApp.dependencies import UserFilterDependency
from sqlalchemy.orm import Session
from typing import Annotated
from api.authApp import repository, schemas
from api import database
from api.authApp import models

models.Base.metadata.create_all(bind=database.engine)

router = APIRouter()

@router.get("/users/", response_model=list[schemas.UserDetails])
async def getUsers(params: CommonQueryParams = Depends(CommonQueryParams), filter:UserFilterDependency = Depends(UserFilterDependency), db:Session = Depends(get_db)):
    return repository.get_users(filter, db, params.skip, params.limit)

@router.post("/user", response_model=schemas.UserDetails)
async def createUser(user:schemas.CreateUser, profile:schemas.Profile, db:Session = Depends(get_db)):
    user_in_db = repository.get_user_by_email(db, user.email)
    if(user_in_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    profile_in_db = repository.create_profile(db = db, profile_obj=profile)
    return repository.create_user(db = db, user_obj = user, profile_id=profile_in_db.id, department_id=None)

@router.get("/user/userid/{userid}", response_model=schemas.UserDetails)
async def getUserByUserId(userid:int, db:Session = Depends(get_db)):
    user_in_db = repository.get_user_by_id(db, userid)
    if(not user_in_db):
        raise HTTPException(status_code=404, detail="User doesn't exist")
    return user_in_db

@router.get("/user/name/{name}", response_model=schemas.UserDetails)
async def getUserByName(name:str, db:Session = Depends(get_db)):
    users_in_db = repository.get_user_by_name(db, name)
    if(not users_in_db):
        raise HTTPException(status_code=404, detail="User doesn't exist")
    return users_in_db
