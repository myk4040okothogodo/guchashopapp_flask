from flask_wtf import Form
from wtforms import TextField, PasswordField, IntegerField
from wtforms.validators import (Required, Length, Email, ValidationError, EqualTo)


class Login(Form):
    """ user login form."""
    first_name = TextField(validators=[Required()], description="First-Name")
    password = PasswordField(validators=[Required()], description="Password")


class SignUp(Form):
    """ User sign up form."""
    first_name = TextField(validators=[Required(), Length(min=2)],
                           description="Name")
    last_name = TextField(validators=[Required(), Length(min=2)],
                          description="Surname")
    password = PasswordField(validators=[Required(), Length(min=6), EqualTo('confirm', message='Password must match.')],
                                         description='Password')

    confirm = PasswordField(description="confirm password")



class Salespoint(Form):
    product_type = TextField(validators=[Required(), Length(min=3)],
                             description="Product-Name")
    quantity = IntegerField( validators=[Required()],
                             description="no-of-products")
    price = IntegerField(validators=[Required()], description="product-price")
    percentage_profit = IntegerField(validators=[Required()],description="%-profit")

class AddStock(Form):
    product_type = TextField(validators=[Required(), Length(min=3)],
                             description="Product-Name")
    quantity = IntegerField( validators=[Required()],
                             description="no-of-products")
    purchase_price = IntegerField(validators=[Required()], description="product-price")
    manufacturer = TextField(validators=[Required()], description="manufacturer")    
