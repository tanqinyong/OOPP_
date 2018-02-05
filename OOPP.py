# Flask, WTForms and cool shit
from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, SubmitField, SelectMultipleField, validators, widgets, PasswordField, DateField, FileField, IntegerField
from werkzeug.utils import secure_filename
import random, datetime, os
from datetime import timedelta, date
from datetime import timedelta
import time
from threading import Timer
# Classes and shit
from Food_Order import FoodOrder
# from Nurse_call import NurseCall
# from Patient_Info import Edit_Patient
from Hospital import *
from scaledrone import Scaledrone
import json
# from Admin import Staff, Patient

# TWILIO
# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
# from twilio.rest import Client
# # Find these values at https://twilio.com/user/account
# account_sid = "AC6ced1d481c8e1d8ec33c4f0da613e3e8"
# auth_token = "5554f393e7cf77b1496cb9f2de0d61e2"
# client = Client(account_sid, auth_token)


UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# Database shit
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('cred/oopp-4e3a2-firebase-adminsdk-njuhh-69bc3a7f98.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopp-4e3a2.firebaseio.com/'
})
root = db.reference()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "toUUtBRQZqXHdVPLXDQH0FbIRs3heozyVGZPigXJ"
app.config['SESSION_TYPE'] = 'filesystem'


class LoginForm(Form):
    username = StringField('Staff ID:', [validators.DataRequired()])
    password = PasswordField('Password:', [validators.DataRequired()])
    submit = SubmitField('Login')


# Login Page
class PatientLogin(Form):
    username = StringField("User ID: ",[validators.Length(min=1, max=7), validators.DataRequired()])
    password = PasswordField("Password: ",[validators.Length(min=1, max=9), validators.DataRequired()])


