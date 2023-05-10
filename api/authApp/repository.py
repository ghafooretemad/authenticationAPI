from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .. import settings



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db:Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
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


def create_user(db:Session, user_obj:schemas.createUser):
    hashed_password = get_password_hash(user_obj.password)
    user_obj.hashed_password = hashed_password
    user = models.User(**user_obj)
    db.add(user)
    db.commit()
    db.refresh(user)
    return db.user

def get_users(db: Session, skip: int = 0, limit: int = settings.LIMIT):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

def get_user_by_email(db:Session, email:str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

def get_user_by_name(db:Session, name:str):
    users = db.query(models.User).filter(models.User.name == name)
    return users
