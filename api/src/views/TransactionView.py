import threading
from flask import request, json, Response, Blueprint
from ..models.TransactionModel import TransactionModel, TransactionSchema
from ..models.AccountModel import AccountModel, AccountSchema

transaction_api = Blueprint('transactions', __name__)
transaction_schema = TransactionSchema()

@transaction_api.route('/', methods=['POST'])
def create_transaction():
    req_data = request.get_json()
    data = transaction_schema.load(req_data)

    from_account_id = data.get('from_account_id')
    to_account_id = data.get('to_account_id')
    amount = data.get('amount')

    from_account = AccountModel.get_account_for_balance_update(from_account_id)
    to_account = AccountModel.get_account_for_balance_update(to_account_id)

    from_account_id = str(from_account_id)
    to_account_id = str(to_account_id)

    account_missing_message = 'Account with id {} does not exist'
    if from_account is None:
        message = { "error": account_missing_message.format(from_account_id) }
        return custom_response(message, 400)

    if to_account is None:
        message = { "error": account_missing_message.format(to_account_id) }
        return custom_response(message, 400)

    if from_account.balance < amount:
        message = { "error": "Account with id {} does not have enough money to make this transaction".format(from_account_id) }
        return custom_response(message, 400)

    transaction = TransactionModel(data)
    transaction.save()

    print ("I'm about to update the balance")
    from_account.update({ 'balance': from_account.balance - amount })
    to_account.update({ 'balance': to_account.balance + amount })

    message = 'Successfully transferred {} from account with id {} to account with id {}'.format(transaction.amount, from_account_id, to_account_id)
    return custom_response({'transaction': message}, 201)


def custom_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
