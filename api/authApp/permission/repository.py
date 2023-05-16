from datetime import datetime
from api.authApp import schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from api import settings
from sqlalchemy import or_, and_
from api.authApp.models import Permission
from api.authApp.dependencies import PermissionFilterDependency



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

def get_permissionById(db: Session, id:int):
    permission = db.query(Permission).filter(Permission.id == id).first()
    return permission

def delete_permission(db: Session, id:int):
    permission = get_permissionById(db, id)
    permission.deleted = True
    permission.deleted_by = None
    permission.deleted_at = datetime.utcnow()
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


def update_permission(db: Session, id:int, permission:schemas.PermissionDetails):
    permission_in_db = get_permissionById(db, id)
    permission_in_db.title = permission.title
    permission_in_db.description = permission.description
    permission_in_db.updated_by = None
    permission_in_db.updated_at = datetime.utcnow()
    db.add(permission_in_db)
    db.commit()
    db.refresh(permission_in_db)
    return permission_in_db