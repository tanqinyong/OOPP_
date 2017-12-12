from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, SubmitField, SelectMultipleField, validators
# e.g. from Patient import Patient
from Food_Order import FoodOrder
from Nurse_call import NurseCall

from Patient_Info import Edit_Patient
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('cred/oopp-4e3a2-firebase-adminsdk-njuhh-69bc3a7f98.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopp-4e3a2.firebaseio.com/'
})

root = db.reference()

app = Flask(__name__)


class NurseCallForm(Form):
    problem = SelectMultipleField('Symptoms', choices=[("Heart","Heart"),("Extremities","Extremities"),("Headache","Headache"),("Stomach","Stomach"),("Nausea","Nausea"),("Breathing","Breathing")])
    submit = SubmitField('Enter')


class FoodOrderForm(Form):
    foodname = RadioField('Food Choices', choices = [('Chicken','Chicken'),('Fish','Fish'),('Beef','Beef'),('Pork','Pork')],default='Chicken')
    patientname = StringField('Name:',[validators.DataRequired(),validators.Length(min=1, max=30)])
    # quantity = StringField('Quantity:',[validators.DataRequired(),validators.Length(min=1, max=30)])
    qty = SelectField('Qty', choices=[('1', '1'), ('2', '2')], default='')
    submit = SubmitField('Enter')


class Patient_Info(Form):
        name = StringField("Name", [validators.Length(min=1, max=50), validators.DataRequired()])
        illness = StringField("Illness", [validators.Length(min=1, max=100), validators.DataRequired()])
        patientdesc = TextAreaField("Patient Description", [validators.DataRequired()])
        medicinedesc = TextAreaField("Medicine Description", [validators.DataRequired()])
        med1 = StringField("Medicine 1", [validators.Length(min=1, max=30), validators.DataRequired()])
        med2 = StringField("Medicine 2", [validators.Length(min=1, max=30), validators.DataRequired()])
        med3 = StringField("Medicine 3", [validators.Length(min=1, max=30), validators.DataRequired()])


@app.route('/')
def render_login():
    return render_template('login.html')


@app.route('/patient_info/')
def render_patient_info():
    patient_infos = root.child("patient_info").get()
    patient_id = "" #probably the login determine this
    for patid in patient_infos:
        eachpatient = patient_infos[patid]
        if patient_id == "":
            patientInfo = Edit_Patient(eachpatient["name"], eachpatient["illness"], eachpatient["patientdesc"], eachpatient["medicinedesc"], eachpatient["med1"], eachpatient["med2"], eachpatient["med3"])
            patientInfo.set_patid(patid)
    return render_template('patient_info.html', patient_infos = patientInfo)


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


@app.route('/nursecallpage/')
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
    return render_template('nursecallpage.html',orders = list)


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


@app.route('/update_order/<string:id>/', methods=['GET', 'POST'])
def update_order(id):
    form = FoodOrderForm(request.form)
    price = 0
    if request.method == 'POST' and form.validate():
        if form.foodname.data == 'Chicken':
            price = 5
        elif form.foodname.data == 'Fish' or 'Pork':
            price = 6
        elif form.foodname.data == 'Beef':
            price = 7
        neworder = FoodOrder(form.foodname.data, form.patientname.data, form.qty.data, price)
        neworder_db = root.child('Food_Order'+id)
        neworder_db.push({
            'foodname': neworder.get_foodname(),
            'patientname': neworder.get_patientname(),
            'quantity': neworder.get_quantity(),
            'price': neworder.get_price(),
        })
        flash('Updated Successfully!')
        return redirect(url_for("render_nurse"))
    else:
        url = 'Food_Order/' + id
        eachorder = root.child(url).get()
        neworder = FoodOrder(form.foodname.data, form.patientname.data, form.qty.data, price)
        neworder.set_foodid(id)
        form.foodname.data = neworder.get_foodname()
        form.patientname.data = neworder.get_patientname()
        form.qty.data = neworder.get_quantity()
    return redirect(url_for("render_nurse"))


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

        flash("Patient Infomation Successfully Updated.", "success")
        return redirect(url_for("render_patient_info"))

    return render_template('patient_info_editor.html', form=form)


#FOR UPDATING PATIENT INFO (MIGHT NEED IT)
# @app.route("/patient_edit/<string:id>/", methods=["GET", "POST"])
# def update_patient(id):
#     form = Patient_Info(request.form)
#     if request.method == "POST" and form.validate():
#         name = form.name.data
#         illness = form.illness.data
#         patientdesc = form.patientdesc.data
#         medicinedesc = form.medicinedesc.data
#         med1 = form.med1.data
#         med2 = form.med2.data
#         med3 = form.med3.data
#
#         pat = Edit_Patient(name, illness, patientdesc, medicinedesc, med1, med2, med3)
#         pat_db = root.child('patient_info/' + id)
#         pat_db.set({
#             "name": pat.get_name(),
#             "illness": pat.get_illness(),
#             "patientdesc": pat.get_patientdesc(),
#             "medicinedesc": pat.get_medicinedesc(),
#             "med1": pat.get_med1(),
#             "med2": pat.get_med2(),
#             "med3": pat.get_med3(),
#         })
#
#         flash("Patient Information Successfully Updated.", "success")
#         return redirect(url_for("render_patient_info"))
#
#     else:
#         url = "patient_info/" + id
#         eachpat = root.child(url).get()
#         patients = Edit_Patient(eachpat["name"], eachpat["illness"], eachpat["patientdesc"], eachpat["medicinedesc"], eachpat["med1"], eachpat["med2"], eachpat["med3"])
#
#         patients.set_patid(id)
#         form.name.data = patients.get_name()
#         form.illness.data = patients.get_illness()
#         form.patientdesc.data = patients.get_patientdesc()
#         form.medicinedesc.data = patients.get_medicinedesc()
#         form.med1.data = patients.get_med1()
#         form.med2.data = patients.get_med2()
#         form.med3.data = patients.get_med3()
#
#     return render_template("patient_edit.html", form=form)




if __name__ == '__main__':
    app.secret_key = 'icare1729'
    app.debug = True
    app.run()
    #app.run(host = '0.0.0.0', port = 5000) not sure if this is how you change it


