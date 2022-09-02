from flask import Flask, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__, template_folder='templates')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:vu3jxg@localhost:3306/my_loan_db'
app.config['SECRET_KEY'] = 'jxg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


## Create tables in the database
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    
    
# user_details:
class User_details(db.Model, UserMixin):
    __tablename__ = 'User_details'
    
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), db.ForeignKey("user.username"),unique=True)
    gender = db.Column(db.String(6), nullable= False)
    married = db.Column(db.String(10), nullable= False)
    dependents = db.Column(db.Integer, nullable= False)
    education = db.Column(db.String(20), nullable= False)
    self_employed = db.Column(db.String(10), nullable= False)
    applicant_Income = db.Column(db.Integer, nullable= False) 
    coapplicant_Income = db.Column(db.Integer, nullable= False)
    loan_amount = db.Column(db.Integer, nullable= False)
    loan_term = db.Column(db.Integer, nullable= False)
    credit_History = db.Column(db.String(10), nullable= False)
    property_Area = db.Column(db.String(20), nullable= False)
    application_Status = db.Column(db.String(20), nullable=False)
    
db.create_all()
db.session.commit()
    
    
    
    
