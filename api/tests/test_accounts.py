import json
from src.models import db
from src.models.AccountModel import AccountModel

def test_create_account_success(test_context):
    test_client, dummy_user = test_context

    new_account = {
            "user_id": dummy_user.id,
            "balance": 5,
            "account_number": "test_create_account_success"
            }

    res = test_client.post('/api/v1/accounts/', data=json.dumps(new_account), content_type='application/json')

    created_account = AccountModel.query.filter(AccountModel.account_number == "test_account_number")

    assert created_account is not None
    assert res.status_code == 201

def test_create_account_failure(test_context):
    test_client, dummy_user = test_context

    account_details = {
            "user_id": dummy_user.id,
            "balance": 5,
            "account_number": "test_create_account_failure"
            }

    account = AccountModel(account_details)
    account.save()

    res = test_client.post('/api/v1/accounts/', data=json.dumps(account_details), content_type='application/json')

    assert res.status_code == 403
    assert res.get_json() == { "error": "Account with account_number {} already exist for user_id {}, please supply another account number".format(account.account_number, str(dummy_user.id)) }

def test_get_account_success(test_context):
    test_client, dummy_user = test_context

    account = AccountModel({
            "user_id": dummy_user.id,
            "balance": 0,
            "account_number": "another_test_account_number"
    })

    account.save()

    route = '/api/v1/accounts/' + str(account.id)
    res = test_client.get(route)
    res_json = res.get_json()

    assert res.status_code == 200
    assert res_json['id'] == account.id
    assert res_json['user_id'] == account.user_id
    assert res_json['balance'] == account.balance
    assert res_json['account_number'] == account.account_number

def test_get_account_failure(test_context):
    test_client, dummy_user = test_context

    route = '/api/v1/accounts/1000'
    res = test_client.get(route)
    res_json = res.get_json()

    assert res.status_code == 404
    assert res.get_json() == { "error": "Account with id 1000 does not exist" }
