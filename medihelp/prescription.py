from .errors import InvalidNameError, InvalidDosesError, InvalidWeekdayError

weekday_name_to_number = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}

weekday_number_to_name = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}


class Prescription:
    '''
    A class to represent user's prescription

    Attributes
    ----------
    :ivar _medicine_name: Name of the prescribed medicine. Name starts with uppercase.
    :vartype _medicine_name: str

    :ivar _dosage: how many doses of the medicine should the user take
    :vartype _dosage: int

    :ivar _weekday: what day should the user take the medicine
    :vartype _weekday: int
    '''

    def __init__(self, medicine_name: str, dosage: int, weekday: int):
        '''
        :param medicine_name: Name of the prescribed medicine
        :type medicine_name: str
        :param dosage: how many doses of the medicine should the user take
        :type dosage: int
        :param weekday: what day should the user take the medicine. Number from 1 to 7
        :type weekday: int
        '''

        medicine_name = str(medicine_name).title()
        if not medicine_name:
            raise (InvalidNameError)
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

    def medicine_name(self):
        '''
        Getter for _medicine_name

        :return: _medicine_name
        :rtype: str
        '''
        return self._medicine_name

    def dosage(self):
        '''
        Getter for _dosage

        :return: _dosage
        :rtype: int
        '''
        return self._dosage

    def weekday(self):
        '''
        Getter for _weekday

        :return: _weekday
        :rtype: int
        '''
        return self._weekday

    def __str__(self):
        return f'{self.dosage()} doses of {self.medicine_name()} every {weekday_number_to_name[self.weekday()]}.'
