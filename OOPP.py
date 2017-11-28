from flask import Flask
from flask import render_template

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


if __name__ == '__main__':
    app.run()


