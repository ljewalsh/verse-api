import threading
import datetime
from marshmallow import fields, Schema
from sqlalchemy import Index
from . import db
from .TransactionModel import TransactionSchema
from ..shared.exceptions import InsufficientFunds

class AccountModel(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    account_number = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    from_transactions = db.relationship('TransactionModel', backref='from_accounts', primaryjoin='AccountModel.id == TransactionModel.from_account_id', lazy=True)
    to_transactions = db.relationship('TransactionModel', backref='to_accounts', primaryjoin='AccountModel.id == TransactionModel.to_account_id', lazy=True)

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.balance = data.get('balance')
        self.account_number = data.get('account_number')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def remove_money_from_account(id, amount):
        account = AccountModel.query.filter_by(id=id).with_for_update().one()
        if (account.balance < amount):
            raise InsufficientFunds("Account with id {} does not have enough money to complete this transaction".format(str(id)))

        account.balance -= amount
        account.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def add_money_to_account(id, amount):
        account = AccountModel.query.filter_by(id=id).with_for_update().one()
        account.balance += amount
        account.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_all_accounts():
        return AccountModel.query.all()

    @staticmethod
    def get_one_account(id):
        return AccountModel.query.filter(AccountModel.id == id).with_for_update().first()

    @staticmethod
    def get_account_by_account_number(user_id, account_number):
        return AccountModel.query.filter(AccountModel.account_number == account_number, AccountModel.user_id == user_id).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

Index('unique_account_number_for_user', AccountModel.account_number, AccountModel.user_id, unique=True)

class AccountSchema(Schema):
  id = fields.Int(dump_only=True)
  user_id = fields.Int(required=True)
  account_number = fields.Str(required=True)
  balance = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  transactions = fields.Nested(TransactionSchema, many=True)
