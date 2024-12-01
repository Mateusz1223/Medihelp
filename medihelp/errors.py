class InvalidNameError(Exception):
    def __init__(self):
        super().__init__('Invalid name.')


class InvalidDoseError(Exception):
    def __init__(self):
        super().__init__('Dose must be greater than zero.')


class InvalidWeekdayError(Exception):
    def __init__(self):
        super().__init__('Weekday can range from 1 to 7.')


class InvalidAgeError(Exception):
    def __init__(self):
        super().__init__('Age must be greater or equal to zero.')


class EmptyListError(Exception):
    def __init__(self):
        super().__init__('This list cannot be empty.')


class AllergyWarning(Exception):
    def __init__(self, substance: str):
        '''
        :param substance: name of the substance the user is allergic to
        :type substance: str
        '''
        super().__init__(f'Medicine cannot be given to the user because he is allergic to {substance}.')


class AgeWarning(Exception):
    def __init__(self):
        super().__init__('User is not old enough to take the medicine.')
