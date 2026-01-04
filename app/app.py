from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    

app = FastAPI(lifespan=lifespan)

text_posts = {
    1: {"title": "New Post", "content": "cool test post"},
    2: {"title": "Python Tip", "content": "Use list for cleaner loops."}
    }

@app.get("/posts") ## This fetches all the posts
def get_all_posts():
    return text_posts

@app.get("/posts/{id}") ## This fetches only particular id posts
def get_post(id: int) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="POST not found")
    return text_posts.get(id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post

## PostResponse - It creates a validation that only that type of data is allowed