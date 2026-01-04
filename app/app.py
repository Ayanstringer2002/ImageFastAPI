from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate

app = FastAPI()

text_posts = {
    1: {"title": "New Post", "content": "cool test post"},
    2: {"title": "Python Tip", "content": "Use list for cleaner loops."}
    }

@app.get("/posts") ## This fetches all the posts
def get_all_posts():
    return text_posts

@app.get("/posts/{id}") ## This fetches only particular id posts
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="POST not found")
    return text_posts.get(id)

@app.post("/posts")
def create_post(post: PostCreate):
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post