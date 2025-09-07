from fastapi import FastAPI

from app.api.endpoints import test

app = FastAPI()

# @app.get("/")
# def read_root():
    # return {"hello": "world"}

app.include_router(test.router)