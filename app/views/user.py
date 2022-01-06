from  flask import (Blueprint,jsonify, render_template, redirect, request, url_for, abort, flash)
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer
from app import app, models, db
from app.forms import user as user_forms
from datetime import datetime
from ..models import User, Sales, Stock, Accounts
import os, json


ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

#create user blueprint
userbp = Blueprint('userbp', __name__, url_prefix='/user')
@userbp.route('/signup', methods=['GET','POST'])
def signup():
    form = user_forms.SignUp()
    if form.validate_on_submit():
        #create a new user
        user = models.User(
            first_name= form.first_name.data,
            last_name = form.last_name.data,
            password = form.password.data
            )
        db.session.add(user)
        db.session.commit()
        flash('Registration completed succesfully.', 'positive')
        return redirect(url_for('index'))
    return render_template('user/signup.html', form=form, title='Sign Up')

@userbp.route('/signin', methods=['GET','POST'])
def signin():
    form = user_forms.Login()
    if form.validate_on_submit():
        user = User.query.filter_by(first_name=form.first_name.data).first()
        #check if user exists
        if user is not None:
            #check the password is correct
            if user.check_password(form.password.data):
                login_user(user)
                flash('Succesfully signed in.','positive')
                return redirect(url_for('userbp.sellingpoint'))
            else:
                flash('The password you have entered is wrong.','negative')
                return redirect('userbp.signin')
        else:
            flash('Unknown username', 'negative')
            return redirect(url_for('userbp.signin'))
    return render_template('/user/signin.html', form=form, title='Log-In')

@userbp.route('/signout')
def signout():
    logout_user()
    flash('You have been logged out', 'positive')
    return redirect(url_for('userbp.signin'))


@userbp.route('/sellingpoint', methods=['GET','POST'])
def sellingpoint():
    form = user_forms.Salespoint()
    if form.validate_on_submit():
        sold= Sales(
            price = form.price.data,
            quantity = form.quantity.data,
            percentage_profit = form.percentage_profit.data
            )
        db.session.add(sold)
        db.session.commit()
        flash('Sale captured', 'positive')
        return redirect(url_for('userbp.sellingpoint'))
    
    return render_template('user/sellingpoint.html', form=form, title='sales page', current_time=datetime.utcnow())

@userbp.route('/salesheet', methods=['GET'])
def salesheet():
    page = request.args.get('page', 1, type=int)
    pagination =models.Sales.query.order_by(models.Sales.timestamp.desc()).paginate(page, error_out=False)
    sales = pagination.items
    return render_template('showsales.html', sales=sales, pagination=pagination, current_time=datetime.utcnow())


@userbp.route('/accounts/<int:id>', methods=['GET','POST'])
def accounts(id):
    account = models.Accounts.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (account.itemz.count() -1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE']+1
    pagination = account.itemz.paginate(page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    productz = pagination.items
    return render_template('showaccounts.html', accounts=[account], productz=productz, pagination=pagination, page=page)


@app.route('/', methods=['GET','POST'])
def index():
    if current_user.is_authenticated:

        page = request.args.get('page', 1 , type= int)
        pagination = Account.query.paginate(page, error_out=False)
        accounts = pagination.items
        return render_template('index.html', accounts=accounts, pagination=pagination, current_time=datetime.utcnow())
    return redirect(url_for('userbp.signin'))
        
@app.route('/home')
def upload_form():
    return render_template('autocomplete.html')


@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        term = (request.form['q']).lower()
        print ('term: ', term)
        
        """SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "data", "results.json")
        try:
            with open('results.json','r') as f:   
                json_data = json.loads((f.read()).lower())
        except:    
            raise IOError('results.json file not found.')                 
        #json_data = json.loads(open(json_url).read())
        #print (json_data)
        #print (json_data[0])
        
        f = open("results.json", mode='w') 
        for value in models.Stock.query.all():
        value = value.product_type
        f.write(value)
        f.close()
        except:
            raise IOError('write operation to file failed.')"""
        
        data_list = []
        z  = open("results.json", 'r')
        while z.readline() != '':
            json_data = (z.readline()).lower()
            data_list.append(json_data)
        print(data_list)
        for v in json_data:
            print(v)
        
        filtered_dict = [v for v in data_list if term in v]	
        print(filtered_dict)
        """
        resp = jsonify(filtered_dict)
        resp.status_code = 200"""
        return render_template('autocomplete.html', filtered_dict = filtered_dict, q='q')    
    return render_template('autocomplete.html')


@app.route('/addstock', methods=['POST', 'GET'])
def addstock():
    form = user_forms.AddStock()
    if form.validate_on_submit():
        stock = models.Stock(
            product_type = form.product_type.data,
            quantity = form.quantity.data,
            manufacturer = form.manufacturer.data,
            purchase_price = form.purchase_price.data
            )
        db.session.add(stock)
        db.session.commit()
        flash('The stock has been added to the database', 'positive')
        redirect(url_for('index'))
    return render_template('addstock.html',form=form)    


f = open("results.json", mode='w')
for value in Stock.query.order_by(Stock.timestamp.desc()):
    f.write(str(value.product_type) + '\n')
f.close()
      
