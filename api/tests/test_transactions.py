import json
from concurrent.futures import ThreadPoolExecutor
from src.models import db
from src.models.UserModel import UserModel
from src.models.AccountModel import AccountModel

def make_post_request(test_client, transaction_details):
    res = test_client.post('/api/v1/transactions/', data=json.dumps(transaction_details), content_type='application/json')
    return res

def test_create_transaction(test_context):
    test_client, dummy_user = test_context

    to_account  = AccountModel({
            "user_id": dummy_user.id,
            "balance": 0,
            "account_number": "to_account",
            })
    to_account.save()

    from_user = UserModel({
            "username": "from_account",
            "email": "from@account.com",
            "password": "test_password"
            })
    from_user.save()

    from_account = AccountModel({
            "user_id": from_user.id,
            "balance": 20,
            "account_number": "from_account"
            })
    from_account.save()

    transaction_details = {
            "to_account_id": to_account.id,
            "from_account_id": from_account.id,
            "amount": 20
            }

    res = make_post_request(test_client, transaction_details)
    assert res.status_code == 201

    updated_from_account = AccountModel.get_one_account(from_account.id)
    updated_to_account = AccountModel.get_one_account(to_account.id)

    assert updated_from_account.balance == 0
    assert updated_to_account.balance == 20

def test_create_transaction_locking(test_context):
    test_client, dummy_user = test_context

    to_account  = AccountModel({
            "user_id": dummy_user.id,
            "balance": 0,
            "account_number": "to_account_locking",
            })
    to_account.save()

    from_user = UserModel({
            "username": "from_account_locking",
            "email": "from@account_locking.com",
            "password": "test_password"
            })
    from_user.save()

    from_account = AccountModel({
            "user_id": from_user.id,
            "balance": 20,
            "account_number": "from_account_locking"
            })
    from_account.save()

    transaction_details = {
            "to_account_id": to_account.id,
            "from_account_id": from_account.id,
            "amount": 20
            }

    with ThreadPoolExecutor(2) as pool:
        first = pool.submit(make_post_request, (test_client), (transaction_details))
        second = pool.submit(make_post_request, (test_client), (transaction_details))

        assert first.result().status_code == 201
        assert second.result().status_code == 403

    db.session.expire(from_account)
    db.session.expire(to_account)

    updated_from_account = AccountModel.get_one_account(from_account.id)
    updated_to_account = AccountModel.get_one_account(to_account.id)

    assert updated_from_account.balance == 0
    assert updated_to_account.balance == 20


