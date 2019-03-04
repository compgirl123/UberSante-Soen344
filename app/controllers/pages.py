from flask import render_template, Blueprint, request, make_response , redirect , url_for, flash
from app.forms import *
from app.controllers.nursecontroller import *
from app.controllers.doctorcontroller import *
import requests

import base64

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
    #_name = request.form['form-nurselogin'];
    return render_template('nursepages/findnurse.html')

@blueprint.route('/nurseaptbook', methods=['GET', 'POST'])
def nurseaptbook():
    user_id = request.cookies.get('nurseid')
    password = request.cookies.get('password')
    print(user_id)
    print(password)
    #_name = request.form['form-nurselogin'];
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
            #print("User not found")
            response = redirect(url_for("pages.error_nurse_login"))
            #raise ValueError("Invalid username or password supplied")
        else:
            print("H")
            response = redirect(url_for("pages.nurseaptbook"))
        #response = redirect(url_for("pages.nurseaptbook"))
        response.set_cookie('nurseid', _name)
        response.set_cookie('password', _password)
        print(request)
        return response
        #return response


@blueprint.route('/doctoraptbook', methods=['GET', 'POST'])
def doctoraptbook():
    user_id = request.cookies.get('permitnumber')
    password = request.cookies.get('password')
    print(user_id)
    print(password)
    #_name = request.form['form-nurselogin'];
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
            #print("User not found")
            response = redirect(url_for("pages.error_doctor_login"))
            #raise ValueError("Invalid username or password supplied")
        else:
            print("H")
            response = redirect(url_for("pages.doctoraptbook"))
        #response = redirect(url_for("pages.nurseaptbook"))
        response.set_cookie('permitnumber', _name)
        response.set_cookie('password', _password)
        print(request)
        return response
        #return response



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
    return render_template('forms/nurse_login.html', form=form)

@blueprint.route('/nurse_doctor_logout')
def nurse_doctor_logout():
    response = redirect(url_for("pages.home"))
    response.set_cookie('nurseid', expires=0)
    response.set_cookie('permitnumber', expires=0)
    return response
    #form = LoginForm(request.form)
    #return render_template('pages/placeholder.home.html', form=form)

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
        return render_template('forms/register_doctor.html')
    return render_template('forms/register_doctor.html')
