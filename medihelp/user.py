from .errors import InvalidNameError, InvalidBirthdateError
from .prescription import Prescription
from typing import Iterable, Optional
from datetime import date


class User:
    '''
    A class to represent user.

    Attributes
    ----------
    :ivar _name: Username. Should be unique as it serves as an id.
    :vartype _name: str
    :ivar _birth_date: User birthdate. Used to calculate the age
    :vartype _birth_date: date
    :ivar _illnesses: list of illnesses that are cured by this medicine. Names should be written in lowercase.
    :vartype _illnesses: iterable of str
    :ivar _allergies: list of active substances to which the user is allergic to. Names should be written in lowercase.
    :vartype _allergies: iterable of str
    :ivar _prescriptions: list of prescriptions that the user is subject to.
    :vartype _prescriptions: list[Prescription]
    '''

    def __init__(self,
                 name: str,
                 birth_date: date,
                 illnesses: Optional[Iterable[str]] = None,
                 allergies: Optional[Iterable[str]] = None,
                 prescriptions: Optional[Iterable[Prescription]] = None):
        '''
        :param name: Username. Should be unique as it serves as an id.
        :type name: str
        :param birth_date: Age of the user.
        :type birth_date: int
        :param illnesses: (optional) list of illnesses that are cured by this medicine. Names of illneses are written in lowercase.
        :type illnesses: iterable of str
        :param allergies: (optional) list of active substances to which the user is allergic to. Names of substances are written in lowercase.
        :type allergies: iterable of str
        :param prescriptions: (optional) list of prescriptions that the user is subject to.
        :type prescriptions: list[Prescription]
        '''

        self.set_name(name)
        self.set_birth_date(birth_date)
        self._illnesses = set()
        if illnesses:
            for e in illnesses:
                self.add_illness(e)
        self._allergies = set()
        if allergies:
            for e in allergies:
                self.add_allergy(e)
        self._prescriptions = set()
        if prescriptions:
            for e in prescriptions:
                self.add_prescription(e)

    def name(self):
        '''
        Getter for _name

        :return: _name
        :rtype: str
        '''
        return self._name

    def set_name(self, name: str):
        '''
        Setter for _name

        :param age: name to be set
        :type age: str
        '''

        name = str(name)
        if not name:
            raise (InvalidNameError)
        self._name = name.title()

    def birth_date(self):
        '''
        Getter for _birth_date
        '''
        return self._birth_date

    def set_birth_date(self, birth_date: date):
        '''
        Setter for _birth_date. Makes sure birthdate is not a date in the future
        '''

        if date.today() < birth_date:
            raise (InvalidBirthdateError)
        self._birth_date = birth_date

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
        self._illnesses.add(illness)

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

    def age(self):
        '''
        :return: Age of the user
        :rtype: int
        '''
        today = date.today()
        age = today.year - self.birth_date().year

        # Adjust if the birthday has not occurred yet this year
        if (today.month, today.day) < (self.birth_date().month, self.birth_date().day):
            age -= 1

        return age

    def add_allergy(self, substance):
        '''
        Adds substance to the __allergies list

        :param substance: substance name
        :type substance: str
        '''

        substance = str(substance).lower()
        if not substance:
            raise (InvalidNameError)
        self._allergies.add(substance)

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
        self._prescriptions.add(prescription)

    def remove_prescription(self, prescription):
        '''
        Removes prescription from the _prescriptions list

        :param prescription: prescription
        :type prescription: Prescription
        '''
        self._prescriptions.remove(prescription)
