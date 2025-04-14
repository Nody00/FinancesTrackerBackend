import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
import pytest

client = TestClient(app)

DATABASE_URL = "sqlite://"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db


def setup() -> None:
    Base.metadata.create_all(bind=engine)


def teardown() -> None:
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)  # Use pytest fixture
def setup_test_database():
    """Sets up and tears down the database for testing."""
    setup()  # Create tables
    yield  # Run the tests
    teardown()  # Drop tables
