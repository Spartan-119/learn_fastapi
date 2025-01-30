from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title": "some title lol", "content": "some content", "id": 1},
    {"title": "second title lol", "content": "second content lol", "id": 2}
]

@app.get("/")
def root():
    return {"message": "hello world"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/createposts")
def create_posts(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}