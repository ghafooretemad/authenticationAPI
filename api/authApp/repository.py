from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from api.authApp import schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from api import settings
from sqlalchemy import or_, and_
from api.authApp.models import User, Profile, UserGroup, Permission, UserGroup, GroupRole, RolePermission, Role, Group
from api.authApp.dependencies import UserFilterDependency
from fastapi_pagination.ext.sqlalchemy import paginate
from api.settings import ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db:Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    return user


def authenticate_user(db:Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if current_user.is_active == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_user(db:Session, user_obj:schemas.UserCreate, profile_id, user_group:list[schemas.UserGroup]):
    hashed_password = get_password_hash(user_obj.hashed_password)
    user_obj.hashed_password = hashed_password
    user = User(**user_obj.dict(), profile_id=profile_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    create_user_Group(db, user_group, user.id)
    return user

def create_profile(db:Session, profile_obj:schemas.Profile):
    profile = Profile(**profile_obj.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def get_users(userFilter:UserFilterDependency, db: Session, skip: int = 0, limit: int = settings.LIMIT):        
    users = db.query(User).join(Profile).filter(and_(*tuple(userFilter.prepareFilter())))
    total = users.count()
    filterd_users = users.offset(skip).limit(limit).all()
    return {"total_records":total, "data":filterd_users}

def get_user_by_email(db:Session, email:str):
    user = db.query(User).filter(User.email == email).first()
    return user

def get_user_by_name(db:Session, name:str):
    users = db.query(User).join(Profile).filter(or_(Profile.first_name.contains(name), Profile.last_name.contains(name))).all()
    return users

def get_user_by_id(db:Session, id:int):
    user = db.query(User).filter(User.id == id).first()
    return user

def update_user(db: Session, id:int, user:schemas.UserCreate):
    user_in_db = get_user_by_id(db, id)
    user_in_db.email = user.email
    user_in_db.department_id = user.department_id
    user_in_db.preference = user.preference
    user_in_db.is_active = user.is_active
    user_in_db.updated_by = None
    user_in_db.updated_at = datetime.utcnow()
    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)
    return user_in_db

def create_user_Group(db:Session, user_groups:list[schemas.UserGroup], user_id:int):
    for i in user_groups:
        user_group = UserGroup(group_id = i.group_id, user_id = user_id)
        user_group.created_at = datetime.utcnow()
        db.add(user_group)
        db.commit()
    return True

def delete_user_group(db:Session, id:int):
    user_group = db.query(UserGroup).filter(UserGroup.id ==id).first()
    db.delete(user_group)
    db.commit()
    return True

def get_user_permission(db:Session, user_id:int):
    permissions = db.query(Permission).join(RolePermission).join(Role).join(GroupRole).join(Group).join(UserGroup).filter(UserGroup.user_id == user_id).all()
    return permissions

def get_user_groups(db:Session, user_id:int):
    user_groups = db.query(Group).join(UserGroup).filter(UserGroup.user_id == user_id).all()
    return user_groups