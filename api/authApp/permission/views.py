from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import CommonQueryParams, get_db
from api.authApp.dependencies import PermissionFilterDependency
from sqlalchemy.orm import Session
from typing import Annotated
from api.authApp.permission import repository
from api.authApp import schemas
from api import database
from api.authApp import models
models.Base.metadata.create_all(bind=database.engine)

router = APIRouter()

@router.post("/", response_model=schemas.PermissionList)
async def getPermission(params: CommonQueryParams = Depends(CommonQueryParams), filter:PermissionFilterDependency = Depends(PermissionFilterDependency), db:Session = Depends(get_db)):
    return repository.get_permission(filter, db, params.skip, params.limit)

@router.post("/permission", response_model=schemas.PermissionDetails)
async def createPermission(user:schemas.Permission, db:Session = Depends(get_db)):
    return repository.create_permission(db, user)

@router.get("/permission/id/{id}", response_model=schemas.PermissionDetails)
async def getPermissionById(id:int, db:Session = Depends(get_db)):
    permission_in_db = repository.get_permissionById(db, id)
    if(not permission_in_db):
        raise HTTPException(status_code=404, detail="Permission doesn't exist")
    return permission_in_db

@router.put("/permission/delete/{id}", response_model=schemas.PermissionDetails)
async def deletePermission(id:int, db:Session = Depends(get_db)):
    return repository.delete_permission(db, id)

@router.put("/permission/update/{id}", response_model=schemas.PermissionDetails)
async def updatePermission(id:int, permission:schemas.PermissionDetails, db:Session = Depends(get_db)):
    return repository.update_permission(db, id, permission)