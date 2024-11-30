from .errors import InvalidNameError, InvalidDoseError, InvalidWeekdayError

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
    :ivar _medicine_name: Name of the prescribed medicine
    :vartype _medicine_name: str
    :ivar _dosage: how many doses of the medicine should the user take
    :vartype _dosage: int
    :ivar _weekday: what day should the user take the medicine
    :vartype _weekday: int
    '''

    def __init__(self, medicine_name, dosage, weekday):
        '''
        :param medicine_name: Name of the prescribed medicine
        :type medicine_name: str
        :param dosage: how many doses of the medicine should the user take
        :type dosage: int
        :param weekday: what day should the user take the medicine
        :type weekday: int
        '''

        medicine_name = str(medicine_name).lower()
        if not medicine_name:
            raise (InvalidNameError)
        self._medicine_name = medicine_name
        dosage = int(dosage)
        if dosage <= 0:
            raise (InvalidDoseError)
        self._dosage = dosage
        weekday = int(weekday)
        if weekday < 1 or weekday > 7:
            raise (InvalidWeekdayError)
        self._weekday = weekday

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
