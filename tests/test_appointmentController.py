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