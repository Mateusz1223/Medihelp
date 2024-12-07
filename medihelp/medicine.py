from datetime import date
from .errors import (InvalidNameError,
                     InvalidDosesError,
                     TooManyDosesLeft,
                     NotEnoughDosesError,
                     InvalidAgeError,
                     EmptyListError,
                     AllergyWarning,
                     AgeWarning,
                     ExpiredMedicineError,
                     InvalidUserIDError)
from typing import Iterable


class Medicine:
    '''
    A class to represent a single medicine.

    Attributes (all of the private attributes can be accesed with a getter)
    ----------
    :ivar _id: Unique Id of the medicine
    :vartype _id: int

    :ivar _name: Name of the medicine.
    :vartype _name: str

    :ivar _manufacturer: Name of the manufacturer.
    :vartype _manufacturer: str

    :ivar _illnesses: Set of illnesses that are cured by this medicine. Illness names are written in lowercase.
    :vartype _illnesses: iterable of str

    :ivar _recipients: Set of the IDs of the users who are taking the medicine. (0 - Dad, 1 - Mom, 2 - Child)
    :vartype _recipients: iterable of int

    :ivar _substances: Set of active substances in the medicine. Substance names are in lowercase.
    :vartype _substances: iterable of str

    :ivar _recommended_age: Recipent recommended age.
    :vartype _recommended_age: int

    :ivar _doses: number of doses in the box.
    :vartype _doses: int

    :ivar _doses_left: how many doses there is left.
    :vartype _doses_left: int

    :ivar _expiration_date: Expiration date.
    :vartype _expiration_date: date

    :ivar _notes: List of three objects. Each of them represents note from one user
    :vartype _notes: list[str/None]
    '''

    def __init__(self, id: int,
                 name: str,
                 manufacturer: str,
                 illnesses: Iterable[str],
                 substances: Iterable[str],
                 recommended_age: int,
                 doses: int,
                 doses_left: int,
                 expiration_date: date,
                 recipients=None):
        '''
        :param id: Unique Id of the medicine
        :type id: int
        :param name: Name of the medicine.
        :type name: str
        :param manufacturer: Name of the manufacturer.
        :type manufacturer: str
        :param illnesses: List of illnesses that are cured by this medicine.
        :type illnesses: iterable of str
        :param substances: List of active substances in the medicine.
        :type substances: iterable of str
        :param recommended_age: Recipent recommended age. Must be greater or equal to zero
        :type recommended_age: int
        :param doses: number of doses in the box. Must be greater than zero
        :type doses: int
        :param doses_left: how many doses there is left.
        :type doses_left: int
        :param expiration_date: Expiration date.
        :type expiration_date: date
        :param recipients: Set of the IDs of the users who are taking the medicine. (0 - Dad, 1 - Mom, 2 - Child)
        :tyoe recipients: iterable of int
        '''

        self._id = int(id)

        name = str(name).title()
        if name == '':
            raise InvalidNameError
        self._name = name

        manufacturer = str(manufacturer).title()
        if manufacturer == '':
            raise InvalidNameError
        self._manufacturer = manufacturer

        if not illnesses:
            raise EmptyListError
        self._illnesses = {str(illness).lower() for illness in illnesses}

        self._recipients = set()
        if recipients:
            for recipient in recipients:
                self.add_recipient(recipient)

        if not substances:
            raise EmptyListError
        self._substances = {str(substance).lower() for substance in substances}

        recommended_age = int(recommended_age)
        if recommended_age < 0:
            raise InvalidAgeError
        self._recommended_age = recommended_age

        doses = int(doses)
        if doses <= 0:
            raise InvalidDosesError
        self._doses = doses
        doses_left = int(doses_left)
        if doses_left <= 0:
            raise InvalidDosesError
        if doses_left > doses:
            raise TooManyDosesLeft
        self._doses_left = doses_left

        self._expiration_date = expiration_date

        self._notes = [None, None, None]

    def __eq__(self, other):
        '''
        Useful when comparing instances of medicines in tests.
        '''
        if self.id() != other.id() or self.name() != other.name():
            return False
        if self.manufacturer() != other.manufacturer() or self.recommended_age() != other.recommended_age():
            return False
        if self.doses() != other.doses() or self.doses_left() != other.doses_left():
            return False
        if self.expiration_date() != other.expiration_date() or self.doses_left() != other.doses_left():
            return False
        if len(self.illnesses().intersection(other.illnesses())) != len(self.illnesses()):
            return False
        if len(self.substances().intersection(other.substances())) != len(self.substances()):
            return False
        if len(self.recipients().intersection(other.recipients())) != len(self.recipients()):
            return False
        if self._notes != other._notes:
            return False
        return True

    def __hash__(self):
        return hash((self.id, self.name))

    def id(self):
        return self._id

    def name(self):
        return self._name

    def manufacturer(self):
        return self._manufacturer

    def illnesses(self):
        return self._illnesses

    def recipients(self):
        return self._recipients

    def substances(self):
        return self._substances

    def recommended_age(self):
        return self._recommended_age

    def doses(self):
        return self._doses

    def doses_left(self):
        return self._doses_left

    def expiration_date(self):
        return self._expiration_date

    def note(self, user_id):
        '''
        Returnes the given user's note for this medicine.

        :param user_id: 0 - Dad, 1 - Mom, 2 - Child
        :type user_id: int
        '''
        if user_id < 0 or user_id > 2:
            raise InvalidUserIDError
        return self._notes[user_id]

    def set_note(self, user_id, note):
        '''
        Changes value of the given user's note for this medicine.

        :param user_id: 0 - Dad, 1 - Mom, 2 - Child
        :type user_id: int
        '''
        if user_id < 0 or user_id > 2:
            raise InvalidUserIDError
        if note:
            self._notes[user_id] = str(note)
        else:
            self._notes[user_id] = None

    def add_recipient(self, user_id):
        if user_id < 0 or user_id > 2:
            raise InvalidUserIDError
        self._recipients.add(user_id)

    def remove_recipient(self, user_id):
        if user_id < 0 or user_id > 2:
            raise InvalidUserIDError
        self._recipients.remove(user_id)

    def take_doses(self, doses, user):
        '''
        Checks if the user can take the medicine based on substances it contains and user allergies. If not raises AllergyWarning
        Checks if the user can take the medicine based on his age the medicine reccomended age. If not raises AgeWarning
        Substracts doses from _doses_left if there is enough of them.
        '''
        if self.is_expired():
            raise (ExpiredMedicineError)
        allergies = self.substances().intersection(user.allergies())
        if allergies:
            raise (AllergyWarning(allergies))
        if self.recommended_age() > user.age():
            raise (AgeWarning)
        if self.doses_left() < doses:
            raise (NotEnoughDosesError)
        self._doses_left -= doses

    def is_expired(self) -> bool:
        return date.today() > self.expiration_date()
