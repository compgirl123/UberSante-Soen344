from flask import render_template, Blueprint, request, make_response
from app.forms import *
from app.controllers.nursecontroller import *
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

@blueprint.route('/findnurse', methods=['GET', 'POST'])
def findnurse():
    #_name = request.form['form-nurselogin'];
    return render_template('nursepages/findnurse.html')

@blueprint.route('/nursedashboard', methods=['GET', 'POST'])
def nursedashboard():
    _name = request.form['name'];
    #nametest = request.form.get("name", False)
    # stores the name that was entered to the next page
    _password = request.form['password'];

    # stores the password that was entered to the next page

    _obj = Nursecontroller()
    _obj2 = _obj.nurse_table(_name)
    #print()
    #issue lies here
    return "dd"

'''
    s = requests.Session()
    data = {"name": request.form['name'], "password": request.form['name']}
    url = "http://127.0.0.1:5000/nurselogin"
    r = s.post(url, data=data)
    print(s.cookies)

    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # input-type values from the html form

    payload = { "username" : request.form['name'], "password": request.form['password'] }

    session = requests.Session()
    ss = session.post('http://127.0.0.1:5000/nurselogin',  data=payload)


    formdata = { "username" : request.form['name'], "password": request.form['password'] }
    #data = urllib.parse.urlencode(d).encode("utf-8")

    #data_encoded = urllib.parse.urlencode(formdata)
    3data_encoded = data_encoded.encode('ascii')

    #data_encoded = urllib.request.Request(formdata).encode('ascii')
    data_encoded = urllib.request.Request(formdata)
    request1 = urllib.request.Request('http://127.0.0.1:5000/nurselogin')
    base64string = bytes('%s:%s' % (request.form['name'], request.form['password']), 'ascii')
    #print(base64string)

    #result = urllib.request.urlopen(request1)
    resulttext = result.read()
    #print(type(data_encoded))
    #response = urllib.request.urlopen("http://127.0.0.1:5000/nurselogin")
    #response = opener.open("http://127.0.0.1:5000/nurselogin", data_encoded)
    #req = urllib2.Request("http://127.0.0.1:5000/nurselogin", data_encoded)
    #response = urllib2.urlopen(req)
    #the_page = response.read()
    #content = response.read()
    #print(content)

    return base64string
    #return _name;
    #return _password;
    # return 0;'''
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
