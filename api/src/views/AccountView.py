from flask import request, json, Response, Blueprint
from ..models.AccountModel import AccountModel, AccountSchema

account_api = Blueprint('accounts', __name__)
account_schema = AccountSchema()

@account_api.route('/', methods=['POST'])
def create_account():
    req_data = request.get_json()
    data = account_schema.load(req_data)
    account_number = data.get('account_number')
    user_id = data.get('user_id')

    account_in_db = AccountModel.get_account_by_account_number(user_id, account_number)
    if account_in_db:
        message = {'error': 'Account with account_number {} already exist for user_id {}, please supply another account number'.format(account_number, str(user_id))}
        return custom_response(message, 403)

    account = AccountModel(data)
    account.save()

    ser_data = account_schema.dump(account)
    return custom_response(ser_data, 201)

@account_api.route('/<int:account_id>', methods=['GET'])
def get_a_account(account_id):
    account = AccountModel.get_one_account(account_id)
    if not account:
        return custom_response({'error': 'Account with id {} does not exist'.format(str(account_id)) }, 404)

    ser_data  = account_schema.dump(account)
    return custom_response(ser_data, 200)


def custom_response(res, status_code):
    return Response(
            mimetype="application/json",
            response=json.dumps(res),
            status=status_code
            )
