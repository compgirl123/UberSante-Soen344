from flask import render_template, Blueprint, request, session, redirect, flash
from app.forms import *
from app.controllers.nursecontroller import *

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
    #_nametest = request.form.get("name", False)
    # stores the name that was entered to the next page
    _password = request.form['password'];
    # stores the password that was entered to the next page
    _obj = Nursecontroller()
    _obj2 = _obj.nurse_table(_name)

    POST_USERNAME = str(request.form['name'])
    POST_PASSWORD = str(request.form['password'])

    print(POST_USERNAME)

    #return POST_PASSWORD

    Session = sessionmaker(bind=engine)
    s= Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User._password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    #return nurse_login()

    return POST_USERNAME
    #return _name;
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

@blueprint.route('/loginnurse', methods=['POST'])
def login_nurse():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    return POST_PASSWORD

    '''Session = sessionmaker(bind=engine)
    s= Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User._password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return nurse_login()'''

@blueprint.route('/patient_login')
def patient_login():
    form = PatientLoginForm(request.form)
    return render_template('forms/patient_login.html', form=form)

@blueprint.route('/logout')
def logout():
    session['logged_in']= False
    return render_template('forms/login.html', form=form)

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
