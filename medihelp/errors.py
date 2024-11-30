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
