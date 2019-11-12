import json
from src.models import db
from src.models.UserModel import UserModel
from tests.shared_methods import make_post_request, make_get_request

def test_create_user(test_context):
    test_client, dummy_user, token = test_context
    new_user = {
            'email': 'create_user@email.com',
            'username': 'test_create_user',
            'password': 'test_password'
            }

    res = make_post_request('/api/v1/users/', test_client, new_user, token)

    created_user = UserModel.get_user_by_email('create_user@email.com')

    assert created_user is not None
    assert res.status_code == 201

def test_get_user_success(test_context):
    test_client, dummy_user, token = test_context

    path = '/api/v1/users/' + str(dummy_user.id)
    res = make_get_request(path, test_client, token)
    res_json = res.get_json()

    assert res.status_code == 200
    assert res_json['id'] == dummy_user.id
    assert res_json['email'] == dummy_user.email
    assert res_json['username'] == dummy_user.username
    assert res_json['password'] == dummy_user.password

def test_get_user_failure(test_context):
    test_client, dummy_user, token = test_context

    path = '/api/v1/users/1000'
    res = make_get_request(path, test_client, token)
    res_json = res.get_json()

    assert res.status_code == 404
    assert res.get_json() == { 'error': 'User with id 1000 does not exist' }
