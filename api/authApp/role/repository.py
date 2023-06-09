from datetime import datetime
from api.authApp.role import schemas
from sqlalchemy.orm import Session
from api import settings
from sqlalchemy import or_, and_
from api.authApp.models import Role, RolePermission, Permission
from api.authApp.dependencies import RoleFilterDependency



def create_role(db:Session, role_obj:schemas.Role, role_permissions:list[schemas.RolePermission]):
    role = Role(**role_obj.dict())
    db.add(role)
    db.commit()
    db.refresh(role)
    role_permissions_in_db = create_role_permission(db, role_permissions, role.id)
    role.role_permissions = role_permissions_in_db
    return role

def get_role(filter:RoleFilterDependency, db: Session, skip: int = 0, limit: int = settings.LIMIT):
    roles = db.query(Role).filter(and_(*tuple(filter.prepareFilter())) if filter.prepareFilter() else True)
    total = roles.count()
    filterd_roles = roles.offset(skip).limit(limit).all()
    return {"total_records":total, "data":filterd_roles}

def get_roleById(db: Session, id:int):
    role = db.query(Role).filter(Role.id == id).first()
    return role

def delete_role(db: Session, id:int):
    role = get_roleById(db, id)
    role.deleted = True
    role.deleted_by = None
    role.deleted_at = datetime.utcnow()
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, id:int, role:schemas.RoleDetails):
    role_in_db = get_roleById(db, id)
    role_in_db.title = role.title
    role_in_db.description = role.description
    role_in_db.updated_by = None
    role_in_db.updated_at = datetime.utcnow()
    db.add(role_in_db)
    db.commit()
    db.refresh(role_in_db)
    return role_in_db

def create_role_permission(db:Session, role_permissions:list[schemas.RolePermission], role:int):
    role_permission_in_db:schemas.RolePermissionDetails = list()
    for i in role_permissions:
        role_permission = RolePermission(permission_id = i.permission_id, role_id = role)
        db.add(role_permission)
        db.commit()
        db.refresh(role_permission)
        role_permission_in_db.append(role_permission)
    return role_permission_in_db

def delete_role_permission(db:Session, id:int):
    role_permission = db.query(RolePermission).filter(RolePermission.id ==id).first()
    db.delete(role_permission)
    db.commit()
    return role_permission
    
def get_role_permission(db:Session, role_id:int):
    role_permission = db.query(Permission).join(RolePermission).filter(RolePermission.role_id ==role_id).all()
    return role_permission