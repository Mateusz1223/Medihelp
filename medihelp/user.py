from .errors import (InvalidUserNameError,
                     InvalidIllnessNameError,
                     InvalidSubstanceNameError,
                     InvalidBirthdateError,
                     IdAlreadyInUseError,
                     NoSuchIdInUserPrescriptionsError,
                     IllegalCharactersInANameError)
from .prescription import Prescription
from medihelp.common import normalize_name
from typing import Iterable, Optional
from datetime import date


class User:
    '''
    A class that encapsulates user-related data.

    Attributes
    ----------
    :ivar _id: User id
    :vartype id: int

    :ivar _name: Username.
    :vartype _name: str

    :ivar _birth_date: User birthdate. Used to calculate the age
    :vartype _birth_date: date

    :ivar _illnesses: set of illnesses that are cured by this medicine. Names should be written in lowercase.
    :vartype _illnesses: set{str}

    :ivar _allergies: set of active substances to which the user is allergic to. Names should be written in lowercase.
    :vartype _allergies: set{str}

    :param _prescriptions: dictionary of prescriptions that the user is subject to,
            where keys are prescriptions's IDs and values are prescriptions
    :type _prescriptions: iterable of Prescription
    '''

    def __init__(self,
                 id: int,
                 name: str,
                 birth_date: date,
                 illnesses: Optional[Iterable[str]] = None,
                 allergies: Optional[Iterable[str]] = None,
                 prescriptions: Optional[Iterable[Prescription]] = None):
        '''
        :param id: User's ID
        :type id: int
        :param name: Username.
        :type name: str
        :param birth_date: Age of the user.
        :type birth_date: int
        :param illnesses: (optional) list of illnesses that the user has. Names of illneses are written in lowercase.
        :type illnesses: iterable of str
        :param allergies: (optional) list of active substances to which the user is allergic to. Names of substances are written in lowercase.
        :type allergies: iterable of str
        :param prescriptions: (optional) list of prescriptions that the user is subject to,
        :type prescriptions: iterable of Prescription
        '''

        self._id = int(id)
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
        self._prescriptions = {}
        if prescriptions:
            for e in prescriptions:
                self.add_prescription(e)

    def __eq__(self, other):
        '''
        Useful for testing
        '''
        if type(other) is not User:
            return False
        if self.id() != other.id() or self.name() != other.name():
            return False
        if self.birth_date() != other.birth_date() or self.name() != other.name():
            return False
        if len(self.illnesses().intersection(other.illnesses())) != len(self.illnesses()):
            return False
        if len(self.allergies().intersection(other.allergies())) != len(self.allergies()):
            return False
        if len(self.prescriptions().keys()) != len(other.prescriptions().keys()):
            return False
        for key, value in self.prescriptions().items():
            other_value = other.prescriptions().get(key)
            if other_value != value:
                return False
        return True

    def id(self):
        return self._id

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
        try:
            name = normalize_name(name)
        except IllegalCharactersInANameError:
            raise InvalidUserNameError
        if len(name) < 1 or len(name) > 16:
            raise (InvalidUserNameError)
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
        try:
            illness = normalize_name(illness)
        except IllegalCharactersInANameError:
            raise InvalidIllnessNameError
        if illness:
            self._illnesses.add(illness)

    def remove_illness(self, illness):
        '''
        Removes illness from the _ilnesses list but first makes sure it doesn't contain any illegal characters.
        If the name is all white spaces it is ignored.
        The name is striped and set to lowercase.

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
        Adds substance to the __allergies list but first makes sure it doesn't contain any illegal characters.
        If the name is all white spaces it is ignored.
        The name is striped and set to lowercase.

        :param substance: substance name
        :type substance: str
        '''
        substance = str(substance).lower()
        try:
            substance = normalize_name(substance)
        except IllegalCharactersInANameError:
            raise InvalidSubstanceNameError
        if substance:
            self._allergies.add(substance)

    def remove_allergy(self, substance):
        '''
        Removes substance from the _allergies list

        :param substance: substance name
        :type substance: str
        '''

        self._allergies.remove(substance)

    def age(self):
        '''
        Calculates and returns the age of the user

        :return: Age of the user
        :rtype: int
        '''
        today = date.today()
        age = today.year - self.birth_date().year

        # Adjust if the birthday has not occurred yet this year
        if (today.month, today.day) < (self.birth_date().month, self.birth_date().day):
            age -= 1

        return age

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
        if prescription.id() in self.prescriptions().keys():
            raise IdAlreadyInUseError
        self._prescriptions[prescription.id()] = prescription

    def remove_prescription(self, prescription_id):
        '''
        Removes prescription with ID prescription_id from _prescriptions

        :param prescription_id: ID of the prescription
        :type prescription_id: int
        '''
        try:
            del self._prescriptions[prescription_id]
        except Exception:
            raise NoSuchIdInUserPrescriptionsError
