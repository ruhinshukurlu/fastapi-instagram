from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_comment
from routers.schemas import CommentBase


router = APIRouter(
    prefix="/comment",
    tags= ['comment']
)


@router.post('/create')
def create_comment(request:CommentBase, db:Session = Depends(get_db)):
    return db_comment.create(db, request)


@router.get("/all/{post_id}")
def get_all_comments(post_id:int, db:Session = Depends(get_db)):
    return db_comment.get_all(db, post_id)
