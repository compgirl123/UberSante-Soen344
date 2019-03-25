import pytest
from app.controllers.appointmentcontroller import AppointmentController

def test_connect_database():
    query1 = "SELECT name FROM room WHERE name=?"
    conn = AppointmentController.connect_database()
    conn.execute(query1,("test_room",))
    result = conn.fetchall()
    assert result == [("test_room",)]

def test_getappointment_type():
    regularAppointment = AppointmentController.getappointment_type("08:00:00", "08:20:00")
    assert regularAppointment == "Regular"
    annualAppointment = AppointmentController.getappointment_type("08:00:00", "09:00:00")
    assert annualAppointment == "Annual"
    specialAppointment = AppointmentController.getappointment_type("08:00:00", "12:00:00")
    assert specialAppointment == "Special"

def test_find_a_doctor():
    c = AppointmentController.connect_database()
    result = AppointmentController.find_a_doctor(c, 'tester', '01-01-2020', '08:40:00', '09:00:00')
    assert result == (1,)
    result = AppointmentController.find_a_doctor(c, 'tester', '01-01-2020', '07:00:00', '07:20:00')
    assert result == (1,)
    result = AppointmentController.find_a_doctor(c, 'tester', '01-01-2020', '07:00:00', '08:20:00')
    assert result == False
    result = AppointmentController.find_a_doctor(c, 'tester', '01-01-2020', '08:00:00', '09:00:00')
    assert result == False
    result = AppointmentController.find_a_doctor(c, 'tester', '02-01-2020', '08:00:00', '08:20:00')
    assert result == False

def test_find_room():
    c = AppointmentController.connect_database()
    result = AppointmentController.find_room(c, '01-01-2020', '07:00:00', '07:20:00')
    assert result == (1,)
    result = AppointmentController.find_room(c, '01-01-2020', '07:00:00', '08:20:00')
    assert result == False
    result = AppointmentController.find_room(c, '01-01-2020', '08:10:00', '09:00:00')
    assert result == False

def test_find_appointment():
    c = AppointmentController.connect_database()
    result = AppointmentController.find_appointment(c, '1', '01-01-2020')
    assert result == [(1,1, 'Regular', 'Approved', '01-01-2020','08:00:00','08:20:00',1,1)]
    result = AppointmentController.find_appointment(c, '1', '01-02-2020')
    assert result == []

def test_finalize_appointment():
    query='DELETE FROM appointment WHERE appointment_date=? AND doctor_id=?'
    c = AppointmentController.connect_database()
    result =  AppointmentController.finalize_appointment(c, '1', 'Annual', 'Approved', '12-12-1990', '12:00:00', '13:00:00', 1, 1)
    assert result == True
    c.execute(query,('12-12-1990',1))

def test_isAvailable():
    with pytest.raises(Exception, match=r'.* doctor .*'):
        AppointmentController.isAvailable('tester', '11-11-2000', '12:00:00', '12:20:00')
    with pytest.raises(Exception, match=r'.* room .*'):
        AppointmentController.isAvailable('tester', '01-02-2020', '08:00:00', '08:20:00')
    result = AppointmentController.isAvailable('tester', '01-02-2020', '09:00:00', '09:20:00')
    assert result == [(1,), (1,)]
    
def test_create_appointment():
    query='DELETE FROM appointment WHERE appointment_date=? AND patient_id=?'
    c = AppointmentController.connect_database()
    result =  AppointmentController.create_appointment('tester', '1', '01-02-2020', '12:00:00', '13:00:00')
    assert result == True
    c.execute(query,('01-02-2020',1))
    






