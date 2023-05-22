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
async def createGroup(group:schemas.Group, group_role:list[schemas.GroupRole], db:Session = Depends(get_db)):
    return repository.create_group(db, group, group_role)

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

@router.post("/group-role/update/{id}")
async def updateGroupRole(group_id:int, group_roles:list[schemas.GroupRole], db:Session = Depends(get_db)):
    return repository.create_group_role(db, group_roles, group_id)

@router.put("/group-role/delete/{id}")
async def deleteGroupRole(id:int, db:Session = Depends(get_db)):
    return repository.delete_group_role(db, id)

@router.get("/group-role/{id}", response_model=list[schemas.GroupRoleList])
async def getGroupRoles(group_id:int, db:Session = Depends(get_db)):
    return repository.get_group_role(db, group_id=group_id)