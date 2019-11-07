from flask import request, json, Response, Blueprint
from ..models.UserModel import UserModel, UserSchema

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

@user_api.route('/', methods=['POST'])
def create():
  """
  Create User Function
  """
  req_data = request.get_json()
  data = user_schema.load(req_data)

  user_in_db = UserModel.get_user_by_email(data.get('email'))

  if user_in_db:
    message = {'error': 'User already exist, please supply another email address'}
    return custom_response(message, 400)

  user = UserModel(data)
  user.save()

  ser_data = user_schema.dump(user)
  return custom_response({'user': ser_data}, 201)

@user_api.route('/<int:user_id>', methods=['GET'])
def get_a_user(user_id):
  """
  Get a single user
  """
  user = UserModel.get_one_user(user_id)
  if not user:
    return custom_response({'error': 'user not found'}, 404)

  ser_user = user_schema.dump(user)
  return custom_response(ser_user, 200)


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
