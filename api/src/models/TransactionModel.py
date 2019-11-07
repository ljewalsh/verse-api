from marshmallow import fields, Schema
import datetime
from . import db

class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.from_account_id = data.get('from_account_id')
        self.to_account_id = data.get('to_account_id')
        self.amount = data.get('amount')
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_transactions():
        return TransactionModel.query.all()

    @staticmethod
    def get_one_transaction(id):
        return TransactionModel.query.get(id)

    def __repr(self):
        return '<id {}>'.format(self.id)

class TransactionSchema(Schema):
  id = fields.Int(dump_only=True)
  from_account_id = fields.Int(required=True)
  to_account_id = fields.Int(required=True)
  amount = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
