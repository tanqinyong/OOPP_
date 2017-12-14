# For Scaledrone - Trainee page messaging API

import requests
from requests.auth import HTTPBasicAuth

BASE_URL = 'https://api2.scaledrone.com'

class ScaleDrone:

    def __init__(self, channel_id, secret_key, base_url=BASE_URL):
        auth = HTTPBasicAuth(channel_id, secret_key)
        self.auth = auth
        self.base_url = base_url + '/' + channel_id + '/'

    def publish(self, room, data = {}):
        url = self.base_url + room + '/publish'
        return requests.post(url, data=data, auth=self.auth)

    def channel_stats(self):
        url = self.base_url + 'stats'
        return requests.get(url, auth=self.auth)

    def users_list(self):
        url = self.base_url + 'users'
        return requests.get(url, auth=self.auth)


import unittest
from scaledrone import ScaleDrone

drone = ScaleDrone('SNazg8KrKdwSphWf', 'fCw1xxKBLoYBFZuif4vRKgK3ibIdH6mk')


class Test(unittest.TestCase):

    def test_publish(self):
        r = drone.publish('notifications', {'foo': 'bar'})
        self.assertEqual(r.status_code, 200)

    def test_publish(self):
        r = drone.channel_stats()
        self.assertTrue('users_count' in r.json())
        self.assertEqual(r.status_code, 200)

    def users_list(self):
        r = drone.users_list()
        self.assertTrue('users' in r.json())
        self.assertEqual(r.status_code, 200)


room = 'notifications'
message = {'foo': 'bar'}
response = drone.publish(room, message)
response = drone.channel_stats()
response = drone.users_list()







# Flask, WTForms and cool shit
from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, SubmitField, SelectMultipleField, validators, widgets, PasswordField
import random

# Classes and shit
from Food_Order import FoodOrder
from Nurse_call import NurseCall
from Patient_Info import Edit_Patient
from Admin import Staff, Patient

# Database shit
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('cred/oopp-4e3a2-firebase-adminsdk-njuhh-69bc3a7f98.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopp-4e3a2.firebaseio.com/'
})
root = db.reference()

app = Flask(__name__)


class LoginForm(Form):
    username = StringField('Staff ID:', [validators.DataRequired()])
    password = PasswordField('Password:', [validators.DataRequired()])
    submit = SubmitField('Login')


