from .errors import InvalidNameError, InvalidAgeError
from .prescription import Prescription


class User:
    '''
    A class to represent user.

    Attributes
    ----------
    :ivar _name: Username. Should be unique as it serves as an id.
    :vartype _name: str
    :ivar _age: Age of the user.
    :vartype _age: int
    :ivar _illnesses: List of illnesses that are cured by this medicine. Names should be written in lowercase.
    :vartype _illnesses: List[str]
    :ivar _allergies: List of active substances to which the user is allergic to. Names should be written in lowercase.
    :vartype _allergies: List[str]
    :ivar _prescriptions: List of prescriptions that the user is subject to.
    :vartype _prescriptions: List[Prescription]
    '''

    def __init__(self, name, age, illnesses=[], allergies=[], prescriptions=[]):
        '''
        :param name: Username. Should be unique as it serves as an id.
        :type name: str
        :param age: Age of the user.
        :type age: int
        :param illnesses: List of illnesses that are cured by this medicine. Names of illneses are written in lowercase.
        :type illnesses: List[str]
        :param allergies: List of active substances to which the user is allergic to. Names of substances are written in lowercase.
        :type allergies: List[str]
        :param prescriptions: List of prescriptions that the user is subject to.
        :type prescriptions: List[Prescription]
        '''

        self.set_name(name)
        self.set_age(age)
        self._illnesses = []
        for e in illnesses:
            self.add_illness(e)
        self._allergies = []
        for e in allergies:
            self.add_allergy(e)
        self._prescriptions = []
        for e in prescriptions:
            self.add_prescription(e)

    def name(self):
        '''
        Getter for _name

        :return: _name
        :rtype: str
        '''
        return self._name

    def set_name(self, name):
        '''
        Setter for _name

        :param age: name to be set
        :type age: str
        '''

        name = str(name)
        if not name:
            raise (InvalidNameError)
        self._name = name.title()

    def age(self):
        '''
        Getter for _age

        :return: _age
        :rtype: int
        '''
        return self._age

    def set_age(self, age):
        '''
        Setter for _age

        :param age: new age
        :type age: int
        '''

        age = int(age)
        if age < 0:
            raise (InvalidAgeError)
        self._age = age

    def illnesses(self):
        '''
        Getter for _illnesses

        :return: _illnesses
        :rtype: list[str]
        '''
        return self._illnesses

    def add_illness(self, illness):
        '''
        Adds illness to the _ilnesses list

        :param illness: ilness name
        :type illness: str
        '''

        illness = str(illness).lower()
        if not illness:
            raise (InvalidNameError)
        self._illnesses.append(illness)

    def remove_illness(self, illness):
        '''
        Removes illness from the _ilnesses list

        :param illness: ilness name
        :type illness: str
        '''

        self._illnesses.remove(illness)

    def allergies(self):
        '''
        Getter for _allergies

        :return: _allergies
        :rtype: list[str]
        '''
        return self._allergies

    def add_allergy(self, substance):
        '''
        Adds substance to the __allergies list

        :param substance: substance name
        :type substance: str
        '''

        substance = str(substance).lower()
        if not substance:
            raise (InvalidNameError)
        self._allergies.append(substance)

    def remove_allergy(self, substance):
        '''
        Removes substance from the _allergies list

        :param substance: substance name
        :type substance: str
        '''

        self._allergies.remove(substance)

    def prescriptions(self):
        '''
        Getter for _prescriptions

        :return: _prescriptions
        :rtype: list[str]
        '''
        return self._prescriptions

    def add_prescription(self, prescription):
        '''
        Adds prescription to the _prescriptions list

        :param prescription: prescription
        :type prescription: Prescription
        '''
        if type(prescription) is not Prescription:
            raise (ValueError)
        self._prescriptions.append(prescription)

    def remove_prescription(self, prescription):
        '''
        Removes prescription from the _prescriptions list

        :param prescription: prescription
        :type prescription: Prescription
        '''
        self._prescriptions.remove(prescription)
