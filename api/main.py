from fastapi import FastAPI, Depends, status, HTTPException
from api.authApp.views import router as authRouter
from api.authApp.permission.views import router as permissionRouter
from api.authApp.group.views import router as groupRouter
from api.authApp.role.views import router as RoleRouter
from api.authApp.repository import oauth2_scheme, authenticate_user,create_access_token
from api.authApp.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from api.dependencies import get_db
from sqlalchemy.orm import Session

import uvicorn

description = """
This mini app help you to do authentication, authorization and user registration . 🚀
"""
tags_metadata = [
    {
        "name": "Authentication & Authorization  APP",
        "description": "Operations with users, permissions, roles, groups and Auth. The **login** logic is also here.",
    },
]

app = FastAPI(
              title="authApp",
              description=description,
              version="0.0.1",
              contact={"name": "Ghafoor Etemad",
                       "email": "ghafooretemad3@gmail.com",
                       },
              openapi_tags=tags_metadata,
              )

app.include_router(authRouter,
     prefix= "/users",
    tags= ["User Operations"],
    dependencies=[Depends(oauth2_scheme)]
    )
app.include_router(permissionRouter,
     prefix= "/permissions",
    tags= ["Permission Operations"],
    dependencies=[Depends(oauth2_scheme)],
    )

app.include_router(groupRouter,
                   prefix="/groups",
                   tags=["Group Operations"],
                   dependencies=[Depends(oauth2_scheme)]
                                 )

app.include_router(RoleRouter,
                   prefix="/roles",
                   tags=["Role Operations"],
                   dependencies=[Depends(oauth2_scheme)])

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],  db: Session = Depends(get_db)
):
    user = authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100, reload=True)