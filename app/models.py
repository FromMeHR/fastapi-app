from sqlalchemy import create_engine, Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from app.config_db import database_url
# from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

def connect_db():
    engine = create_engine(database_url, connect_args={'check_same_thread': False})
    session = Session(bind=engine.connect())
    return session

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String(120), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    created_at = Column(String, default=datetime.utcnow())

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(50))
    topic = Column(String(50))
    status = Column(Boolean, default=False)
    created_at = Column(String, default=datetime.utcnow())

class AuthToken(Base):
    __tablename__ = "auth_token"

    id = Column(Integer, primary_key=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(String, default=datetime.utcnow())



