from flask import render_template, Blueprint, request, make_response , redirect, url_for, flash
from app.forms import *
from app.controllers.nursecontroller import *
from app.controllers.doctorcontroller import *
from app.controllers.patientcontroller import *

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

'''
    Nurse Search Page routes
'''
@blueprint.route('/findnurse', methods=['GET', 'POST'])
def findnurse():
    user_id = request.cookies.get('nurseid')
    password = request.cookies.get('password')
    _obj = Nursecontroller()
    _nurse_full_name = _obj.nurse_full_name(user_id)
    print(_nurse_full_name)
    return render_template('nursepages/findnurse.html',name=user_id, nurse_full_name = _nurse_full_name)

@blueprint.route('/nursesearchctrlpermit', methods=['GET', 'POST'])
def nursesearchctrlpermit():

    if request.method == "POST":
        _permit = request.form['permit']  # stores the name that was entered to the next page
        print(_permit)
        _obj = Doctorcontroller()
        _doctor_found = _obj.find_doctor_by_permit_number(_permit)
        response = redirect(url_for("pages.doctorresults"))
        response.set_cookie('permit',_permit)
    return response

@blueprint.route('/nursesearchctrlhealthcare', methods=['GET', 'POST'])
def nursesearchctrlhealthcare():

    if request.method == "POST":
        _healthcare = request.form['healthcare']  # stores the name that was entered to the next page
        _obj = Patientcontroller()
        _patient_found = _obj.find_a_patient(_healthcare)
        response = redirect(url_for("pages.patientresults"))
        response.set_cookie('healthcare', _healthcare)
    return response

@blueprint.route('/doctorresults', methods=['GET', 'POST'])
def doctorresults():
    permit = request.cookies.get('permit')
    _obj = Doctorcontroller()
    _doctor_found = _obj.find_doctor_by_permit_number(permit)
    _results = 0
    if not _doctor_found:
        _results = 0
    else:
        _results = 1
    return render_template('resultpages/doctorresults.html',doctor_found = _doctor_found, results = _results)

@blueprint.route('/patientresults', methods=['GET', 'POST'])
def patientresults():
    healthcare = request.cookies.get('healthcare')
    _obj = Patientcontroller()
    _patient_found = _obj.find_a_patient(healthcare)
    _results = 0
    if not _patient_found:
        _results = 0
    else:
        _results = 1

    return render_template('resultpages/patientresults.html',patient_found = _patient_found, results = _results)

'''
    End of Nurse Search Page routes
'''

@blueprint.route('/nursedashboard', methods=['GET', 'POST'])
def nursedashboard():
    if request.method == "POST":
        _name = request.form['name'];# stores the name that was entered to the next page
        _password = request.form['password'];# stores the password that was entered to the next page
        _obj = Nursecontroller()
        _user = _obj.user(_name,_password)

        print(type(_user))
        print(type(_user) == type(None))
        _user2 = 1
        _obj2 = _obj.nurse_table(_name)
        if type(_user) == type(None):
            response = redirect(url_for("pages.error_nurse_login"))
        else:
            response = redirect(url_for("pages.findnurse"))

        response.set_cookie('nurseid', _name)
        response.set_cookie('password', _password)
        print(request)
        return response


@blueprint.route('/doctorschedule', methods=['GET', 'POST'])
def doctoraptbook():
    user_id = request.cookies.get('permitnumber')
    password = request.cookies.get('password')
    print(user_id)
    print(password)
    return render_template('doctorpages/doctorschedule.html', user = user_id )

#doctor login controller
@blueprint.route('/doctordashboard', methods=['GET', 'POST'])
def doctordashboard():
    if request.method == "POST":
        _name = request.form['name'];# stores the name that was entered to the next page
        _password = request.form['password'];# stores the password that was entered to the next page
        _obj = Doctorcontroller()
        _user = _obj.user(_name,_password)

        print(type(_user))
        print(type(_user) == type(None))
        _user2 = 1
        _obj2 = _obj.doctor_table(_name)
        if type(_user) == type(None):
            response = redirect(url_for("pages.error_doctor_login"))
        else:
            response = redirect(url_for("pages.doctorschedule"))

        response.set_cookie('permitnumber', _name)
        response.set_cookie('password', _password)
        print(request)
        return response

