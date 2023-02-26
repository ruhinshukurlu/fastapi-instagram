from fastapi import FastAPI
from db.database import engine
from db import models


app = FastAPI()


@app.get("/")
def hello():
    return "Hello world"


models.Base.metadata.create_all(engine)