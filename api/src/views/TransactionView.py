import threading
import sqlalchemy
from flask import request, json, Response, Blueprint
from ..models.TransactionModel import TransactionModel, TransactionSchema
from ..models.AccountModel import AccountModel, AccountSchema
from ..shared.exceptions import InsufficientFunds

transaction_api = Blueprint('transactions', __name__)
transaction_schema = TransactionSchema()

@transaction_api.route('/', methods=['POST'])
def create_transaction():
    req_data = request.get_json()
    data = transaction_schema.load(req_data)

    from_account_id = data.get('from_account_id')
    to_account_id = data.get('to_account_id')
    amount = data.get('amount')

    try:
        AccountModel.remove_money_from_account(from_account_id, amount)
        AccountModel.add_money_to_account(to_account_id, amount)

    except sqlalchemy.orm.exc.NoResultFound:
        return custom_response({ "error": "Account with id {} does not exist".format(str(from_account_id)) }, 403)
    except InsufficientFunds:
        return custom_response({ "error": str(InsufficientFunds) }, 403)

    transaction = TransactionModel(data)
    transaction.save()

    message = 'Successfully transferred {} from account with id {} to account with id {}'.format(transaction.amount, from_account_id, to_account_id)
    return custom_response({'transaction': message}, 201)


def custom_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
