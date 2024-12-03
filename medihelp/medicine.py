from datetime import date
from .errors import InvalidNameError, InvalidDoseError, InvalidAgeError, EmptyListError
from typing import List, Iterable


class Medicine:
    '''
    A class to represent a single medicine.

    Attributes (all of the private attributes can be accesed with a getter)
    ----------
    :ivar _name: Name of the medicine.
    :vartype _name: str
    :ivar _manufacturer: Name of the manufacturer.
    :vartype _manufacturer: str
    :ivar _illnesses: List of illnesses that are cured by this medicine. Illness names are written in lowercase.
    :vartype _illnesses: iterable of str
    :ivar _recipents: List of the names of the users who are taking the medicine.
    :vartype _recipents: iterable of str
    :ivar _substances: List of active substances in the medicine. Substance names are in lowercase.
    :vartype _substances: iterable of str
    :ivar _recommended_age: Recipent recommended age.
    :vartype _recommended_age: int
    :ivar _doses: number of doses in the box.
    :vartype _doses: int
    :ivar _doses_left: how many doses there is left.
    :vartype _doses_left: int
    :ivar _expiration_date: Expiration date.
    :vartype _expiration_date: date
    :ivar _notes: Notes that can be added by users.
    :vartype _notes: list[Note]
    '''

    def __init__(self, name: str,
                 manufacturer: str,
                 illnesses: Iterable[str],
                 substances: Iterable[str],
                 recommended_age: int,
                 doses: int,
                 expiration_date: date):
        '''
        :param _name: Name of the medicine.
        :type _name: str
        :param _manufacturer: Name of the manufacturer.
        :type _manufacturer: str
        :param _illnesses: List of illnesses that are cured by this medicine.
        :type _illnesses: iterable of str
        :param _substances: List of active substances in the medicine.
        :type _substances: iterable of str
        :param _recommended_age: Recipent recommended age. Must be greater or equal to zero
        :type _recommended_age: int
        :param _doses: number of doses in the box. Must be greater than zero
        :type _doses: int
        :param _expiration_date: Expiration date.
        :type _expiration_date: date
        '''

        name = str(name).title()
        if name == '':
            raise (InvalidNameError)
        self._name = name

        manufacturer = str(manufacturer).title()
        if manufacturer == '':
            raise (InvalidNameError)
        self._manufacturer = manufacturer

        if not illnesses:
            raise (EmptyListError)
        self._illnesses = {str(illness).lower() for illness in illnesses}

        if not substances:
            raise (EmptyListError)
        self._substances = {str(substance).lower() for substance in substances}

        recommended_age = int(recommended_age)
        if recommended_age < 0:
            raise (InvalidAgeError)
        self._recommended_age = recommended_age

        doses = int(doses)
        if doses <= 0:
            raise (InvalidDoseError)
        self._doses = doses
        self._doses_left = doses

        self._expiration_date = expiration_date

        self._notes = []

    def name(self):
        '''
        Getter for _name
        '''
        return self._name

    def manufacturer(self):
        '''
        Getter for _manufacturer
        '''
        return self._manufacturer

    def illnesses(self):
        '''
        Getter for _illnesses
        '''
        return self._illnesses

    def substances(self):
        '''
        Getter for _substances
        '''
        return self._substances

    def recommended_age(self):
        '''
        Getter for _recommended_age
        '''
        return self._recommended_age

    def doses(self):
        '''
        Getter for _doses
        '''
        return self._doses

    def doses_left(self):
        '''
        Getter for _doses_left
        '''
        return self._doses_left

    def expiration_date(self):
        '''
        Getter for _expiration_date
        '''
        return self._expiration_date

    def add_note(self, note):
        pass

    def take_doses(self, doses, user):
        '''
        Checks if the user can take the medicine based on substances it contains and user allergies. If not raises AllergyWarning
        Checks if the user can take the medicine based on his age the medicine reccomended age. If not raises AgeWarning
        Substracts doses from _doses_left if there is enough of them.
        '''
        pass

    def is_expired(self) -> bool:
        return date.today() > self.expiration_date()
