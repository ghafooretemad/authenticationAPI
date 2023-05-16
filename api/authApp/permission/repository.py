from datetime import datetime, timedelta
from typing import Annotated
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .. import settings
from sqlalchemy import or_, and_
from ..models import User, Profile, Permission
from ..dependencies import PermissionFilterDependency



def create_permission(db:Session, permission_obj:schemas.Permission):
    permission = Permission(**permission_obj.dict())
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

def get_permission(filter:PermissionFilterDependency, db: Session, skip: int = 0, limit: int = settings.LIMIT):
    conditionList = list()
    if(filter.name !=''):
        conditionList.append(Permission.name.contains(filter.name))
        
    permissions = db.query(Permission).filter(and_(*tuple(conditionList))).offset(skip).limit(limit).all()
    return permissions

def get_permissionById(id:int, db: Session):
    permission = db.query(Permission).filter(Permission.id == id).first()
    return permission

def delete_permission(id:int, db: Session):
    permission = get_permissionById(id, db)
    permission.deleted = True
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission