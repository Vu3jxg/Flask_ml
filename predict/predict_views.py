from optparse import Values
from flask import Blueprint,render_template,request
from flask_login import current_user
import pickle
import numpy as np
import sklearn
from db_stack import db, User, User_details

from db_stack import *

predict_view = Blueprint('prediction', __name__, template_folder="templates")
model = pickle.load(open('model_dt_Classifier.pkl', 'rb')) # loading the trained model

@predict_view.route('/prediction.enter_details')

## for entering details
def enter_details():
    return render_template('predict.html')

@predict_view.route('/prediction.predict',methods=['POST'])

def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    
    for i, j in zip(request.form.keys(), request.form.values()):
        if i == 'Gender':
            gender = 'male' if j == '1' else 'female'
            
        elif i == 'married':
            married = 'yes' if j == '1' else 'no'

        elif i == 'dependents':
            dependents = request.form['dependents']

        elif i == 'education':
            education = 'graduate' if j == '1' else 'not graduate'

        elif i == 'self_employed':
            self_employed = 'yes' if j == '1' else 'no'

        elif i == 'applicantincome':
            applicantincome = request.form['applicantincome']

        elif i == 'coapplicantincome':
            coapplicantincome = request.form['coapplicantincome']

        elif i == 'loanamount':
            loanamount = request.form['loanamount']

        elif i == 'loan_amount_term':
            loan_amount_term = request.form['loan_amount_term']

        elif i == 'credit_history':
            credit_history = 'yes' if j == '1' else 'no'

        elif i == 'property_area':
            if j == '0' :
                property_area = 'rural'
            elif j == '1' :
                property_area = 'urban'
            elif j == '2' :
                property_area = 'semiurban'

    applicationStatus = 'Approved' if prediction[0] == 1 else 'Not Approved'

    
    user_db = User_details.query.filter_by(user_name=current_user.username).first()
    if user_db:
        print(user_db.gender)
        user_db.gender = gender
        user_db.married = married
        user_db.dependents = dependents
        user_db.education = education
        user_db.self_employed = self_employed
        user_db.applicant_Income = applicantincome
        user_db.coapplicant_Income = coapplicantincome
        user_db.loan_amount = loanamount
        user_db.loan_term = loan_amount_term
        user_db.credit_History = credit_history
        user_db.property_Area = property_area
        user_db.application_Status = applicationStatus
        print(user_db.gender)
        db.session.commit()
    else:
        userDetails = User_details(user_name=current_user.username,gender=gender,married=married,dependents=dependents,
            education=education,self_employed=self_employed,applicant_Income=applicantincome,
            coapplicant_Income=coapplicantincome,loan_amount=loanamount,loan_term=loan_amount_term,
                              credit_History=credit_history,property_Area=property_area,
                              application_Status=applicationStatus)
        db.session.add(userDetails)
        db.session.commit()
    
    if prediction==0:
        return render_template('predict.html', prediction_text='Sorry:( you are not eligible for the loan ')
    else:
        return render_template('predict.html', prediction_text='Congrats!! you are eligible for the loan')