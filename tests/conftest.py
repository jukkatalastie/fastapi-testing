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
from app.oauth2 import create_access_token
from app import models
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

@pytest.fixture
def test_user(client):
    user_data = {"email": "testiuser1@testi.com", "password": "testipassu"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "testiuser123@testi.com", "password": "testipassu"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
        "title": "1st title",
        "content": "1st content",
        "owner_id": test_user['id']
        },
        {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
        },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
        },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
        },
    ]

    posts = [ models.Post(**post) for post in posts_data ]

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
