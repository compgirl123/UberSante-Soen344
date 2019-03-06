from flask import render_template, Blueprint, request, make_response , redirect, url_for, flash
from app.forms import *
from app.controllers.nursecontroller import *
from app.controllers.doctorcontroller import *
from app.controllers.patientcontroller import *

import requests
import base64
import datetime

import urllib.request as urllib2
from urllib.request import urlopen
import urllib.parse
from http.cookiejar  import CookieJar

from urllib.request import urlopen


'''
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# input-type values from the html form
formdata = { "username" : request.form['name'], "password": request.form['password'] }
data_encoded = urllib.urlencode(formdata)
response = opener.open("https://page.com/login.php", data_encoded)
content = response.read()
'''
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
    user_id = request.cookies.get('nurseid')
    password = request.cookies.get('password')
    print(user_id)
    return render_template('nursepages/findnurse.html')

@blueprint.route('/nurseaptbook', methods=['GET', 'POST'])
def nurseaptbook():
    user_id = request.cookies.get('nurseid')
    password = request.cookies.get('password')
    print(user_id)
    print(password)
    return render_template('nursepages/nursedashboardbookapts.html', user = user_id )

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
            response = redirect(url_for("pages.nurseaptbook"))

        response.set_cookie('nurseid', _name)
        response.set_cookie('password', _password)
        print(request)
        return response


@blueprint.route('/doctoraptbook', methods=['GET', 'POST'])
def doctoraptbook():
    user_id = request.cookies.get('permitnumber')
    password = request.cookies.get('password')
    print(user_id)
    print(password)
    return render_template('doctorpages/doctordashboardapts.html', user = user_id )

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
            response = redirect(url_for("pages.doctoraptbook"))

        response.set_cookie('permitnumber', _name)
        response.set_cookie('password', _password)
        print(request)
        return response

@blueprint.route('/doctorlogin')
def doctor_login():
    form = LoginForm(request.form)
    if 'permitnumber' in request.cookies:
        response = redirect(url_for("pages.doctoraptbook"))
        return response
    else:
        return render_template('forms/doctor_login.html', form=form)

@blueprint.route('/nurselogin')
def nurse_login():
    form = LoginForm(request.form)
    if 'nurseid' in request.cookies:
        response = redirect(url_for("pages.nurseaptbook"))
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


@blueprint.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


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
    time_slot_list = schedule_time_slots()
    print(user_id)
    print(password)
    return render_template('patientpages/patientdashboardapts.html', user = user_id, tlist = time_slot_list )    

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
        _obj = Doctorcontroller()
        message = _obj.register_doctor(first_name, last_name, speciality, city, password, permit_number)
        flash(message)
        return redirect(url_for(".doctor_login"))
    return render_template('forms/register_doctor.html')


#function to generate time slots
def schedule_time_slots():
    time_slot_list = []

    a = datetime.time(8,0,0)
    time_slot_list.append(a)
    #print a          
    for x in range(0,36):
        b = addSecs(a, 1200)
        timeStr = str(b)
        splitTime = timeStr.split(':')
        hours = int(splitTime[0])
        mins = int(splitTime[1])
        secs = int(splitTime[2])
        a = datetime.time(hours,mins,secs)
        #print b
        time_slot_list.append(b)

    return time_slot_list

def addSecs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

