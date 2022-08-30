from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.database import Base, get_db
from server import get_application
from tests.utils.user import authentication_token
from tests.fixtures import ingredientes, opcionais, status, users, burgers


USERNAME_TESTE = 'teste'

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, Any, None]:
    """ Create a fresh database on each test case """
    Base.metadata.create_all(engine)
    _app = get_application()
    yield _app
    Base.metadata.drop_all(engine)
    import os
    os.remove("test_db.db")

@pytest.fixture(scope="session")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def header_access_token(client: TestClient, db_session: Session):
    return authentication_token(
        client=client, username=USERNAME_TESTE, db=db_session
    )





