from sqlalchemy import create_engine
from app.config_db import database_url
from app.models import Base
from app.connection import session

def main():
    engine = create_engine(database_url)
    sess = session
    Base.metadata.create_all(bind=engine)
    sess.close()

if __name__ == '__main__':
    main()