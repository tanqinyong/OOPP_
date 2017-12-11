from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired

# e.g. from Patient import Patient
from Food_Order import FoodOrder

import firebase_admin
from firebase_admin import credentials, db


cred = credentials.Certificate('cred/oopp-4e3a2-firebase-adminsdk-njuhh-69bc3a7f98.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopp-4e3a2.firebaseio.com/'
})

root = db.reference()

app = Flask(__name__)


class NurseCallForm(Form):
    pass # the description & form (input text button shit like that) also ya the urgency and description thing try to be specific (headache heartattack)


class FoodOrderForm(Form):
    foodname = SelectField('Food Choices', choices = [('chk','Chicken'),('fsh','fish'),('bf','beef')])
    patientname = StringField('Name:')
    quantity = StringField('Quantity:')
    totalprice = 0
    waitingtime = 0
    submit = SubmitField('Enter')


@app.route('/')
def render_login():
    return render_template('login.html')


@app.route('/nursecallpage/')
def render_nurse():
    return render_template('nursecallpage.html')


@app.route('/patient_info/')
def render_patient_info():
    return render_template('patient_info.html')


@app.route('/trainee_notes/')
def render_trainee_notes():
    return render_template('trainee_notes.html')


@app.route('/billing/')
def render_billing():
    return render_template('billing.html')


@app.route('/remote_doctor/')
def render_remote_doctor():
    return render_template('remote_doctor.html')


@app.route('/speech_to_text/')
def render_speech_to_text():
    return render_template('speech_to_text.html')


@app.route('/menu/', methods = ['GET','POST'])
def render_menu():
    form = FoodOrderForm(request.form)

    if request.method =='POST':
        # if form.validate() == False:
        #     return render_template('menu.html', form=form)
        # else:
            neworder = FoodOrder(form.foodname.data,form.patientname.data,form.quantity.data,0,0 )
            neworder_db = root.child('Food_Order')
            neworder_db.push ({
            'foodname':neworder.get_foodname(),
            'patientname':neworder.get_patientname(),
            'quantity':0,
            'price':0,
            'waitingtime':0
        })
            return 'Success!'

    elif request.method =='GET':
        return render_template('menu.html', form=form)


@app.route('/patient_info_editor/')
def render_patient_info_editor():
    return render_template('patient_info_editor.html')


if __name__ == '__main__':
    app.secret_key = 'icare1729'
    app.run()