@blueprint.route('/doctorlogin')
def doctor_login():
    form = LoginForm(request.form)
    if 'permitnumber' in request.cookies:
        response = redirect(url_for("pages.doctorschedule"))
        return response
    else:
        return render_template('forms/doctor_login.html', form=form)

@blueprint.route('/nurselogin')
def nurse_login():
    form = LoginForm(request.form)
    if 'nurseid' in request.cookies:
        response = redirect(url_for("pages.findnurse"))
        return response
    else:
        return render_template('forms/nurse_login.html', form=form)

@blueprint.route('/nurse_doctor_logout')
def nurse_doctor_logout():
    response = redirect(url_for("pages.home"))
    response.set_cookie('nurseid', expires=0)
    response.set_cookie('permitnumber', expires=0)
    response.set_cookie('healthcard', expires=0)
    return response

@blueprint.route('/errornurselogin')
def error_nurse_login():
    form = LoginForm(request.form)
    return render_template('nursepages/error_nurse_login.html', form=form)

@blueprint.route('/errordoctorlogin')
def error_doctor_login():
    form = LoginForm(request.form)
    return render_template('doctorpages/error_doctor_login.html', form=form)

@blueprint.route('/patient_login')
def patient_login():
    form = LoginForm(request.form)
    if 'healthcard' in request.cookies:
        response = redirect(url_for("pages.patientaptbook"))
        return response
    else:
        return render_template('forms/patient_login.html', form=form)

@blueprint.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)

@blueprint.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@blueprint.route('/patient_register',  methods=['GET', 'POST'])
def patient_register():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birthday = request.form.get("birthday")
        gender = request.form.get("gender")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")
        address = request.form.get("address")
        age = int(request.form.get("age"))
        healthcard = request.form.get("healthcard")
        _obj = Patientcontroller()
        message = _obj.patient_register(first_name, last_name, birthday, gender, phone_number, email,address,age,healthcard)
        flash(message)
        return redirect(url_for(".patient_login"))
    return render_template('forms/patient_register.html')

@blueprint.route('/patientaptbook', methods=['GET', 'POST'])
def patientaptbook():
    user_id = request.cookies.get('healthcard')
    password = request.cookies.get('phoneNumber')
    print(user_id)
    print(password)
    return render_template('patientpages/patientdashboardapts.html', user = user_id )    

#patient login controller
@blueprint.route('/patientdashboard', methods=['GET', 'POST'])
def patientdashboard():
    if request.method == "POST":
        _healthcard = request.form['healthcard'];
        _phoneNumber = request.form['phoneNumber'];
        _obj = Patientcontroller()
        _user = _obj.user(_healthcard,_phoneNumber)

        print(type(_user))
        print(type(_user) == type(None))
        _user2 = 1
        _obj2 = _obj.patient_table(_healthcard)
        if type(_user) == type(None):
            response = redirect(url_for("pages.error_patient_login"))
        else:
            response = redirect(url_for("pages.patientaptbook"))

        response.set_cookie('healthcard', _healthcard)
        response.set_cookie('phoneNumber', _phoneNumber)
        print(request)
        return response

@blueprint.route('/register_doctor',  methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        speciality = request.form.get("speciality")
        city = request.form.get("city")
        password = request.form.get("password")
        permit_number = int(request.form.get("permit_number"))
        permit_number_str = request.form.get("permit_number")
        _obj = Doctorcontroller()
        users = _obj.find_doctor_by_permit_number(permit_number_str)
        # checks if the returned list is not empty
        if len(users) != 0:
            message = "Registration failed!!! User already exists."
            flash(message)
            return redirect(url_for(".doctor_login"))
        message = _obj.register_doctor(first_name, last_name, speciality, city, password, permit_number)
        flash(message)
        return redirect(url_for(".doctor_login"))
    return render_template('forms/register_doctor.html')
