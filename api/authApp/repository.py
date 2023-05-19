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
from api.authApp.models import User, Profile
from api.authApp.dependencies import UserFilterDependency
from fastapi_pagination.ext.sqlalchemy import paginate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db:Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user


def authenticate_user(db:Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
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
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_user(db:Session, user_obj:schemas.CreateUser, profile_id, department_id):
    hashed_password = get_password_hash(user_obj.hashed_password)
    user_obj.hashed_password = hashed_password
    user = User(**user_obj.dict(), profile_id=profile_id, department_id=department_id)
    db.add(user)
    db.commit()
    db.refresh(user)
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
