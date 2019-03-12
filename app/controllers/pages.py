from flask import render_template, Blueprint, request, make_response , redirect, url_for, flash
from app.forms import *
from app.controllers.nursecontroller import *
from app.controllers.doctorcontroller import *
from app.controllers.patientcontroller import *
from app.controllers.appointmentcontroller import *
import datetime

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

@blueprint.route('/payment')
def payment():
    return render_template('patientpages/payment.html')

@blueprint.route('/update_apt')
def update_apt():
    return render_template('patientpages/update_info_page.html')

@blueprint.route('/thank_you')
def thank_you():
    return render_template('patientpages/thank_you.html')

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
        #_obj2 = _obj.doctor_table(_name)
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

        users = _obj.find_patient_by_health_card(healthcard)
        # checks if the returned list is not empty
        if len(users) != 0:
            message = "Registration failed!!! User already exists."
            flash(message)
            return redirect(url_for(".patient_login"))

        message = _obj.patient_register(first_name, last_name, birthday, gender, phone_number, email,address,age,healthcard)
        flash(message)
        return redirect(url_for(".patient_login"))
    return render_template('forms/patient_register.html')

@blueprint.route('/updateapt', methods=['GET', 'POST'])
def updateapt():
    user_id = request.cookies.get('healthcard')
    password = request.cookies.get('phone_number')
    regularChecked = "checked"
    annualChecked = ""
    _doctor_obj = Doctorcontroller()
    _doctors_list = _doctor_obj.doctor_table()
    print(_doctors_list)
    doctorlist = []
    print(_doctors_list)
    for infos in _doctors_list:
        doctorlist.append(infos[2] + " " + infos[1])
    # check if annual or regular is selected and adjust the time slots accordingly
    opt_param = request.args.get("apttype")
    if opt_param is not None:
        if opt_param == "regular":
            time_slot_list = schedule_time_slots(1200, 36)
            regularChecked = "checked"
            annualChecked = ""
        elif opt_param == "annual":
            time_slot_list = schedule_time_slots(3600, 12)
            regularChecked = ""
            annualChecked = "checked"
    else:
        time_slot_list = schedule_time_slots(1200, 36)
    print(user_id)
    print(password)
    return render_template('patientpages/patientdashboardaptsupdate.html', user=user_id, tlist=time_slot_list,
                           regularCheck=regularChecked, annualCheck=annualChecked, doctorlist=doctorlist)


@blueprint.route('/patientaptbook', methods=['GET', 'POST'])
def patientaptbook():
    user_id = request.cookies.get('healthcard')
    password = request.cookies.get('phone_number')

    regularChecked = "checked"
    annualChecked = ""
    _doctor_obj = Doctorcontroller()
    _doctors_list = _doctor_obj.doctor_table()
    #print(_doctors_list)
    doctorlist = []
    #print(_doctors_list)
    for infos in _doctors_list:
        doctorlist.append(infos[2]+ " "+ infos[1])
    # check if annual or regular is selected and adjust the time slots accordingly
    opt_param = request.args.get("apttype")
    if opt_param is not None:
        if opt_param == "regular":
            time_slot_list = schedule_time_slots(1200, 36)
            regularChecked = "checked"
            annualChecked = ""
        elif  opt_param == "annual":
            time_slot_list = schedule_time_slots(3600, 12)
            regularChecked = ""
            annualChecked = "checked"
    else:
        time_slot_list = schedule_time_slots(1200, 36)
    #print(user_id)
    #print(password)

    return render_template('patientpages/patientdashboardapts.html', user = user_id, tlist = time_slot_list,
                           regularCheck = regularChecked, annualCheck = annualChecked , doctorlist = doctorlist)

@blueprint.route('/savebookedaptupdate', methods=['GET', 'POST'])
def savebookedaptupdate():

    if request.method == "POST":
        print(request.form)
        _time = request.form['time']
        _appointment_selected = request.form['appointment_selected']
        _doctor_picked = request.form['doctor_picked']
        response = redirect(url_for("pages.patient_apts_scheduled_update"))
        response.set_cookie('time', _time)
        response.set_cookie('appointment_selected', _appointment_selected)
        response.set_cookie('doctor_picked',_doctor_picked)
    return response


# save selected appointments booked for patients
@blueprint.route('/savebookedapt', methods=['GET', 'POST'])
def savebookedapt():

    if request.method == "POST":
        print(request.form)
        _time = request.form['time']
        _appointment_selected = request.form['appointment_selected']
        _doctor_picked = request.form['doctor_picked']
        response = redirect(url_for("pages.patient_apts_scheduled"))
        response.set_cookie('time', _time)
        response.set_cookie('appointment_selected', _appointment_selected)
        response.set_cookie('doctor_picked',_doctor_picked)
    return response

