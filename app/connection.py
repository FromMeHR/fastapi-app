from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config_db import database_url
from app.models import Base

engine = create_engine(database_url, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Base.metadata.create_all(bind=engine)
