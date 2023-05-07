from fastapi import FastAPI, Depends


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

@app.get("/")
def main():
    return {"message": "Welcome to the authApp using FastAPI"}

