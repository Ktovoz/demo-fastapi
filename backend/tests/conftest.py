import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.database import Base
from app.core.config import settings

# Create an in-memory SQLite database for testing
@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create a test database session"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()