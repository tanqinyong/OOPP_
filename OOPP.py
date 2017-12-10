from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators
# e.g. from Patient import Patient
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
    pass # the description & form (input text button shit like that) also ya the urgency and description thing try to be specific (headache heartattack)


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


@app.route('/menu/')
def render_menu():
    return render_template('menu.html')




class Patient_Info(Form):
    name = StringField("Name", [validators.Length(min=1, max=50), validators.DataRequired()])
    illness = StringField("Illness", [validators.Length(min=1, max=100), validators.DataRequired()])
    patientdesc = TextAreaField("Patient Description", [validators.DataRequired()])
    medicinedesc = TextAreaField("Medicine Description", [validators.DataRequired()])
    med1 = StringField("Medicine 1", [validators.Length(min=1, max=30), validators.DataRequired()])
    med2 = StringField("Medicine 2", [validators.Length(min=1, max=30), validators.DataRequired()])
    med3 = StringField("Medicine 3", [validators.Length(min=1, max=30), validators.DataRequired()])

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

if __name__ == '__main__':
    app.secret_key = 'icare1729'
    app.debug = True
    app.run()
    #app.run(host = '0.0.0.0', port = 5000) not sure if this is how you change it


