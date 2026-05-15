import pytest
from app import create_app
from core.db.sync_db import SyncDB
from core.db.base import Base
from core import config


@pytest.fixture(scope='session')
def app():
    """Creates a test Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture(scope='function')
def client(app):
    """A test HTTP client."""
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='function')
def db_session():
    """Creates a clean synchronous session for tests."""
    db = SyncDB(config.db_config)
    db.connect()

    Base.metadata.create_all(db._engine)

    session = db.get_session()
    yield session

    session.rollback()
    session.close()

    Base.metadata.drop_all(db._engine)
    db.close()


@pytest.fixture(scope='function')
def notification_data():
    """Example of notification data."""
    return {
        "type": "email",
        "recipient": "user@example.com",
        "message": "Test notification message",
        "subject": {"title": "Hello"}
    }