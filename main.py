# from crypt import methods
# from unicodedata import name
from flask import Flask, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, logout_user, current_user
# from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from predict.predict_views import predict_view

from db_stack import *
from db_stack import db


app = Flask(__name__, template_folder='templates')
model = pickle.load(open('model_dt_Classifier.pkl', 'rb')) # loading the trained model

ENV = 'dev'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:vu3jxg@localhost:3306/my_loan_db'
app.config['SECRET_KEY'] = 'jxg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt = Bcrypt(app)

## for managing our application and Flask_login to work together
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

## To reload the objects from the user_ids stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

## Create tables in the database
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)
    

# db.create_all()



## Create a RegisterForm
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    
    

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


## Create a loginform
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('prediction.enter_details'))
    return render_template('login.html', form=form)

## hashing the password is optional for the learners
@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data) ## creates a password hash
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/get_user_count')
def get_user_count():
    return redirect(url_for('user_count'))

# CREATE THE METADATA OBJECT TO ACCESS THE TABLE
@app.route('/user_count')
def user_count():
    result = db.session.query(User).count()
    male = User_details.query.filter_by(gender='male').count()
    female = User_details.query.filter_by(gender='female').count()
    Married = User_details.query.filter_by(married='yes').count()
    Unmarried = User_details.query.filter_by(married='no').count()
    not_graduate = User_details.query.filter_by(education='not graduate').count()
    Graduate = User_details.query.filter_by(education='graduate').count()
    rural_Property = User_details.query.filter_by(property_Area='rural').count()
    urban_Property = User_details.query.filter_by(property_Area='urban').count()
    semiurban_Property = User_details.query.filter_by(property_Area='semiurban').count()
    Application_Status_Approved = User_details.query.filter_by(application_Status='Approved').count()
    Application_Status_Not_Approved = User_details.query.filter_by(application_Status='Not Approved').count()
    return jsonify({'Number of registered users': result},{'Number of Male users': male}, 
                   {'Number of female users': female}, {'Married': Married},
                   {'Unmarried':Unmarried}, {'Not_graduate':not_graduate},
                   {'Graduate':Graduate},{'rural_Property':rural_Property},
                   {'urban_Property':urban_Property},{'semiurban_Property':semiurban_Property},
                   {'Application_Status_Approved':Application_Status_Approved}, {'Application_Status_Not_Approved':Application_Status_Not_Approved})
    # return jsonify({'Number of registered users': result})

@app.route('/summary_outcome')
def summary_outcome():
    result = db.session.query(User).count()
    loan_approved = User_details.query.filter_by(application_Status='Approved').count()
    approved_percentage = loan_approved*100/result
    return jsonify({'Percantage of users whose loan got approved': approved_percentage})


## Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
        # return render_template('login.html')

# register the blueprints
app.register_blueprint(predict_view)
db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=6622)
    app.config['TEMPLATES_AUTO_RELOAD'] = True