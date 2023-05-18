from fastapi import FastAPI, Depends
from api.authApp.views import router as authRouter
from api.authApp.permission.views import router as permissionRouter
import uvicorn

description = """
This mini app help you to do authentication, authorization and user registration . 🚀
"""
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
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
    tags= ["Users"]
    )
app.include_router(permissionRouter,
     prefix= "/permissions",
    tags= ["Permissions"]
    )


@app.get("/")
def main():
    return {"message": "Welcome to the authApp using FastAPI"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)