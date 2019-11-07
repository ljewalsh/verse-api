from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

__all__ = ["UserModel", "AccountModel", "TransactionModel"]

