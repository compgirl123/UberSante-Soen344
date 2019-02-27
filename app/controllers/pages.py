from flask import render_template, Blueprint, request
from app.forms import *

blueprint = Blueprint('pages', __name__)


################
#### routes ####
################


@blueprint.route('/')
def home():
    return render_template('pages/placeholder.home.html')

@blueprint.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@blueprint.route('/findnurse', methods=['GET', 'POST'])
def findnurse():
    #_name = request.form['form-nurselogin'];
    return render_template('nursepages/findnurse.html')

@blueprint.route('/nursedashboard', methods=['GET', 'POST'])
def nursedashboard():
    _name = request.form['name'];
    # stores the name that was entered to the next page
    _password = request.form['password'];
    # stores the password that was entered to the next page
    return _name;
    #return _password;
    # return 0;
    # placeholder to test function in order to not make it have an error

@blueprint.route('/doctorlogin')
def doctor_login():
    form = LoginForm(request.form)
    return render_template('forms/doctor_login.html', form=form)

@blueprint.route('/nurselogin')
def nurse_login():
    form = LoginForm(request.form)
    return render_template('forms/nurse_login.html', form=form)

@blueprint.route('/patient_login')
def patient_login():
    form = PatientLoginForm(request.form)
    return render_template('forms/patient_login.html', form=form)

@blueprint.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@blueprint.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@blueprint.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@blueprint.route('/patient_register')
def patient_register():
    form = PatientRegisterForm(request.form)
    return render_template('forms/patient_register.html', form=form)


@blueprint.route('/register_doctor')
def register_doctor():
    form = RegisterDoctorForm(request.form)
    return render_template('forms/register_doctor.html', form=form)
