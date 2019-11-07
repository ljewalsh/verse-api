import pytest
from src.app import create_app
from src.models import db

@pytest.fixture()
def test_client():
    app = create_app('testing')
    testing_client = app.test_client()

    with app.app_context():
        yield testing_client
        db.drop_all()
