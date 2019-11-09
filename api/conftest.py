import pytest
from src.app import create_app
from src.models import db
from src.models.UserModel import UserModel

@pytest.fixture()
def test_context():
    """
    Test Configuration
    """
    app = create_app('testing')
    testing_client = app.test_client()

    with app.app_context():
        db.create_all()

        dummy_user = UserModel({
            "username": "test_user",
            "email": "test@email.com",
            "password": "test_password"
        })
        dummy_user.save()

        yield testing_client, dummy_user

        db.session.close()
        db.drop_all()
