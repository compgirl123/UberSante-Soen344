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

@blueprint.route('/doctorschedule')
def doctorschedule():
    return render_template('doctorpages/doctorschedule.html')

@blueprint.route('/findnurse')
def findnurse():
    return render_template('nursepages/findnurse.html')

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
