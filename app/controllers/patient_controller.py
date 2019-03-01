from app.controllers.controller import Controller
from app.classes.database_container import DatabaseContainer
from app.classes.patient import Patient
import app.classes.catalogs

class PatientController(Controller):
	"""
	This class uses the Singleton pattern.
	"""
	_instance = None

	@staticmethod
	def get_instance():
	    """ Static access method. """
	    if PatientController._instance is None:
	        PatientController._instance = PatientController()
	    return PatientController._instance

	def __init__(self):
	    if PatientController._instance is not None:
	        raise Exception("This class is a singleton!")

	    else:
	        PatientController._instance = self
	        Controller.__init__(self, DatabaseContainer.get_instance())

	        self._db_loaded = False
	        self._patient_catalog =  app.classes.catalogs.PatientCatalog()

	# function takes self and a string "healthCard" to get the patient from the patient table.
	# returns list with client information or emptylist if client doesn't
	# exist in database
	def get_patient_by_healthCard(self, healthcard):

	    found_patient = []

	    patients = self._patient_catalog.get_all()

	    for id, patientObj in patients.items():

	        if patientObj._healthCard == healthCard:
	            found_patient.append(patientObj)

	    return found_patient

	# function takes self and several values to create a patient
	# inserts a new patient into the patient table
	def create_patient(self, firstName, lastName, birthday, email, phoneNumber, gender, address,
	                  age, healthCard):

	    attributesDict = {"firstName": firstName, "lastName": lastName, "birthday": birthday,
	                      "email": email, "phoneNumber": phoneNumber, "gender": gender, "address": address,
	                      "age": age, "health_card": healthCard}

	    self._patient_catalog.add(Patient(attributesDict), True)