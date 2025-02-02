from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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
    return {"data": my_posts}

@app.post("/createposts", status_code = status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
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
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} does not exist")
    my_posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} does not exist")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}