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

def test_find_doctor():
    c = AppointmentController.connect_database()
    result = AppointmentController.find_doctor(c, 'tester', '01-01-2020', '08:40:00', '09:00:00')
    assert result == (1,)
    result = AppointmentController.find_doctor(c, 'tester', '01-01-2020', '07:00:00', '08:20:00')
    assert result == False
    result = AppointmentController.find_doctor(c, 'tester', '01-01-2020', '08:00:00', '09:00:00')
    assert result == False
    result = AppointmentController.find_doctor(c, 'tester', '02-01-2020', '08:00:00', '08:20:00')
    assert result == False



