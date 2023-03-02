from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from db.database import get_db
from routers.schemas import PostDisplay, PostBase
from db import db_post
from typing import List
import random
import string
import shutil
from routers.schemas import UserAuth
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix="/post",
    tags = ['post']
)

image_url_types = ['absolute', 'relative']

@router.post('/', response_model=PostDisplay)
def create_post(request:PostBase, db: Session = Depends(get_db)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="image_url_type can only get 'absolute' or 'relative' values ")
    return db_post.create_post(db, request)


@router.get('/all', response_model=List[PostDisplay])
def get_all_posts(db:Session = Depends(get_db)):
    return db_post.get_all_posta(db)


@router.post("/image")
def upload_image(image: UploadFile = File(...), current_user:UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    random_str = ''.join(random.choice(letters) for i in range(6))
    new = f"_{random_str}."
    filename = new.join(image.filename.rsplit('.',1))
    path = f"images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {
        "filename":path
    }


@router.get('/delete/{id}')
def delete_post(id:int, db:Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    db_post.delete(id, db, current_user.id)