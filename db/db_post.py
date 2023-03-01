from routers.schemas import PostBase
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm.session import Session
from db.models import DbPost
from datetime import datetime

def create_post(db:Session, request: PostBase):
    new_post = DbPost(
        user_id = request.creator_id,
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        caption = request.caption,
        timestamp = datetime.now()
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all_posta(db:Session):
    return db.query(DbPost).all()


def delete(id:int, db:Session, user_id:int):
    post = db.query(DbPost).filter(DbPost.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found!")

    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only post creator can delete the post!")

    db.delete(post)
    db.commit()
    return "ok"
