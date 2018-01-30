# Flask, WTForms and cool shit
from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, SubmitField, SelectMultipleField, validators, widgets, PasswordField, DateField, FileField, IntegerField
from werkzeug.utils import secure_filename
import random, datetime, os
now = datetime.datetime.now()
print(now.strftime("%d/%m/%Y %H:%M"))
# Classes and shit
from Food_Order import FoodOrder
# from Nurse_call import NurseCall
# from Patient_Info import Edit_Patient
from Hospital import *
# from Admin import Staff, Patient
from trainee_notes import comment

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
    problem = SelectMultipleField('Symptoms', choices=[("Heart","Heart"),("Extremities","Extremities"),("Headache","Headache"),("Stomach","Stomach"),("Nausea","Nausea"),("Breathing","Breathing")],option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Enter')


# Menu Page
class FoodOrderForm(Form):
    foodname = RadioField('Food Choices:', choices = [('Indian Cuisine','indian'),('Chinese Cuisine','chinese'),('Western Cuisine','western'),('International Cuisine','international')],default='international')
    # patientname = StringField('Name:',[validators.DataRequired(),validators.Length(min=1, max=30)])
    # qty = SelectField('Qty', choices=[('1', '1'), ('2', '2'),('3','3'),('4','4'),('5','5')], default='')
    submit = SubmitField('Enter')


# Trainee page
class TraineeForm(Form):
    name = StringField('Name:',[validators.DataRequired(),validators.Length(min=1, max=30)])
    comment = TextAreaField('Comment:')
    submit = SubmitField('Enter')


# Patient info page
class Patient_Medicine(Form):
    medName = StringField("Medicine Name")
    medDesc = TextAreaField("Medicine Description", [validators.DataRequired()])
    medDosage = IntegerField("Dosage")
    sideEffect = StringField("Side Effect")
    submitMed = SubmitField("submit")

class Patient_Info(Form):
    name = StringField("Name")
    illness = StringField("Illness", [validators.Length(min=1, max=100), validators.DataRequired()])
    patientdesc = TextAreaField("Illness Description", [validators.DataRequired()])
    ward = SelectField("Ward: ", choices=[("C","C"),("B2", "B2"), ("B1","B1"), ("A", "A")], default="")
    submitInfo = SubmitField("submit")
    #https://wtforms.readthedocs.io/en/latest/fields.html#wtforms.fields.FieldList


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
                'image_name': new_staff.get_image_name()
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

    return render_template('Admin.html',form=admin_form)


@app.route('/patient_info/<string:id>', methods=["GET"])
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
            med2 = Medicine(med1["medName"], med1["medDesc"], med1["medDosage"], med1["sideEffect"])
            med2.set_med_id(med)
            medList.append(med2)
    except TypeError:
        flash("No Records Found!", "danger")
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
        medName = medform.medName.data
        medDesc = medform.medDesc.data
        medDosage = medform.medDosage.data
        sideEffect = medform.sideEffect.data
        medicine = Medicine(medName, medDesc, medDosage, sideEffect)
        med_db = root.child("Medicine/" + session["user_id"])
        med_db.push({
            "medName": medicine.get_medName(),
            "medDesc": medicine.get_medDesc(),
            "medDosage": medicine.get_medDosage(),
            "sideEffect": medicine.get_sideEffect(),
            "newthing": session["user_id"] #just in case
        })

    #All the code below could just use the one above lol (not really)
    if request.method == "POST" and form.submitInfo.data and form.validate():
        name = form.name.data #redundant
        illness = form.illness.data
        patientdesc = form.patientdesc.data
        time = now.strftime("%d/%m/%Y %H:%M")
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
                        "time": "(Date Modified) " + now.strftime("%d/%m/%Y %H:%M"),
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
                "time": "(Date Added) " + now.strftime("%d/%m/%Y %H:%M"),
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
                "time": "(Date Added) " + now.strftime("%d/%m/%Y %H:%M"),
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

    return render_template('patient_info_editor.html', form=form, data=data, medform=medform)

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
# @app.route("/patient_delete/<string:id>", methods=["POST"])
# def delete_patient(id):
#     pat_db = root.child("patient_info/" + id)
#     pat_db.delete()
#     flash("Patient's information has been delete", "success")
#
#     return redirect(url_for("render_patient_info"))


@app.route('/trainee_notes/',methods=['POST',"GET"])
def render_trainee_notes():
    form = TraineeForm(request.form)
    if request.method == "POST" and form.validate():
        newcomment = comment(form.name.data,form.comment.data)
        newcomment_db = root.child('comment')
        newcomment_db.push ({
            'name': newcomment.get_name(),
            'comment':newcomment.get_comment()
        })
        flash('Comment posted successfully.', 'success')
    comments = root.child('comment').get()
    list = []
    for commentid in comments:

        eachcomment = comments[commentid]
        thatcomment = comment(eachcomment['name'],eachcomment['comment'])
        list.append(thatcomment)
    return render_template('trainee_notes.html', comments=list,form=form)


@app.route('/billing/')
def render_billing():
    return render_template('billing.html')


@app.route('/nursecallpage/',methods=['GET','POST'])
def render_nurse():
        # DAYS
        # FOOD ORDER
        Food_Order = root.child('Food_Order').get()
        list = []
        for food_id in Food_Order:
            eachorder = Food_Order[food_id]
            order = FoodOrder(eachorder['foodname'],eachorder['patientname'],eachorder['price'])
            order.set_foodid(food_id)
            list.append(order)

        # NURSE CALL
        nurse_form = NurseCallForm(request.form)
        if request.method == 'POST' and nurse_form.validate():
            newcall = NurseCall(nurse_form.problem.data,session['user_id'])
            newcall_db = root.child('Nurse Call')
            newcall_db.push ({
               'symptom': newcall.get_reason(),
               'id': newcall.get_user_id()
             })
            flash('A nurse will attend to you shortly.','success')
        return render_template('nursecallpage.html',orders = list,nurse = nurse_form)


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
    if request.method =='POST' and form.validate():
            neworder = FoodOrder(form.foodname.data,form.patientname.data,form.qty.data)
            neworder_db = root.child('Food_Order')
            neworder_db.push ({
            'patientname': neworder.get_patientname(),
            'foodname': neworder.get_foodname(),
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


if __name__ == '__main__':
    # app.secret_key = 'toUUtBRQZqXHdVPLXDQH0FbIRs3heozyVGZPigXJ'
    # app.debug = True
    app.run(port=80)
    #app.run(host = '0.0.0.0', port = 5000) not sure if this is how you change it
