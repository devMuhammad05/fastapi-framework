from fastapi import FastAPI, status, HTTPException, Response, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from datetime import datetime
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastDB",
            user="muhammad",
            password="1234"
        )

        cursor = conn.cursor(cursor_factory=RealDictCursor)

        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)


@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "fast api is running"}


app.include_router(post.router)
app.include_router(user.router)



