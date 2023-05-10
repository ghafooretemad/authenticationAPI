from fastapi import APIRouter, Depends
from .. import dependencies
from sqlalchemy.orm import Session
from typing import Annotated
from . import repository
from .. import database
from . import models
models.Base.metadata.create_all(bind=database.engine)

router = APIRouter()

@router.get("/users/", tags=["users"], response_model = None)
async def getUsers(db:Session = Depends(dependencies.get_db), params: dependencies.CommonQueryParams = Depends(dependencies.CommonQueryParams)):
    return repository.get_users(db, params)
