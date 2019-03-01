import abc
from app.classes.database_container import DatabaseContainer

class Catalog(abc.ABC):
    """Abstract class Catalog"""

    @abc.abstractmethod
    def get_all(self):
        """This method returns a collection"""
        pass

    @abc.abstractmethod
    def get(self, id):
        """This method returns a single object from a collection"""
        pass

    @abc.abstractmethod
    def add(self, object, add_to_db):
        """This method adds a single object to a collection"""
        pass


# Can be used to store either administrators or clients
class PatientCatalog(Catalog):

    def __init__(self):

        self.db = DatabaseContainer.get_instance()
        self._patients = {}

    def get_all(self):
        temp = self._patients
        return temp

    def get(self, health_card):
        print("Patient Health Care number-- > " + str(health_card))

        temp = self._patients[health_card]
        return temp

    def add(self, patient, add_to_db):

        if add_to_db is True:

            insert_new_user_query = 'INSERT INTO patient(first_name,last_name,birthday,gender,phone_number,email,address,age,health_card)' \
                                    'VALUES(?,?,?,?,?,?,?,?,?)'

            tuple_for_insert_query = (patient._first_name, patient._last_name, patient._birthday,
                                      patient._gender, patient._phone_number, patient._email, patient._address,
                                      patient._age, patient._health_card)

            # getting the id of the last inserted patient
            new_patient_id = self.db.execute_query_write(insert_new_user_query, tuple_for_insert_query).lastrowid
            # since the object created has by default id = 0, we have to set
            # its id to the id obtained above
            patient.set_id(new_patient_id)
            self._patients[new_patient_id] = patient

        else:
            self._patients[patient._id] = patient
            