class NurseCallForm(Form):
    problem = SelectMultipleField('Symptoms', choices=[("Heart","Heart"),("Extremities","Extremities"),("Headache","Headache"),("Stomach","Stomach"),("Nausea","Nausea"),("Breathing","Breathing")],option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Enter')


class FoodOrderForm(Form):
    foodname = RadioField('Food Choices', choices = [('Chicken','Chicken'),('Fish','Fish'),('Beef','Beef'),('Pork','Pork')],default='Chicken')
    patientname = StringField('Name:',[validators.DataRequired(),validators.Length(min=1, max=30)])
    qty = SelectField('Qty', choices=[('1', '1'), ('2', '2'),('3','3'),('4','4'),('5','5')], default='')
    submit = SubmitField('Enter')


class Patient_Info(Form):
    name = StringField("Name", [validators.Length(min=1, max=50), validators.DataRequired()])
    illness = StringField("Illness", [validators.Length(min=1, max=100), validators.DataRequired()])
    patientdesc = TextAreaField("Illness Description", [validators.DataRequired()])
    medicinedesc = TextAreaField("Medicine Description", [validators.DataRequired()])
    med1 = StringField("Medicine 1", [validators.Length(min=1, max=30), validators.DataRequired()])
    med2 = StringField("Medicine 2")
    med3 = StringField("Medicine 3")


class AdminForm(Form):
    type = RadioField('Type: ', choices=[('Staff','Staff'),('Patient','Patient')])
    nric = StringField("NRIC: ", [validators.Length(min=1, max=9), validators.DataRequired()])
    name = StringField("Name: ", [validators.Length(min=1, max=30), validators.DataRequired()])


class PatientLogin(Form):
    username = StringField("Patient ID: ",[validators.Length(min=1, max=7), validators.DataRequired()])
    password = PasswordField("Password: ",[validators.Length(min=1, max=9), validators.DataRequired()])


@app.route('/', methods=['GET','POST'])
def render_login():
    form = PatientLogin(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data

        validate = root.child('Patient').order_by_child("username").equal_to(username).get()

        for i, j in validate.items():
            print(i, j)
            print(j['username'])
            if username == j['username'] and password == j['password']:
                session['logged_in'] = True
                return redirect(url_for('render_nurse'))
            else:
                error = "Invalid Login"
                flash(error, "danger")
    return render_template('login.html', form=form)


@app.route('/Admin/',methods=['GET','POST'])
def render_admin():
    admin_form = AdminForm(request.form)
    if request.method == 'POST' and admin_form.validate():
        if admin_form.type.data == 'Staff':
            username = 'S' + str(random.randint(10000, 99999))
            new_staff = Staff(admin_form.name.data,admin_form.nric.data,username)
            new_staff_db = root.child('Staff')
            new_staff_db.push ({

                'username': new_staff.get_username(),
                'name': new_staff.get_name(),
                'password': new_staff.get_nric()

            })
            flash(new_staff.get_name() +' added!(Staff)'+ ' User = '+username + ' Password = '+new_staff.get_nric(), 'success')

        elif admin_form.type.data == 'Patient':
            username = 'P' + str(random.randint(10000, 99999))
            new_patient = Patient(admin_form.name.data,admin_form.nric.data,username)
            new_patient_db = root.child('Patient')
            new_patient_db.push({
                'name': new_patient.get_name(),
                'password': new_patient.get_nric(),
                'username': new_patient.get_username()
            })
            flash(new_patient.get_name() +' added!(Patient)'+ ' User = '+username + ' Password = '+new_patient.get_nric(), 'success')

    return render_template('Admin.html',form=admin_form)


@app.route('/patient_info/')
def render_patient_info():
    try:
        patient_infos = root.child("patient_info").get()
        patient_id = "" #probably the login determine this
        for patid in patient_infos:
            eachpatient = patient_infos[patid]
            if patient_id == "":
                patientInfo = Edit_Patient(eachpatient["name"], eachpatient["illness"], eachpatient["patientdesc"], eachpatient["medicinedesc"], eachpatient["med1"], eachpatient["med2"], eachpatient["med3"])
                patientInfo.set_patid(patid)
        return render_template('patient_info.html', patient_infos = patientInfo)

    except TypeError:
        flash("No patient left in the database!", "danger")
        return redirect(url_for("render_patient_info_editor"))


@app.route('/new 1/')
def render_new1():
    return render_template('new 1.html')


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


@app.route('/nursecallpage/',methods=['GET','POST'])
def render_nurse():
    # FOOD ORDER
        Food_Order = root.child('Food_Order').get()
        list = []
        for food_id in Food_Order:
            eachorder = Food_Order[food_id]
            order = FoodOrder(eachorder['foodname'],eachorder['patientname'],eachorder['price'],eachorder['quantity'])
            order.set_foodid(food_id)
            list.append(order)

    # NURSE CALL
        nurse_form = NurseCallForm(request.form)
        if request.method == 'POST' and nurse_form.validate():
            newcall = NurseCall(nurse_form.problem.data)
            newcall_db = root.child('Nurse Call')
            newcall_db.push ({
               'symptom': newcall.get_reason()
             })
            flash('A nurse will attend to you shortly.','success')
        return render_template('nursecallpage.html',orders = list,nurse = nurse_form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    print(request.method)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        validate = root.child('Staff').order_by_child("username").equal_to(username).get()

        for i, j in validate.items():
            print(i, j)
            print(j['username'])
            if username == j['username'] and password == j['password']:
                session['logged_in_staff'] = True
                return redirect(url_for('render_patient_info'))
            else:
                error = "Invalid Login"
                flash(error, "danger")

    return render_template('StaffLogin.html', form=form)


@app.route('/logout/')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('render_login'))


@app.route('/staff_logout/')
def logout_staff():
    session.pop("logged_in_staff", None) #None is pass in as the "default" value (else it will return its "default" value)
    flash('You are now logged out', 'success')
    return redirect(url_for('render_nurse'))


@app.route('/menu/', methods = ['GET','POST'])
def render_menu():
    form = FoodOrderForm(request.form)
    price = 0
    if request.method =='POST' and form.validate():
            if form.foodname.data == 'Chicken':
                price = 5
            elif form.foodname.data == 'Fish' or 'Pork':
                price = 6
            elif form.foodname.data == 'Beef':
                price = 7
            neworder = FoodOrder(form.foodname.data,form.patientname.data,form.qty.data,price)
            neworder_db = root.child('Food_Order')
            neworder_db.push ({
            'foodname': neworder.get_foodname(),
            'patientname': neworder.get_patientname(),
            'quantity': neworder.get_quantity(),
            'price': neworder.get_price(),
            })
            flash('Success!','success')
            return redirect(url_for("render_nurse"))

    elif request.method == 'GET':
        return render_template('menu.html', form=form)
    return render_template('menu.html', form=form)


# @app.route('/update_order/<string:id>/', methods=['GET', 'POST'])
# def update_order(id):
#     form = FoodOrderForm(request.form)
#     price = 0
#     if request.method == 'POST' and form.validate():
#         if form.foodname.data == 'Chicken':
#             price = 5
#         elif form.foodname.data == 'Fish' or 'Pork':
#             price = 6
#         elif form.foodname.data == 'Beef':
#             price = 7
#         neworder = FoodOrder(form.foodname.data, form.patientname.data, form.qty.data, price)
#         neworder_db = root.child('Food_Order/'+id)
#         neworder_db.push({
#             'foodname': neworder.get_foodname(),
#             'patientname': neworder.get_patientname(),
#             'quantity': neworder.get_quantity(),
#             'price': neworder.get_price(),
#         })
#         flash('Updated Successfully!')
#         return render_template('nursecallpage.html', order=form)
#         #return redirect(url_for("render_nurse"))
#     else:
#         url = 'Food_Order/' + id
#         eachorder = root.child(url).get()
#         neworder = FoodOrder(eachorder['foodname'],eachorder['patientname'],eachorder['quantity'],eachorder['price'])
#         neworder.set_foodid(id)
#         form.foodname.data = neworder.get_foodname()
#         form.patientname.data = neworder.get_patientname()
#         form.qty.data = neworder.get_quantity()
#     return render_template('nursecallpage.html',order=form, nurse = "",orders="")


@app.route('/delete_order/<string:id>', methods=['POST'])
def delete_order(id):
    order_db = root.child('Food_Order/' + id)
    order_db.delete()
    flash('Order Deleted', 'success')

    return redirect(url_for('render_nurse'))


@app.route('/patient_info_editor/', methods=["GET", "POST"])
def render_patient_info_editor():
    form = Patient_Info(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        illness = form.illness.data
        patientdesc = form.patientdesc.data
        medicinedesc = form.medicinedesc.data
        med1 = form.med1.data
        med2 = form.med2.data
        med3 = form.med3.data

        pat = Edit_Patient(name, illness, patientdesc, medicinedesc, med1, med2, med3)
        pat_db = root.child('patient_info')
        pat_db.push({
            "name": pat.get_name(),
            "illness": pat.get_illness(),
            "patientdesc": pat.get_patientdesc(),
            "medicinedesc": pat.get_medicinedesc(),
            "med1": pat.get_med1(),
            "med2": pat.get_med2(),
            "med3": pat.get_med3(),
        })

        flash("Patient Information Successfully Updated.", "success")
        return redirect(url_for("render_patient_info"))

    return render_template('patient_info_editor.html', form=form)


@app.route("/patient_edit/<string:id>/", methods=["GET", "POST"])
def update_patient(id):
    form = Patient_Info(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        illness = form.illness.data
        patientdesc = form.patientdesc.data
        medicinedesc = form.medicinedesc.data
        med1 = form.med1.data
        med2 = form.med2.data
        med3 = form.med3.data

        pat = Edit_Patient(name, illness, patientdesc, medicinedesc, med1, med2, med3)
        pat_db = root.child('patient_info/' + id)
        pat_db.set({
            "name": pat.get_name(),
            "illness": pat.get_illness(),
            "patientdesc": pat.get_patientdesc(),
            "medicinedesc": pat.get_medicinedesc(),
            "med1": pat.get_med1(),
            "med2": pat.get_med2(),
            "med3": pat.get_med3(),
        })

        flash("Patient Information Successfully Updated.", "success")
        return redirect(url_for("render_patient_info"))

    else:
        url = "patient_info/" + id
        eachpat = root.child(url).get()
        patients = Edit_Patient(eachpat["name"], eachpat["illness"], eachpat["patientdesc"], eachpat["medicinedesc"], eachpat["med1"], eachpat["med2"], eachpat["med3"])

        patients.set_patid(id)
        form.name.data = patients.get_name()
        form.illness.data = patients.get_illness()
        form.patientdesc.data = patients.get_patientdesc()
        form.medicinedesc.data = patients.get_medicinedesc()
        form.med1.data = patients.get_med1()
        form.med2.data = patients.get_med2()
        form.med3.data = patients.get_med3()

    return render_template("patient_edit.html", form=form)


@app.route("/patient_delete/<string:id>", methods=["POST"])
def delete_patient(id):
    pat_db = root.child("patient_info/" + id)
    pat_db.delete()
    flash("Patient's information has been delete", "success")

    return redirect(url_for("render_patient_info"))


if __name__ == '__main__':
    app.secret_key = 'icare1729'
    app.debug = True
    app.run()
    #app.run(host = '0.0.0.0', port = 5000) not sure if this is how you change it
