from typing import Iterable


class InvalidNameError(Exception):
    def __init__(self):
        super().__init__('Invalid name.')


class InvalidDosesError(Exception):
    def __init__(self):
        super().__init__('Dose must be greater than zero.')


class NotEnoughDosesError(Exception):
    def __init__(self):
        super().__init__('There is not enough doses of the medicine.')


class TooManyDosesLeft(Exception):
    def __init__(self):
        super().__init__('There cannot be more doses left than doses!')


class InvalidWeekdayError(Exception):
    def __init__(self):
        super().__init__('Weekday can range from 1 to 7.')


class InvalidAgeError(Exception):
    def __init__(self):
        super().__init__('Age must be greater or equal to zero.')


class InvalidBirthdateError(Exception):
    def __init__(self):
        super().__init__('Birthdate cannot be a date in the future')


class EmptyListError(Exception):
    def __init__(self):
        super().__init__('This list cannot be empty.')


class AllergyWarning(Exception):
    def __init__(self, substances: Iterable[str]):
        '''
        :param substance: name of the substance the user is allergic to
        :type substance: str
        '''
        substances = list(substances)
        substances.sort()
        info = f'Medicine cannot be given to the user because he is allergic to {', '.join([word for word in substances])}.'
        super().__init__(info)


class AgeWarning(Exception):
    def __init__(self):
        super().__init__('User is not old enough to take the medicine.')


class ExpiredMedicineError(Exception):
    def __init__(self):
        super().__init__('This medicine is expired!')


class InvalidUserIDError(Exception):
    def __init__(self):
        super().__init__('User Id must range from 0 to 2!')


class MalformedDataError(Exception):
    def __init__(self, path, line):
        super().__init__(f'Zniekształcone dane w pliku {path}, w rzędzie (plik csv)/objekcie (plik json) {line}')


class IdAlreadyInUseError(Exception):
    def __init__(self):
        super().__init__('This ID is already in use in the database!')


class NoSuchIdInTheDatabaseError(Exception):
    def __init__(self):
        super().__init__('There is no such id in the database!')


class DataLoadingError(Exception):
    def __init__(self):
        super().__init__('Wystąpił błąd podczas ładowania danych!')


class DataSavingError(Exception):
    def __init__(self):
        super().__init__('Wystąpił błąd podczas otwierania pliku!')


class NoFileOpenedError(Exception):
    def __init__(self):
        super().__init__('Brak otwartego pliku!')
