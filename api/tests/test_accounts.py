import json
from src.models import db
from src.models.AccountModel import AccountModel

def test_create_account(test_context):
    test_client, dummy_user = test_context

    new_account = {
            "user_id": dummy_user.id,
            "balance": 5,
            "account_number": "test_account_number"
            }

    res = test_client.post('/api/v1/accounts/', data=json.dumps(new_account), content_type='application/json')

    created_account = AccountModel.query.filter(AccountModel.account_number == "test_account_number")

    assert created_account is not None
    assert res.status_code == 201


def test_get_account(test_context):
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
