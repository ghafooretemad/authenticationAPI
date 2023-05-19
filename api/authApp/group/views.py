from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import CommonQueryParams, get_db
from api.authApp.dependencies import GroupFilterDependency
from sqlalchemy.orm import Session
from api.authApp.group import repository
from api.authApp.group import schemas
from api import database
from api.authApp import models
models.Base.metadata.create_all(bind=database.engine)

router = APIRouter()

@router.post("/", response_model=schemas.GroupList)
async def getGroup(params: CommonQueryParams = Depends(CommonQueryParams), filter:GroupFilterDependency = Depends(GroupFilterDependency), db:Session = Depends(get_db)):
    return repository.get_group(filter, db, params.skip, params.limit)

@router.post("/group", response_model=schemas.GroupDetails)
async def createGroup(user:schemas.Group, db:Session = Depends(get_db)):
    return repository.create_group(db, user)

@router.get("/group/id/{id}", response_model=schemas.GroupDetails)
async def getGroupById(id:int, db:Session = Depends(get_db)):
    group_in_db = repository.get_groupById(db, id)
    if(not group_in_db):
        raise HTTPException(status_code=404, detail="Group doesn't exist")
    return group_in_db

@router.put("/group/delete/{id}", response_model=schemas.GroupDetails)
async def deleteGroup(id:int, db:Session = Depends(get_db)):
    return repository.delete_group(db, id)

@router.put("/group/update/{id}", response_model=schemas.GroupDetails)
async def updateGroup(id:int, group:schemas.GroupDetails, db:Session = Depends(get_db)):
    return repository.update_group(db, id, group)