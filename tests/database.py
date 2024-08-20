from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base
from alembic import command


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():

    # pyalchemy way
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # alembic way
    # need to make sure env variables are set up correctly
    # command.downgrade("base")
    # command.upgrade("head")
    with TestingSessionLocal() as db:
        yield db


@pytest.fixture()
def client(session):

    def override_get_db():
        with TestingSessionLocal() as db:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
