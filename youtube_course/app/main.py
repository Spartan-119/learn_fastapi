from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor

import os
import dotenv

import time

dotenv.load_dotenv()

POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRESQL_DATABASE = os.getenv("POSTGRESQL_DATABASE")
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try: 
        conn = psycopg2.connect(host = POSTGRESQL_HOST, database = POSTGRESQL_DATABASE, user = POSTGRESQL_USER, password = POSTGRESQL_PASSWORD, cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successful!!!")
        break

    except Exception as error:
        print(f"Connecting to database failed: \n{error}")
        time.sleep(2)

my_posts = [
    {"title": "some title lol", "content": "some content", "id": 1},
    {"title": "second title lol", "content": "second content lol", "id": 2}
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "hello world"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/createposts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit() # be sure to add this to actually make changes to the database

    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    # post = find_post(id)
    # doing a quick check
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} not found"}
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} not found."
            )
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # logic to delete the post
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} does not exist")
   
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} does not exist")
    
    return {"data": updated_post}