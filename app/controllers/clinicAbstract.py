"""
Define the skeleton of an algorithm in an operation, deferring some
steps to subclasses. Template Method lets subclasses redefine certain
steps of an algorithm without changing the algorithm's structure.
"""

import abc
from app.controllers.nursecontroller import *
from app.controllers.doctorcontroller import *
# add patient 
class ClinicAbstract(metaclass=abc.ABCMeta):
    """
    Define abstract primitive operations that concrete subclasses define
    to implement steps of an algorithm.
    Implement a template method defining the skeleton of an algorithm.
    The template method calls primitive operations as well as operations
    defined in AbstractClass or those of other objects.
    """

    def template_method(self):  
        self.process_doctor()
        self.process_nurse()

    def process_doctor(self):
        _obj1 = Doctorcontroller()
        return _obj1
       # pass

    def process_nurse(self):
        _obj2 = Nursecontroller()
        return _obj2
       # pass
