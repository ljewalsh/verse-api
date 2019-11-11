from concurrent.futures import ThreadPoolExecutor
from src.models import db
from src.models.AccountModel import AccountModel
from tests.shared_methods import make_post_request

def test_create_account_success(test_context):
    test_client, dummy_user = test_context

    new_account = {
            "user_id": dummy_user.id,
            "balance": 5,
            "account_number": "test_create_account_success"
            }

    res = make_post_request('/api/v1/accounts/', test_client, new_account)

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

    res = make_post_request('/api/v1/accounts/', test_client, account_details)

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

def test_get_account_balance_during_transaction(test_context):
    test_client, dummy_user = test_context

    account = AccountModel({
            "user_id": dummy_user.id,
            "balance": 20,
            "account_number": "test_account_during_transaction"
    })

    account.save()

    to_account = AccountModel({
        "user_id": dummy_user.id,
        "balance": 0,
        "account_number": "test_to_account_during_transaction"
        })
    to_account.save()

    transaction_details = {
            "to_account_id": to_account.id,
            "from_account_id": account.id,
            "amount": 20
            }

    with ThreadPoolExecutor(2) as pool:
        first = pool.submit(make_post_request, ('/api/v1/transactions/'), (test_client), (transaction_details))

        second = pool.submit(test_client.get, '/api/v1/accounts/{}'.format(str(account.id)))

        requested_account = second.result().get_json()
        assert requested_account["balance"] == 0

def test_get_account_failure(test_context):
    test_client, dummy_user = test_context

    route = '/api/v1/accounts/1000'
    res = test_client.get(route)
    res_json = res.get_json()

    assert res.status_code == 404
    assert res.get_json() == { "error": "Account with id 1000 does not exist" }
