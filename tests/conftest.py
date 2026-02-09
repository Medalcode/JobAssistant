
import os
import tempfile
import pytest
from app import app
from models import db

@pytest.fixture
def client():
    # Create a temporary file to use as a database
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)