# view upcoming appointments for the patient
@blueprint.route('/patient_apts_scheduled', methods=['GET', 'POST'])
def patient_apts_scheduled():
    time = request.cookies.get('time')
    appointment_selected = request.cookies.get('appointment_selected')
    doctor_selected = request.cookies.get('doctor_picked')
    health_care = request.cookies.get('healthcard')

    _doc_obj = Doctorcontroller()
    _appointment_obj = AppointmentController()

    first_last_name_arr = doctor_selected.split(" ")
    _doc_query = _doc_obj.find_doctor_by_full_name(first_last_name_arr[0], first_last_name_arr[1])
    _doc_speciality = _doc_query[2]
    print(_doc_query[2])

    _time_end = get_time_end()

    date = appointment_selected.split("-")[1]
    print(appointment_selected.split("-")[1])
    print(str(_time_end[0]+":"+_time_end[1]+":"+_time_end[2]))

    _appointment_obj.create_appointment(_doc_query[2], 12345, str("0"+date), str(time), str(_time_end[0]+":"+_time_end[1]+":"+_time_end[2]))
    # create_appointment(doctor_speciality, patient_id, appointment_date, start_time, end_time)
    #_appointment_obj.create_appointment("Family", 12345, "03/11/2019", "09:40:00", "10:00:00")
    _obj_user = Patientcontroller()
    _patient_obj = Patientcontroller()
    _get_user = _patient_obj.find_a_patient(health_care)
    _user_full_name = _get_user[0]+" "+_get_user[1]

    return render_template('patientpages/patient_dashboard.html', time = time, appointment_selected = appointment_selected ,
                           doctor_picked = doctor_selected , user_name = _user_full_name)

# view upcoming appointments for the patient
@blueprint.route('/patient_apts_scheduled_update', methods=['GET', 'POST'])
def patient_apts_scheduled_update():
    time = request.cookies.get('time')
    appointment_selected = request.cookies.get('appointment_selected')
    doctor_selected = request.cookies.get('doctor_picked')
    health_care = request.cookies.get('healthcard')

    _doc_obj = Doctorcontroller()
    _appointment_obj = AppointmentController()

    first_last_name_arr = doctor_selected.split(" ")
    _doc_query = _doc_obj.find_doctor_by_full_name(first_last_name_arr[0], first_last_name_arr[1])
    _doc_speciality = _doc_query[2]
    print(_doc_query[2])

    _time_end = get_time_end()

    date = appointment_selected.split("-")[1]
    print(appointment_selected.split("-")[1])
    print(str(_time_end[0]+":"+_time_end[1]+":"+_time_end[2]))

    _appointment_obj.appointmentupdate(_doc_query[2], 12345, str("0"+date), str(time), str(_time_end[0]+":"+_time_end[1]+":"+_time_end[2]))
    #_appointment_obj.appointmentupdate("Gyne", 12345, "03/11/2019", "08:00:00", "08:20:00")
       # create_appointment(_doc_query[2], 12345, str("0"+date), str(time), str(_time_end[0]+":"+_time_end[1]+":"+_time_end[2]))
    # create_appointment(doctor_speciality, patient_id, appointment_date, start_time, end_time)
    #_appointment_obj.create_appointment("Family", 12345, "03/11/2019", "09:40:00", "10:00:00")
    _obj_user = Patientcontroller()
    _patient_obj = Patientcontroller()
    _get_user = _patient_obj.find_a_patient(health_care)
    _user_full_name = _get_user[0]+" "+_get_user[1]

    return render_template('patientpages/aptupdated.html', time = time, appointment_selected = appointment_selected ,
                           doctor_picked = doctor_selected , user_name = _user_full_name)
#patient update controller
'''@blueprint.route('/patientdashboardupdate', methods=['GET', 'POST'])
def patientdashboardupdate():
    if request.method == "POST":
        print("HELLO")
        print(request.form)
        _update = request.form['update']
        if request.form['update']:
            print(request.form['update'])
            response = redirect(url_for("pages.patientaptbook"))
            response.set_cookie('update', _update)
        else:
            response = redirect(url_for("pages.patientaptbook"))
            print('Structure is empty.')
    return response
    '''

#patient login controller
@blueprint.route('/patientdashboard', methods=['GET', 'POST'])
def patientdashboard():
    print(request.method)
    if request.method == "POST":
        _healthcard = request.form['healthcard']
        _phone_number = request.form['phone_number']
        _obj = Patientcontroller()
        _user = _obj.user(_healthcard,_phone_number)

        print(type(_user))
        print(type(_user) == type(None))

        _obj2 = _obj.patient_table(_healthcard)
        if type(_user) == type(None):
            message = "Patient is not in the system."
            flash(message)
            response = redirect(url_for("pages.patient_login"))

        else:
            response = redirect(url_for("pages.patientaptbook"))
            response.set_cookie('healthcard', _healthcard)
            response.set_cookie('phone_number', _phone_number)

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


#function to generate time slots
def schedule_time_slots(block_size = 1200, num_blocks = 36):
    time_slot_list = []

    a = datetime.time(8,0,0)
    time_slot_list.append(a)
    #print a          
    for x in range(0,num_blocks):
        b = addSecs(a, block_size)
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

# function to add 20 minute appointments and get ending time
def get_time_end():
    time = request.cookies.get('time')
    _time_split = time.split(":")
    _time_end = time.split(":")

    if (_time_split[1] == "00"):
        _time_end[1] = "20"
    elif (_time_split[1] == "20"):
        _time_end[1] = "40"
    elif (_time_split[1] == "40"):
        numb = int(_time_end[0])
        next_hour = numb + 1
        if(next_hour<10):
            _time_end[0] = "0" + str(next_hour)
        else:
            _time_end[0] = str(next_hour)
        _time_end[1] = "00"
    print(_time_end)
    return _time_end
