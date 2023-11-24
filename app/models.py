from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String(120), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    auth_key = Column(String(50))
    created_at = Column(String, default=datetime.utcnow())

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(50))
    topic = Column(String(50))
    status = Column(Boolean, default=False)
    created_at = Column(String, default=datetime.utcnow())



