from datetime import datetime
from api.authApp.group import schemas
from sqlalchemy.orm import Session
from api import settings
from sqlalchemy import or_, and_
from api.authApp.models import Group, GroupRole
from api.authApp.dependencies import GroupFilterDependency



def create_group(db:Session, group_obj:schemas.Group, group_roles:schemas.GroupRole):
    group = Group(**group_obj.dict())
    db.add(group)
    db.commit()
    db.refresh(group)
    group_role_in_db = create_group_role(db, group_roles, group.id)
    group.group_roles = group_role_in_db
    
    return group

def get_group(filter:GroupFilterDependency, db: Session, skip: int = 0, limit: int = settings.LIMIT):
    groups = db.query(Group).filter(and_(*tuple(filter.prepareFilter())))
    total = groups.count()
    filterd_groups = groups.offset(skip).limit(limit).all()
    return {"total_records":total, "data":filterd_groups}

def get_groupById(db: Session, id:int):
    group = db.query(Group).filter(Group.id == id).first()
    return group

def delete_group(db: Session, id:int):
    group = get_groupById(db, id)
    group.deleted = True
    group.deleted_by = None
    group.deleted_at = datetime.utcnow()
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def update_group(db: Session, id:int, group:schemas.GroupDetails):
    group_in_db = get_groupById(db, id)
    group_in_db.title = group.title
    group_in_db.description = group.description
    group_in_db.updated_by = None
    group_in_db.updated_at = datetime.utcnow()
    db.add(group_in_db)
    db.commit()
    db.refresh(group_in_db)
    return group_in_db

def create_group_role(db:Session, group_roles:schemas.GroupRole, group:int):
    group_role_in_db:schemas.GroupRoleDetails = list()
    for i in group_roles:
        group_role = GroupRole(role_id = i.role_id, group_id = group)
        db.add(group_role)
        db.commit()
        db.refresh(group_role)
        group_role_in_db.append(group_role)
    return group_role_in_db