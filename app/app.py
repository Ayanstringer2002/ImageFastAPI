from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse, UserRead, UserCreate, userupdate
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
import shutil
import os
import uuid
import tempfile
from app.users import auth_backend, current_active_user, fastapi_users

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])


## Creating a POST Request
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    
    
    session: AsyncSession = Depends(get_async_session)
    
):
    post = Post(
        caption=caption,
        url="dummy url",
        file_type="photo",
        file_name="dummy name"
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post



 ## Retrieving Data
@app.get("/feed")
async def get_feed(
    ## This is dependency injection
    session:AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
    return {"posts": posts_data}

## Delete the post
@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        await session.delete(post)
        await session.commit()
        return {"success": True, "message": "Post deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
        
        


