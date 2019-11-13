from flask import request, json, Response, Blueprint
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

@user_api.route('/', methods=['POST'])
def create_user():
  data = request.get_json()
  data = user_schema.load(data)

  user_in_db = UserModel.get_user_by_email(data.get('email'))
  if user_in_db:
    message = {'error': 'User already exist, please supply another email address'}
    return custom_response(message, 400)

  user = UserModel(data)
  user.save()

  ser_data = user_schema.dump(user)
  token = Auth.generate_token(ser_data['id'])

  return custom_response({ 'jwt_token': json.dumps(token) }, 201)


@user_api.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  if not email or not password:
    return custom_response({'error': 'An email and password is required to sign in'}, 400)

  user = UserModel.get_user_by_email(email)

  if not user:
    return custom_response({'error': 'Invalid credentials'}, 400)

  if not user.check_hash(password):
    return custom_response({'error': 'Invalid credentials'}, 400)

  token = Auth.generate_token(user.id)
  return custom_response({'jwt_token': token }, 200)

@user_api.route('/<int:target_user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id, target_user_id):
    if (user_id != target_user_id):
        return custom_response({ 'error': 'User with id {} does not have permission to view information about user with id {}'.format(str(user_id), str(target_user_id)) }, 403)
    user = UserModel.get_one_user(user_id)

    ser_data = user_schema.dump(user)
    del ser_data['password']
    return custom_response(ser_data, 200)

def custom_response(res, status_code):
  return Response(
    mimetype='application/json',
    response=json.dumps(res),
    status=status_code
  )
