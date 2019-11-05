from flask import request, json, Response, Blueprint
from ..models.TransactionModel import TransactionModel, TransactionSchema
from ..models.AccountModel import AccountModel, AccountSchema

transaction_api = Blueprint('transactions', __name__)
transaction_schema = TransactionSchema()

@transaction_api.route('/', methods=['POST'])
def create():
  """
  Create Transaction Function
  """
  req_data = request.get_json()
  data = transaction_schema.load(req_data)

  from_account_id = data.get('from_account_id')
  to_account_id = data.get('to_account_id')
  amount = data.get('amount')

  from_account = AccountModel.get_account_for_balance_update(from_account_id)
  to_account = AccountModel.get_account_for_balance_update(to_account_id)

  if from_account is None:
      message = 'Account with id ' + str(from_account_id) + ' does not exist'
      return custom_response(message, 400)

  if to_account is None:
      message = 'Account with id ' + str(to_account_id) + ' does not exist'
      return custom_response(message, 400)

  if from_account.balance < amount:
      message = 'Account with number ' + from_account.account_number + ' does not have enough money to make this transaction'
      return custom_response(message, 400)

  transaction = TransactionModel(data)
  transaction.save()

  from_account.update({ 'balance': from_account.balance - amount })
  to_account.update({ 'balance': to_account.balance + amount })


  message = 'Successfully transferred ' + str(amount) + ' from ' + from_account.account_number + ' to ' + to_account.account_number
  return custom_response({'transaction': message}, 201)


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
