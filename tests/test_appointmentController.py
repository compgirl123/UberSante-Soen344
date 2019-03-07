from app.controllers.appointmentcontroller import AppointmentController

def test_connect_database():
    query1 = "INSERT INTO room (name) VALUES (?)"
    query2 = "SELECT name FROM room where name=?"
    query3 = "DELETE FROM room WHERE name=?"

    conn = AppointmentController.connect_database()

    conn.execute(query1,("test_room",))
    conn.execute(query2,("test_room",))
    result = conn.fetchall()
    assert result == [("test_room",)]
    conn.execute(query3,("test_room",))

def test_getappointment_type():
    regularAppointment = AppointmentController.getappointment_type("08:00:00", "08:20:00")
    assert regularAppointment == "Regular"
    annualAppointment = AppointmentController.getappointment_type("08:00:00", "09:00:00")
    assert annualAppointment == "Annual"
    specialAppointment = AppointmentController.getappointment_type("08:00:00", "12:00:00")
    assert specialAppointment == "Special"