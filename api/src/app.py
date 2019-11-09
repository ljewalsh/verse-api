from flask import Flask

from .config import app_config
from .models import db, bcrypt
from .models.UserModel import UserModel
from .models.AccountModel import AccountModel
from .models.TransactionModel import TransactionModel

from .views.UserView import user_api as user_blueprint
from .views.AccountView import account_api as account_blueprint
from .views.TransactionView import transaction_api as transaction_blueprint

def create_app(env_name):
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  bcrypt.init_app(app)
  db.init_app(app)

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(account_blueprint, url_prefix='/api/v1/accounts')
  app.register_blueprint(transaction_blueprint, url_prefix='/api/v1/transactions')

  return app

