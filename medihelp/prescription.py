from .errors import (InvalidMedicineNameError,
                     InvalidDosesError,
                     InvalidWeekdayError,
                     IllegalCharactersInANameError)
from medihelp.gui.common import normalize_name


class Prescription:
    '''
    Class Prescription represents informations about medicine that user takes regularly.
        Those informations are the name of the medicine, number of doses that user should take and the day of the week.

    Attributes
    ----------
    :ivar _id: ID of the prescription
    :vartype _id: int

    :ivar _medicine_name: Name of the prescribed medicine. Name starts with uppercase.
    :vartype _medicine_name: str

    :ivar _dosage: how many doses of the medicine should the user take
    :vartype _dosage: int

    :ivar _weekday: what day should the user take the medicine
    :vartype _weekday: int
    '''

    def __init__(self, id: int, medicine_name: str, dosage: int, weekday: int):
        '''
        :param id: ID of the prescription
        :type id: int
        :param medicine_name: Name of the prescribed medicine
        :type medicine_name: str
        :param dosage: how many doses of the medicine should the user take
        :type dosage: int
        :param weekday: what day should the user take the medicine. Number from 1 to 7
        :type weekday: int
        '''
        self._id = int(id)
        medicine_name = str(medicine_name).title()
        try:
            medicine_name = normalize_name(medicine_name)
        except IllegalCharactersInANameError:
            raise InvalidMedicineNameError
        if len(medicine_name) < 1 or len(medicine_name) > 16:
            raise InvalidMedicineNameError
        self._medicine_name = medicine_name
        dosage = int(dosage)
        if dosage <= 0:
            raise (InvalidDosesError)
        self._dosage = dosage
        weekday = int(weekday)
        if weekday < 1 or weekday > 7:
            raise (InvalidWeekdayError)
        self._weekday = weekday

    def __eq__(self, other):
        '''
        Useful for testing
        '''
        if self.id() != other.id():
            return False
        if self.medicine_name() != other.medicine_name():
            return False
        if self.dosage() != other.dosage():
            return False
        if self.weekday() != other.weekday():
            return False
        return True

    def __hash__(self):
        '''
        Useful for testing
        '''
        return hash((self.medicine_name(), self.dosage()))

    def id(self):
        return self._id

    def medicine_name(self):
        return self._medicine_name

    def dosage(self):
        return self._dosage

    def weekday(self):
        return self._weekday
