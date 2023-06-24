import sys
from pathlib import Path

app_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_dir))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from db import get_session
from main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        url="sqlite://",
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
