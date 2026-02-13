from fastapi import FastAPI, Body, status, HTTPException, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db

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


class Post(BaseModel):
    title: str
    content: str
    published: bool

class PostUpdate(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "fast api is running"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)) :
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(post.model_dump())
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "data": new_post,
        "message": "Post created successfully",
    }


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"The post with the id:{id} was not found"
            )
    return {
            "message" : "Post retrieved successfully",
            "data": post
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)) -> Response:
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"The post with the id:{id} was not found"
            )

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post: PostUpdate) -> Dict[str, Any]:
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING *",
        (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()
    
    print(updated_post)
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"The post with the id:{id} was not found"
            )
    return {
            "message" : "Post updated successfully",
            "data": updated_post
    }