# Nurse Call Page
class NurseCallForm(Form):
    problem = SelectMultipleField("", choices=[("Heart","Heart"),("Extremities","Extremities"),("Headache","Headache"),("Stomach","Stomach"),("Nausea","Nausea"),("Breathing","Breathing")],option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Enter')


# Menu Page
class FoodOrderForm(Form):
    foodname = RadioField('Food Choices:', choices = [('Indian Cuisine','Indian Cuisine'),('Malay Cuisine','Malay Cuisine'),('Chinese Cuisine','Chinese Cuisine'),('Western Cuisine','Western Cuisine'),('International Cuisine','International Cuisine')],default='international')
    indian = RadioField('Indian Meals:', [validators.Optional()], default="", choices = [('Appam', 'Appam'), ('Prata w/ Chicken Curry', 'Prata w/ Chicken Curry'),('Nazi Briyani', 'Nazi Briyani')])
    malay = RadioField('Malay Meals', [validators.Optional()] , default="", choices = [('Mee Rebus','Mee Rebus'),('Nazi Lemak','Nazi Lemak'),('Mee Siam','Mee Siam')])
    chinese = RadioField('Chinese Meals', [validators.Optional()] , default="", choices = [('Chicken Rice','Chicken Rice'),('Shredded Chicken Porridge','Shredded Chicken Porridge'),('Handmade noodles','Handmade noodles')])
    western = RadioField('Western Meals', [validators.Optional()] , default="", choices = [('Chicken Chop','Chicken Chop'),('Fish & Chips','Fish & Chips'),('Bolognese Spaghetti','Bolognese Spaghetti')])
    international = RadioField('International Meals', [validators.Optional()] , default="", choices = [('Paella','Paella'),('Swedish Meatballs & Mashed Potatoes','Swedish Meatballs & Mashed Potatoes'),('Mediterranean Grilled Bass','Mediterranean Grilled Bass')])
    submit = SubmitField('')


# Trainee page
# class TraineeForm(Form):
#    name = StringField('Name:',[validators.DataRequired(),validators.Length(min=1, max=30)])
#    comment = TextAreaField('Comment:')
#    submit = SubmitField('Enter')


# Patient info page
class Patient_Medicine(Form):
    #Medicine names are not to be trusted as they were randomly taken from Google search!!!
    medName = SelectField("Medicine Name", choices=[("select","--Select A Medicine--"), ("Dextromethorphan (Cough)", "Dextromethorphan (Cough)"), ("Paracetamol (Cold)", "Paracetamol (Cold)"),
                                                    ("Acetaminophen (Fever)", "Acetaminophen (Fever)"), ("Antiemetic (Nausea)", "Antiemetic (Nausea)"), ("Diclofenac (Stomach Ache)", "Diclofenac (Stomach Ache)")], default="select")
    medDesc = TextAreaField("Medicine Description", [validators.DataRequired()])
    medDosage = IntegerField("Dosage")
    sideEffect = StringField("Side Effect")
    medInterval = SelectField("Hours for patient to take med", choices=[("6","6"),("8","8"),("12","12")], default="")
    submitMed = SubmitField("")

class Patient_Info(Form):
    name = StringField("Name")
    illness = StringField("Illness", [validators.Length(min=1, max=100), validators.DataRequired()])
    patientdesc = TextAreaField("Illness Description", [validators.DataRequired()])
    ward = SelectField("Ward: ", choices=[("select", "--Select Ward--"),("A", "A"),("B1","B1"), ("B2", "B2"), ("C","C")], default="select")
    submitInfo = SubmitField("")
    #https://wtforms.readthedocs.io/en/latest/fields.html#wtforms.fields.FieldList


class StaffProfile(Form):
    name = StringField("Name", [validators.Length(min=1, max=30), validators.DataRequired()])
    nric = StringField("NRIC")
    dob = StringField("DOB")  # , format='%d/%m/%Y', validators=(validators.Optional(),))
    email = StringField("Email")
    address = StringField("Address", [validators.Length(min=1, max=30), validators.DataRequired()])
    gender = SelectField("Gender", choices=[("Male", "Male"), ("Female", "Female"), ("Others", "Others")], default="")
    phone_no = StringField("Contact No")
    username = StringField('Username')


# Admin Page
# validations not yet done for AdminForm!!!!!!!!!!
class AdminForm(Form):
    type = RadioField('Type: ', choices=[('Staff','Staff'),('Patient','Patient')])
    name = StringField("Name: ", [validators.Length(min=1, max=30), validators.DataRequired()])
    nric = StringField("NRIC: ", [validators.Length(min=1, max=9), validators.DataRequired()])
    dob =  StringField("Date of Birth: ")#, format='%d/%m/%Y', validators=(validators.Optional(),))
    email = StringField("Email: ")
    address = StringField("Address: ")
    gender = SelectField("Gender: ", choices=[("Male", "Male"), ("Female", "Female"), ("Others", "Others")], default="")
    occupation = StringField("Occupation: ")
    income = StringField("Household Income: ")
    bloodtype = SelectField("Blood Type: ", choices=[("O", "O"), ("A", "A"), ("B", "B"), ("AB", "AB")], default="")
    race = StringField("Race: ")
    phone_no = StringField("Contact No: ")
    emergency_contact_no = StringField("Emergency Contact No: ")
    emergency_contact_address = StringField("Emergency Contact Address: ")
    emergency_contact_relationship = StringField("Emergency Contact Relationship: ")
    maritalstatus = SelectField("Marital Status: ", choices=[("Married", "Married"), ("Single", "Single"), ("Divorced", "Divorced"), ("Widowed", "Widowed")], default="")
    image_name = FileField("Patient's Image: ") #not even used


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET','POST'])
def render_login():
    form = PatientLogin(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        #https://firebase.google.com/docs/database/admin/retrieve-data
        if username[0].upper() == "P":
            validate = root.child('Patient').order_by_child("username").equal_to(username).get()

            for key, val in validate.items():
                if username == val['username'] and password == val['password']:
                    session['logged_in'] = True
                    session['db_id'] = key
                    session['user_id'] = username
                    logindate = datetime.datetime.now()
                    session["login_date"] = logindate.strftime("%d%m%y")

                    pat_url = root.child('patient_info').order_by_child("newthing").equal_to(session["user_id"]).get()
                    for pat, url in pat_url.items():
                        if session["user_id"] == url['newthing']:
                            session["patient_url"] = pat
                    return redirect(url_for('render_nurse'))
                else:
                    error = "Invalid Login"
                    flash(error, "danger")

        elif username[0].upper() == 'S':
            validate = root.child('Staff').order_by_child("username").equal_to(username).get()

            for key, val in validate.items():
                if username == val['username'] and password == val['password']:
                    session['logged_in_staff'] = True
                    session['db_id'] = key
                    session['user_id'] = username

                    return redirect(url_for('render_trainee_notes'))
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
            password = "S" + str(random.randint(10000, 99999))
            name = admin_form.name.data
            nric = admin_form.nric.data
            dob = admin_form.dob.data
            email = admin_form.email.data
            address = admin_form.address.data
            gender = admin_form.gender.data
            occupation = admin_form.occupation.data
            income = admin_form.income.data
            bloodtype = admin_form.bloodtype.data
            race = admin_form.race.data
            phone_no = admin_form.phone_no.data
            emergency_contact_no = admin_form.emergency_contact_no.data
            emergency_contact_address = admin_form.emergency_contact_address.data
            emergency_contact_relationship = admin_form.emergency_contact_relationship.data
            maritalstatus = admin_form.maritalstatus.data

            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image_name = file.filename

            new_staff = Admin_Work(name, nric, dob, email, address, gender, occupation, income,
                                     bloodtype, race, phone_no,
                                     emergency_contact_no, emergency_contact_address, emergency_contact_relationship,
                                     maritalstatus, username, password, image_name)

            new_staff_db = root.child('Staff')
            new_staff_db.push({
                'name': new_staff.get_name(),
                'nric': new_staff.get_nric(),
                'dob': new_staff.get_dob(),
                'email': new_staff.get_email(),
                'address': new_staff.get_address(),
                'gender': new_staff.get_gender(),
                'occupation': new_staff.get_occupation(),
                'income': new_staff.get_income(),
                'bloodtype': new_staff.get_bloodtype(),
                'race': new_staff.get_race(),
                'phone_no': new_staff.get_phone_no(),
                'emergency_contact_no': new_staff.get_emergency_contact_no(),
                'emergency_contact_address': new_staff.get_emergency_contact_address(),
                'emergency_contact_relationship': new_staff.get_emergency_contact_relationship(),
                'maritalstatus': new_staff.get_maritalstatus(),
                'username': new_staff.get_username(),
                'password': new_staff.get_password(),
                'image_name': new_staff.get_image_name(),
            })
            hospital_admin = root.child("Staff").get()
            for data in hospital_admin:
                datainfo = hospital_admin[data]
                setid = Admin_Work(datainfo["name"], datainfo["nric"], datainfo["dob"], datainfo["email"],
                                   datainfo["address"], datainfo["gender"], datainfo["occupation"],
                                   datainfo["income"], datainfo["bloodtype"], datainfo["race"], datainfo["phone_no"],
                                   datainfo["emergency_contact_no"], datainfo["emergency_contact_address"],
                                   datainfo["emergency_contact_relationship"], datainfo["maritalstatus"],
                                   datainfo["username"], datainfo["password"], datainfo["image_name"])
                setid.set_patient_id(data)
                print(data)
            flash(new_staff.get_name() +' added!(Staff)'+ ' User = '+username + ' Password = '+password, 'success')
            # client.api.account.messages.create(
            #     to="+6592211065",
            #     from_="+18636927542",
            #     body="Your user is: {} and password: {}".format(username,password))

        elif admin_form.type.data == 'Patient':
            username = 'P' + str(random.randint(10000, 99999))
            password = "P" + str(random.randint(10000, 99999))
            name = admin_form.name.data
            nric = admin_form.nric.data
            dob = admin_form.dob.data
            email = admin_form.email.data
            address = admin_form.address.data
            gender = admin_form.gender.data
            occupation = admin_form.occupation.data
            income = admin_form.income.data
            bloodtype = admin_form.bloodtype.data
            race = admin_form.race.data
            phone_no = admin_form.phone_no.data
            emergency_contact_no = admin_form.emergency_contact_no.data
            emergency_contact_address = admin_form.emergency_contact_address.data
            emergency_contact_relationship = admin_form.emergency_contact_relationship.data
            maritalstatus = admin_form.maritalstatus.data

            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image_name = file.filename

            new_patient = Admin_Work(name, nric, dob, email, address, gender, occupation, income,
                                   bloodtype, race, phone_no,
                                   emergency_contact_no, emergency_contact_address, emergency_contact_relationship,
                                   maritalstatus, username, password, image_name)

            new_patient_db = root.child('Patient')
            new_patient_db.push({
                'name': new_patient.get_name(),
                'nric': new_patient.get_nric(),
                'dob': new_patient.get_dob(),
                'email': new_patient.get_email(),
                'address': new_patient.get_address(),
                'gender': new_patient.get_gender(),
                'occupation': new_patient.get_occupation(),
                'income': new_patient.get_income(),
                'bloodtype': new_patient.get_bloodtype(),
                'race': new_patient.get_race(),
                'phone_no': new_patient.get_phone_no(),
                'emergency_contact_no': new_patient.get_emergency_contact_no(),
                'emergency_contact_address': new_patient.get_emergency_contact_address(),
                'emergency_contact_relationship': new_patient.get_emergency_contact_relationship(),
                'maritalstatus': new_patient.get_maritalstatus(),
                'username': new_patient.get_username(),
                'password': new_patient.get_password(),
                "image_name": new_patient.get_image_name()
            })
            hospital_admin = root.child("Patient").get()
            for data in hospital_admin:
                datainfo = hospital_admin[data]
                setid = Admin_Work(datainfo["name"], datainfo["nric"], datainfo["dob"], datainfo["email"], datainfo["address"], datainfo["gender"], datainfo["occupation"],
                                   datainfo["income"], datainfo["bloodtype"], datainfo["race"], datainfo["phone_no"], datainfo["emergency_contact_no"], datainfo["emergency_contact_address"],
                                   datainfo["emergency_contact_relationship"], datainfo["maritalstatus"], datainfo["username"], datainfo["password"], datainfo["image_name"])
                setid.set_patient_id(data)
                print(data)
            flash(new_patient.get_name() +' added!(Patient)'+ ' User = '+username + ' Password = '+password, 'success')
            # client.api.account.messages.create(
            #     to="+6592211065",
            #     from_="+18636927542",
            #     body="Your user is: {} and password: {}".format(username,password))

    return render_template('Admin.html',form=admin_form)

@app.route("/med_time/<patientid>/<medid>", methods=["POST"])
def med_time(patientid, medid):
    med_db2 = root.child("Medicine/" + patientid + "/" + medid).get()
    medicine3 = Medicine(med_db2["medName"], med_db2["medDesc"], med_db2["medDosage"], med_db2["sideEffect"], med_db2["medTime"], med_db2["medInterval"])
    medicine3.set_med_id(medid)
    name = medicine3.get_medName()
    desc = medicine3.get_medDesc()
    dosage = medicine3.get_medDosage()
    side = medicine3.get_sideEffect()
    medInterval = medicine3.get_medInterval()
    x = int(medInterval)
    newthing = session["user_id"]
    duration = datetime.datetime.now() + timedelta(hours=x)
    # def startTime():
    #     session[patientid + "_" + medid] = True
    # def endTime():
    #     session.pop(patientid + "_" + medid, None)

    def countDown():
        range = duration - datetime.datetime.now()
        secondsDiff = range.total_seconds()
        try:
            med_db3 = root.child("Medicine/" + patientid + "/" + medid).get()
            if len(med_db3) > 0:
                root.child("Medicine/" + patientid + "/" + medid).set({
                    "medName": name,
                    "medDesc": desc,
                    "medDosage": dosage,
                    "sideEffect": side,
                    "newthing": newthing,
                    "medTime":("%02.f" % secondsDiff),
                    "medInterval": medInterval
                })
                countDownTime = Timer(1, countDown)
                if secondsDiff > 0.5:
                    countDownTime.start() #every 1sec then update the firebase (should increase time to not flood db)
                else:
                    print("End")
        except TypeError:
            print("Med Field Deleted")
    countDown()

    return redirect(url_for("render_patient_info", id=session["patient_url"]))

@app.route('/patient_info/<string:id>', methods=["GET", "POST"])
def render_patient_info(id):
    url = "patient_info/" + id
    eachpat = root.child(url).get()
    patients = Edit_Patient(eachpat["name"], eachpat["illness"], eachpat["patientdesc"], eachpat["time"], eachpat["image_name"], eachpat["ward"])
    patients.set_patient_id(id)

    try:
        history = root.child('archived_patient_info').order_by_child("newthing").equal_to(session["user_id"]).get()
        medicine = root.child("Medicine/" + session["user_id"]).get()
        list = []
        medList = []
        for data in history:
            info = history[data]
            infos = Edit_Patient(info["name"], info["illness"], info["patientdesc"], info["time"], info["image_name"], info["ward"])
            infos.set_patient_id(data)
            list.append(infos)
        for med in medicine:
            med1 = medicine[med]
            med2 = Medicine(med1["medName"], med1["medDesc"], med1["medDosage"], med1["sideEffect"], med1["medTime"], med1["medInterval"])
            med2.set_med_id(med)
            medList.append(med2)
    except TypeError:
        pass
    return render_template('patient_info.html', eachpat=patients, history=list, medicine=medList) # patient_infos=patientInfo)

# New patient when logging in!
@app.route('/patient_info/')
def point_p():
    return render_template("point_p.html")

# newthing = patient id
@app.route('/patient_info_editor/', methods=["GET", "POST"])
def render_patient_info_editor():
    form = Patient_Info(request.form)
    medform = Patient_Medicine(request.form)

    if request.method == "POST" and medform.submitMed.data and medform.validate():
        if medform.medName.data == "select":
            flash('Please select a medicine', 'danger')
            return redirect(request.url)
        medName = medform.medName.data
        medDesc = medform.medDesc.data
        medDosage = medform.medDosage.data
        sideEffect = medform.sideEffect.data
        medTime = ""
        medInterval = medform.medInterval.data
        medicine = Medicine(medName, medDesc, medDosage, sideEffect, medTime, medInterval)
        med_db = root.child("Medicine/" + session["user_id"])
        med_db.push({
            "medName": medicine.get_medName(),
            "medDesc": medicine.get_medDesc(),
            "medDosage": medicine.get_medDosage(),
            "sideEffect": medicine.get_sideEffect(),
            "medTime": 0,
            "medInterval": medicine.get_medInterval(),
            "newthing": session["user_id"] #just in case
        })

    #All the code below could just use the one above lol (not really)
    if request.method == "POST" and form.submitInfo.data and form.validate():
        if form.ward.data == "select":
            flash('Please select the patient\'s wards', 'danger')
            return redirect(request.url)
        name = form.name.data #redundant
        illness = form.illness.data
        patientdesc = form.patientdesc.data
        time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ward = form.ward.data
        pat_db = root.child("Patient").order_by_child("username").equal_to(session["user_id"]).get()
        image_name = ""
        print(session["user_id"])
        for key, val in pat_db.items():
            if session["user_id"] == val['username']:
                pat_name = val["name"]
                img_name = val["image_name"]
            else:
                pat_name = name
        pat = Edit_Patient(name, illness, patientdesc, time, image_name, ward)

        #find and check if there any patient with the same "newthing"
        pat_db2 = root.child('patient_info').order_by_child("newthing").equal_to(session["user_id"]).get()
        if len(pat_db2) > 0:
            for key2, val2 in pat_db2.items():
                if session["user_id"] == val2['newthing']:
                    # if "newthing" exists, set the "session url" to the "-L0spKVkqG0t9WeLaHvq"
                    session["patient_url"] = key2
                    # update the patient_info folder
                    pat_db3 = root.child("patient_info/" + session["patient_url"])
                    pat_db3.set({
                        "name": pat_name,
                        "illness": pat.get_illness(),
                        "patientdesc": pat.get_patientdesc(),
                        "newthing": session["user_id"],
                        "time": "(Date Modified) " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "image_name": img_name,
                        "ward": pat.get_ward()
                    })
            #get the updated version again......
            pat_db4 = root.child("patient_info").order_by_child("newthing").equal_to(session["user_id"]).get()
            for key3, val3 in pat_db4.items():
                if session["user_id"] == val3['newthing']:
                    # keep the recently updated record into another folder
                    arc_pat_db = root.child("archived_patient_info")
                    arc_name = val3["name"]
                    arc_illness = val3["illness"]
                    arc_patientdesc = val3["patientdesc"]
                    arc_time = val3["time"]
                    arc_img_name = val3["image_name"]
                    arc_ward = val3["ward"]

                    arc_pat_db.push({
                        "name": arc_name,
                        "illness": arc_illness,
                        "patientdesc": arc_patientdesc,
                        "newthing": session["user_id"],
                        "time": arc_time,
                        "image_name": arc_img_name,
                        "ward": arc_ward
                    })
            print("Patient Info Updated!")
        else:
            #if new patient, add it in
            pat_db5 = root.child('patient_info')
            pat_db5.push({
                "name": pat_name,
                "illness": pat.get_illness(),
                "patientdesc": pat.get_patientdesc(),
                "newthing": session["user_id"],
                "time": "(Date Added) " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "image_name": img_name,
                "ward": pat.get_ward()
                })
            #add the new patient record into another folder
            pat_db6 = root.child('archived_patient_info')
            pat_db6.push({
                "name": pat_name,
                "illness": pat.get_illness(),
                "patientdesc": pat.get_patientdesc(),
                "newthing": session["user_id"],
                "time": "(Date Added) " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "image_name": img_name,
                "ward": pat.get_ward()
            })

            print("New Patient Added!")

        # pat_db2 = root.child('patient_info').order_by_child('name').equal_to(pat_name).get()
        # for key2, val2, in enumerate(pat_db2):
        #     if key2 == len(pat_db2)-1:
        #         print(key2)
        #         print("key 2 ^")
        #         print(val2)
        #         print("val 2 ^")
        #         id = val2

        #loop through the firebase again to check for the UPDATED "newthing"
        pat_db7 = root.child('patient_info').order_by_child("newthing").equal_to(session["user_id"]).get()
        for key4, val4 in pat_db7.items():
            if session["user_id"] == val4['newthing']:
                #assign the id/url as the "-L0spKVkqG0t9WeLaHvq" because the previous "session["patient_url"]" does not exist for the newly added patient
                session["patient_url"] = key4

        flash("Patient Information Successfully Updated.", "success")
        return redirect(url_for("render_patient_info", id=session["patient_url"]))
    else:
        pat_db8 = root.child("Patient").order_by_child("username").equal_to(session["user_id"]).get()
        for key5, val5 in pat_db8.items():
            if session["user_id"] == val5['username']:
                session["pat_admin_info"] = key5
                # pat_name = val["name"]
        # form.name.data = pat_name
        datainfo = root.child("Patient/" + session["pat_admin_info"]).get()
        data = Admin_Work(datainfo["name"], datainfo["nric"], datainfo["dob"], datainfo["email"], datainfo["address"],
                           datainfo["gender"], datainfo["occupation"],
                           datainfo["income"], datainfo["bloodtype"], datainfo["race"], datainfo["phone_no"],
                           datainfo["emergency_contact_no"], datainfo["emergency_contact_address"],
                           datainfo["emergency_contact_relationship"], datainfo["maritalstatus"], datainfo["username"],
                           datainfo["password"], datainfo["image_name"])
        pat_db9 = root.child('patient_info').order_by_child("newthing").equal_to(session["user_id"]).get()
        if len(pat_db9) > 0:
            formpat = root.child("patient_info/" + session["patient_url"]).get()
            pat_form = Edit_Patient(formpat["name"], formpat["illness"], formpat["patientdesc"], formpat["time"], formpat["image_name"], formpat["ward"])

            form.illness.data = pat_form.get_illness()
            form.patientdesc.data = pat_form.get_patientdesc()
            form.ward.data = pat_form.get_ward()
        try:
            med_db1 = root.child("Medicine/" + session["user_id"]).get()
            medList2 = []
            if len(med_db1) > 0:
                for med in med_db1:
                    med3 = med_db1[med]
                    med4 = Medicine(med3["medName"], med3["medDesc"], med3["medDosage"], med3["sideEffect"], med3["medTime"], med3["medInterval"])
                    med4.set_med_id(med)
                    medList2.append(med4)
        except:
            pass

    return render_template('patient_info_editor.html', form=form, data=data, medform=medform, medicine2=medList2)

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
#         patients.set_patient_id(id)
#         form.name.data = patients.get_name()
#         form.illness.data = patients.get_illness()
#         form.patientdesc.data = patients.get_patientdesc()
#         form.medicinedesc.data = patients.get_medicinedesc()
#         form.med1.data = patients.get_med1()
#         form.med2.data = patients.get_med2()
#         form.med3.data = patients.get_med3()
#
#     return render_template("patient_edit.html", form=form)
#
#
@app.route("/delete_med/<medicine>/<string:id>", methods=["POST"])
def delete_med(medicine, id):
    med_db = root.child("Medicine/" + medicine + "/" + id)
    med_db.delete()
    med_db.delete()
    med_db.delete()
    med_db.delete()
    med_db.delete()
    #MULTIPLE DELETE IS INTENDED
    #REASON BEING: COUNTDOWN() MIGHT SET A NEW 1 ALONG WHEN OLD ONE IS DELETED
    #2 IS ENOUGH TO DELETE THE OTHER ONE THAT WAS SETTED
    #BUT I HARDSTUCKED ON THAT LOGICAL ERROR SO I ADDED IN MORE
    flash("Medicine has been removed", "success")

    return redirect(url_for("render_patient_info_editor"))

@app.route('/staff_profile/<string:id>', methods=['POST', 'GET'])
def render_staff_profile(id):

    url = "Staff/" + id
    print(url)
    eachstaff = root.child('Staff').order_by_child('username').equal_to(id).get()
    list = []

    # print(eachstaff)

    for k, v in eachstaff.items():
        print(k, v)
        # print(v['username'])
        # print(v['password'])
        staff = Staff(v["name"], v["nric"], v["gender"], v["dob"], v["email"], v["phone_no"], v["address"], v['username'], v['password'], v['image_name'])
        # staff.set_st(v)
        # print(staff.get_st())
        # list.append(staff)

    # staff.set_staff_profile(id)
    def alert():            #function to update database Staff
        form = StaffProfile(request.form)
        if request.method == 'POST' and form.validate():
            name = form.name.data  # redundant
            nric = form.nric.data
            gender = form.gender.data
            dob = form.dob.data
            email = form.email.data
            phone_no = form.phone_no.data
            username = form.username.data
            address = form.address.data
            image_name = ""

            okay = root.child("Staff").order_by_child("username").equal_to(session["user_id"])
            okay.set({
                "name": name,
                "nric": nric,
                "gender": gender,
                "dob": dob,
                "email": email,
                "phone_no": phone_no,
                "username": username,
                "address": address,
                "image_name": image_name
            })

    alert1 = alert()
    list.append(alert1)

    return render_template('staff_profile.html', eachstaff=staff, updatealert=alert1)

'''
            print(session["user_id"])
            for key, val in okay.items():
            if session["user_id"] == val['username']:
                staff_name = val["name"]
                img_name = val["image_name"]
            else:
                staff_name = name
                st = Staff(name, nric, gender, dob, email, phone_no, address, username, image_name)
    else:
        ok = root.child("Staff").order_by_child("username").equal_to(session["user_id"]).get()
        for key, val in ok.items():
            if session["user_id"] == val['username']:
                session["staff_admin_info"] = key
          # pat_name = val["name"]
         # form.name.data = pat_name
        datainfo = root.child("Staff/" + session["staff_admin_info"]).get()
        data = Admin_Work(datainfo["name"], datainfo["nric"], datainfo["dob"], datainfo["email"], datainfo["address"],
                          datainfo["gender"], datainfo["occupation"],
                          datainfo["income"], datainfo["bloodtype"], datainfo["race"], datainfo["phone_no"],
                          datainfo["emergency_contact_no"], datainfo["emergency_contact_address"],
                          datainfo["emergency_contact_relationship"], datainfo["maritalstatus"], datainfo["username"],
                          datainfo["password"], datainfo["image_name"])

        formstaff = root.child("staff_ino/" + session["staff_url"]).get()
        staff_form = Staff(formstaff["name"], formstaff["illness"], formstaff["patientdesc"], formstaff["medicinedesc"],
                                    formstaff["med1"], formstaff["med2"], formstaff["med3"],
                                    formstaff["time"], formstaff["image_name"])

        form.gender.data = staff_form.get_gender()
        form.nric.data = staff_form.get_nric()
        form.dob.data = staff_form.get_dob()
        form.username.data = staff_form.get_username()
        form.phone_no.data = staff_form.get_phone_no()
        form.email.data = staff_form.get_email()
        form.address.data = staff_form.get_address()
        form.username.data = staff_form.get_username()'''



@app.route('/billing')
def render_billing():
    pat_info = root.child('patient_info').get()

    for key, val in pat_info.items():
        time_list = val["time"].split()
        date_list = time_list[2].split("/")
        date_in = date(int(date_list[2]), int(date_list[1]), int(date_list[0]))
        days_full = date.today() - date_in
        days_string = str(days_full)
        days_list = days_string.split()
        days = int(days_list[0])

        ward = val["ward"]
        if ward == "A":
            cost = 466.52
        elif ward == "B1":
            cost = 251.45
        elif ward == "B2":
            cost = 75
        elif ward == "C":
            cost = 35

        medicine1 = val["med1"]
        medicine2 = val["med2"]
        medicine3 = val["med3"]

    service_fee = 50
    operation_fee = 5000

    return render_template('billing.html', ward=ward, ward_cost=cost, stay_in_days=days, med1=medicine1, med2=medicine2, med3=medicine3, service=service_fee, operation=operation_fee)


@app.route('/nursecallpage/',methods=['GET','POST'])
def render_nurse():
        # DAYS
        # FOOD ORDER
        Food_Order = root.child('Food_Order').get()
        Nurses_calling = root.child('Nurse Call').get()
        id_list = []
        list = []
        nurse_list = []
        if Food_Order is not None:
            for i in Food_Order:
                eachorder = Food_Order[i]
                order = FoodOrder(eachorder['foodname'],eachorder['day'],eachorder['user_id'],eachorder['indian'],eachorder['malay'],eachorder['chinese'],eachorder['western'],eachorder['international'],eachorder['meal'])
                # order.set_foodid(food_id)
                list.append(order)
                id_list.append(i)
        else:
            pass


        # NURSE CALL
        nurse_form = NurseCallForm(request.form)
        if request.method == 'POST' and nurse_form.validate():
            newcall = NurseCall(nurse_form.problem.data,session['user_id'])
            newcall_db = root.child('Nurse Call')
            newcall_db.push ({
               'symptom': newcall.get_reason(),
               'id': newcall.get_user_id()
             })

            flash('A nurse will attend to you shortly.', 'success')
            return redirect(url_for('render_nurse'))

        for n in Nurses_calling:
            eachnurse = Nurses_calling[n]
            call = NurseCall(eachnurse['symptom'],eachnurse['id'])
            nurse_list.append(call)

        # FOOD ORDER
        # client.api.account.messages.create(
        #     to="+12316851234",
        #     from_="+15555555555",
        #     body="Hello there!")
        return render_template('nursecallpage.html',orders = list,nurse = nurse_form,id_list=id_list,nurse_list=nurse_list)



# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm(request.form)
#     print(request.method)
#     if request.method == 'POST' and form.validate():
#         username = form.username.data
#         password = form.password.data
#         validate = root.child('Staff').order_by_child("username").equal_to(username).get()
#
#         for key, val in validate.items():
#             if username == val['username'] and password == val['password']:
#                 session['logged_in_staff'] = True
#                 return redirect(url_for('render_patient_info', id=session["patient_url"]))
#             else:
#                 error = "Invalid Login"
#                 flash(error, "danger")
#form=form)
#     return render_template('StaffLogin.html',


@app.route('/logout/')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('render_login'))


# @app.route('/staff_logout/')
# def logout_staff():
#     session.pop("logged_in_staff", None) #None is pass in as the "default" value (else it will return its "default" value)
#     flash('You are now logged out', 'success')
#     return redirect(url_for('render_nurse'))


@app.route('/menu/', methods = ['GET','POST'])
def render_menu():
    form = FoodOrderForm(request.form)

    # getting the number of days
    now_unformatted = datetime.datetime.now()
    now = now_unformatted.strftime("%d%m%y")
    days = int(now[0:2]) - int(session["login_date"][0:2])
    days = days + 1

    # getting timing for breakfast, lunch or dinner
    current_time = datetime.datetime.now().strftime('%H%M%S')
    hours = current_time[0:2]
    hours = int(hours)

    # check what meal it is
    meal = "extra order"
    if 11 >= hours >= 7:
        meal = "breakfast"
    elif 14 > hours > 11:
        meal = "lunch"
    elif 22 > hours > 17:
        meal = "dinner"

    # neworder_db = root.child('Food_Order').order_by_child('user_id').equal_to(session['user_id']).get()
    # for key, val in neworder_db.items():
    #     print(key)
    #     print(val)
    #     print(val['day'])

    if request.method == 'POST' and form.validate():
        # testing
        neworder_db = root.child('Food_Order').order_by_child('user_id').equal_to(session['user_id']).get()
        nigger = root.child('Food_Order').get()
        # if nigga is empty
        if nigger is None:
            print('push')
            # new class + push into db
            neworder = FoodOrder(form.foodname.data, days, session["user_id"], form.indian.data, form.malay.data,
                                 form.chinese.data, form.western.data, form.international.data, meal)
            neworder_db = root.child('Food_Order')
            neworder_db.push({
                'day': neworder.get_days(),
                'user_id': neworder.get_patient_id(),
                'foodname': neworder.get_foodname(),
                'indian': neworder.get_indian(),
                'malay': neworder.get_malay(),
                'chinese': neworder.get_chinese(),
                'western': neworder.get_western(),
                'international': neworder.get_international(),
                'meal': neworder.get_meal(),
            })
            flash('Success! Your order has been received!', 'success')
            return redirect(url_for("render_nurse"))

        for key, val in neworder_db.items():
            print(key)
            print(val)
            if val['day'] == days:
                if val['meal'] == meal:
                    # update
                    print('update')
                    neworder = FoodOrder(form.foodname.data, days, session["user_id"], form.indian.data, form.malay.data, form.chinese.data, form.western.data, form.international.data,meal)
                    neworder_db = root.child('Food_Order/'+ key)
                    neworder_db.set({
                        'day': neworder.get_days(),
                        'user_id': neworder.get_patient_id(),
                        'foodname': neworder.get_foodname(),
                        'indian': neworder.get_indian(),
                        'malay': neworder.get_malay(),
                        'chinese': neworder.get_chinese(),
                        'western': neworder.get_western(),
                        'international': neworder.get_international(),
                        'meal': neworder.get_meal(),
                    })
                    flash('Successfully updated! Your order has been updated! ', 'success')
                    return redirect(url_for("render_nurse"))

            else:
                print('push')
                # new class + push into db
                neworder = FoodOrder(form.foodname.data, days,session["user_id"],form.indian.data,form.malay.data,form.chinese.data,form.western.data,form.international.data,meal)
                neworder_db = root.child('Food_Order')
                neworder_db.push ({
                'day': neworder.get_days(),
                'user_id':neworder.get_patient_id(),
                'foodname': neworder.get_foodname(),
                'indian':neworder.get_indian(),
                'malay':neworder.get_malay(),
                'chinese':neworder.get_chinese(),
                'western':neworder.get_western(),
                'international':neworder.get_international(),
                'meal':neworder.get_meal(),
                })
                flash('Success! Your order has been received!','success')
                return redirect(url_for("render_nurse"))

            return redirect(url_for("render_nurse"))

    elif request.method == 'GET':
        return render_template('menu.html', form=form, days=days, current_time=current_time,hours = hours)

    return render_template('menu.html', form=form, days =days, current_time=current_time, hours = hours)

@app.route('/trainee_notes/')
def render_trainee_notes():
    drone = Scaledrone('SNazg8KrKdwSphWf', 'fCw1xxKBLoYBFZuif4vRKgK3ibIdH6mk')
    room = 'observable-room'
    message = {'foo': 'bar'}
    response = drone.publish(room, json.dumps(message))
    print(response)
    return render_template('trainee_notes.html')

@app.route('/delete_order/<string:id>', methods=['POST'])
def delete_order(id):
    order_db = root.child('Food_Order/' + id)
    order_db.delete()
    flash('Order Deleted', 'success')

    return redirect(url_for('render_nurse'))


if __name__ == '__main__':
    # app.secret_key = 'toUUtBRQZqXHdVPLXDQH0FbIRs3heozyVGZPigXJ'
    app.debug = True
    #PLEASE KEEP IT AT PORT 80
    app.run(port=80)
    #app.run(host = '0.0.0.0', port = 5000) not sure if this is how you change it
