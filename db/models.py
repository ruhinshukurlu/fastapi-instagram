from .database import Base
from sqlalchemy import Column, String, Integer


class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, index=True, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)