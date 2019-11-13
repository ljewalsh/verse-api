import pytest
from src.app import create_app
from src.models import db
from src.models.UserModel import UserModel
from src.shared.Authentication import Auth

@pytest.fixture()
def test_context():
    '''
    Test Configuration
    '''
    app = create_app('testing')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://verse_developer:iamaversedeveloper@localhost:5432/verse_testing'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()

    test_client = app.test_client()

    with app.app_context():
        db.create_all()

        dummy_user = UserModel({
            'username': 'test_user',
            'email': 'test@email.com',
            'password': 'test_password'
        })
        dummy_user.save()

        token = Auth.generate_token(dummy_user.id)
        yield test_client, dummy_user, token

        db.session.close()
        db.drop_all()
