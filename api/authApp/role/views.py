from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import CommonQueryParams, get_db
from api.authApp.dependencies import RoleFilterDependency
from sqlalchemy.orm import Session
from api.authApp.role import repository
from api.authApp.role import schemas
from api import database
from api.authApp import models
models.Base.metadata.create_all(bind=database.engine)

router = APIRouter()

@router.post("/", response_model=schemas.RoleList)
async def getRole(params: CommonQueryParams = Depends(CommonQueryParams), filter:RoleFilterDependency = Depends(RoleFilterDependency), db:Session = Depends(get_db)):
    return repository.get_role(filter, db, params.skip, params.limit)

@router.post("/role", response_model=schemas.RoleDetails)
async def createRole(role:schemas.Role, role_permissions:list[schemas.RolePermission], db:Session = Depends(get_db)):
    return repository.create_role(db, role, role_permissions)

@router.get("/role/id/{id}", response_model=schemas.RoleDetails)
async def getRoleById(id:int, db:Session = Depends(get_db)):
    role_in_db = repository.get_roleById(db, id)
    if(not role_in_db):
        raise HTTPException(status_code=404, detail="Role doesn't exist")
    return role_in_db

@router.put("/role/delete/{id}", response_model=schemas.RoleDetails)
async def deleteRole(id:int, db:Session = Depends(get_db)):
    return repository.delete_role(db, id)

@router.put("/role/update/{id}", response_model=schemas.RoleDetails)
async def updateRole(id:int, role:schemas.RoleDetails, db:Session = Depends(get_db)):
    return repository.update_role(db, id, role)