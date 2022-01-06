from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column,DateTime,String,Integer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db, bcrypt



class User(db.Model, UserMixin):
    """ user accounts on the websites."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    _password = db.Column(db.String)
    #sales = db.relationship('Sales', backref='seller', lazy='dynamic')

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
    @hybrid_property
    def password(self):
        return self._password
    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext)
    def check_password(self, plaintext):
        return check_password_hash(self.password, plaintext)
        

class Sales(db.Model):
    """Sales made from the shop ,unique to each user"""
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String )
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    percentage_profit = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

class Stock(db.Model):
    """ the current available stock in the business."""
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String) # db.ForeignKey('sales.id'))
    quantity = db.Column(db.String)
    manufacturer = db.Column(db.String)
    purchase_price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    product_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

class Accounts(db.Model):
    """ The constitutent products of each account."""
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index= True)
    comments = db.Column(db.String)
    purchase_date = db.Column(db.DateTime, index=True)
    itemz = db.relationship('Stock', backref='product', lazy='dynamic')














