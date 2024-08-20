from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from time import sleep
import psycopg
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# SqlAlchemy dependency
def get_db():
    with SessionLocal() as db:
        yield db

## improve this by creating separate connection module
# use this when not using sqlalchemy

#while True:
#
#    try:
#        conn = psycopg.connect(host='127.0.0.1', dbname='fastapi', user='testuser', password='passw0rd', row_factory=psycopg.rows.dict_row)
#        cursor = conn.cursor()
#        print("Database connection was succesfull!")
#        break
#    except psycopg.Error as e:
#        print("Connecting to database fails: ", e)
#        sleep(5)
