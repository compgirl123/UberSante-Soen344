class Patient:

    def __init__(self, arguments):

        if 'id' in dict(arguments):
            self._id = arguments['id']
        else:
            self._id = 0

        self._first_name = arguments['firstName']
        self._last_name = arguments['lastName']
        self._birthday = arguments['birthday']
        self._gender = arguments['gender']
        self._email = arguments['email']
        self._phone_number = arguments['phoneNumber'] 
        self._address = arguments['address']
        self._age = arguments['age']
        self._health_card = arguments['health_card']

    def get_id(self):
        """Returns the id of the object"""
        return self._id

    def set_id(self, id):
        """
        Sets the current id of the patienr in this object

        :param id:
        :return:
        """
        self._id = id  