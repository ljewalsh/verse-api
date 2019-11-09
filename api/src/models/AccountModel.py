from marshmallow import fields, Schema
import datetime
from .TransactionModel import TransactionSchema
from . import db

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

    @staticmethod
    def get_all_accounts():
        return AccountModel.query.all()

    @staticmethod
    def get_one_account(id):
        return AccountModel.query.get(id)

    @staticmethod
    def get_account_for_balance_update(id):
        return AccountModel.query.filter_by(id=id).with_for_update().populate_existing().first()

    def get_account_by_account_number(account_number):
        return AccountModel.query.filter(AccountModel.account_number == account_number).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

class AccountSchema(Schema):
  id = fields.Int(dump_only=True)
  user_id = fields.Int(required=True)
  account_number = fields.Str(required=True)
  balance = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  transactions = fields.Nested(TransactionSchema, many=True)
