from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators
# e.g. from Patient import Patient
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('cred/oopp-4e3a2-firebase-adminsdk-njuhh-69bc3a7f98.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopp-4e3a2.firebaseio.com/'
})

root = db.reference()

app = Flask(__name__)


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

if __name__ == '__main__':
    app.secret_key = 'icare1729'
    app.run()


