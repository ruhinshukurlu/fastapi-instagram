from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from db.database import get_db
from routers.schemas import PostDisplay, PostBase
from db import db_post


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