from sqlalchemy import create_engine
from app.config_db import database_url
from app.models import Base, connect_db

def main():
    engine = create_engine(database_url)
    session = connect_db()
    Base.metadata.create_all(bind=engine)
    session.close()

if __name__ == '__main__':
    main()