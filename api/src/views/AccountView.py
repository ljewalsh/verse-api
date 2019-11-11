from flask import request, json, Response, Blueprint
from ..models.AccountModel import AccountModel, AccountSchema

account_api = Blueprint('accounts', __name__)
account_schema = AccountSchema()

@account_api.route('/', methods=['POST'])
def create_account():
    req_data = request.get_json()
    data = account_schema.load(req_data)

    account_in_db = AccountModel.get_account_by_account_number(data.get('account_number'))
    if account_in_db:
        message = {'error': 'Account already exist, please supply another account number'}
        return custom_response(message, 400)

    account = AccountModel(data)
    account.save()

    ser_data = account_schema.dump(account)
    return custom_response(ser_data, 201)

@account_api.route('/<int:account_id>', methods=['GET'])
def get_a_account(account_id):
    account = AccountModel.get_one_account(account_id)
    if not account:
        return custom_response({'error': 'Account not found'}, 404)

    ser_data  = account_schema.dump(account)
    return custom_response(ser_data, 200)


def custom_response(res, status_code):
    return Response(
            mimetype="application/json",
            response=json.dumps(res),
            status=status_code
            )
