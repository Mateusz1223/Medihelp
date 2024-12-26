from typing import Iterable

'''
Errors with the English descriptions are never meant to be seen by the user.
'''


class InvalidUserNameError(Exception):
    def __init__(self):
        super().__init__('Nieprawidłowa nazwa użytkownika!')


class InvalidIllnessNameError(Exception):
    def __init__(self):
        super().__init__('Nieprawidłowa nazwa choroby!')


class InvalidSubstanceNameError(Exception):
    def __init__(self):
        super().__init__('Nieprawidłowa nazwa substancji!')


class InvalidMedicineNameError(Exception):
    def __init__(self):
        super().__init__('Nieprawidłowa nazwa leku!')


class InvalidManufacturerNameError(Exception):
    def __init__(self):
        super().__init__('Nieprawidłowa nazwa producenta!')


class InvalidDosesError(Exception):
    def __init__(self):
        super().__init__('Ilość dawek nie może być mniejsza niż zero!')


class NotEnoughDosesError(Exception):
    def __init__(self):
        super().__init__('Nie ma wystarczającej ilości dawek!')


class TooManyDosesLeft(Exception):
    def __init__(self):
        super().__init__('Ilość pozostałych dawek nie może być większa od ilości dawek w pudełku!')


class InvalidWeekdayError(Exception):
    def __init__(self):
        super().__init__('Dzień tygodnia musi mieścić się w zakresie od 1 do 7!')


class InvalidAgeError(Exception):
    def __init__(self):
        super().__init__('Wiek musi być większy lub równy zeru!')


class InvalidBirthdateError(Exception):
    def __init__(self):
        super().__init__('Data urodzenia nie może być datą przyszłą!')


class EmptyListError(Exception):
    def __init__(self, list_name):
        super().__init__(f'Lista {list_name} nie może być pusta.')


class AllergyWarning(Exception):
    def __init__(self, substances: Iterable[str]):
        '''
        :param substance: name of the substance the user is allergic to
        :type substance: str
        '''
        substances = list(substances)
        substances.sort()
        info = f'Użytkownik nie może przyjąć leku, ponieważ jest uczulony na następujące substancje {', '.join([word for word in substances])}.'
        super().__init__(info)


class UserIsNotARecipientWarning(Exception):
    def __init__(self):
        super().__init__("Użytkownik nie może przyjąć tego leku, ponieważ nie jest wpisany na jego listę odbiorców!")


class AgeWarning(Exception):
    def __init__(self):
        super().__init__('Użytkownik jest za młody aby przyjąć ten lek!')


class ExpiredMedicineError(Exception):
    def __init__(self):
        super().__init__('Nie można przyjąć dawki tego leku, ponieważ jest przeterminowany!')


class MalformedDataError(Exception):
    def __init__(self, path, line):
        super().__init__(f'Zniekształcone dane w pliku {path}, w rzędzie (plik csv)/objekcie (plik json) {line}')


class IdAlreadyInUseError(Exception):
    def __init__(self):
        super().__init__('To ID jest już w użytku!')


class NoSuchIdInTheDatabaseError(Exception):
    def __init__(self):
        super().__init__('Nie ma obiektu o takim ID w bazie danych!')


class NoSuchIdInUserPrescriptionsError(Exception):
    def __init__(self):
        super().__init__('Użytkownik nie posiada recepty o danym ID!')


class DataLoadingError(Exception):
    def __init__(self):
        super().__init__('Wystąpił błąd podczas ładowania danych!')


class DataSavingError(Exception):
    def __init__(self):
        super().__init__('Wystąpił błąd podczas zapisywania danych do pliku!')


class NoFileOpenedError(Exception):
    def __init__(self):
        super().__init__('Brak otwartego pliku!')


class NoteIsToLongError(Exception):
    def __init__(self):
        super().__init__('Notatka może mieć maksymalnie 500 znaków!')


class EmptyNoteError(Exception):
    def __init__(self):
        super().__init__('Notatka nie może być pusta!')


class TooManyLinesInTheNoteError(Exception):
    def __init__(self):
        super().__init__('Notatka może mieć maksymalnie 6 linii!')


class MedicineDoesNotExistError(Exception):
    def __init__(self, id: int):
        super().__init__(f'Lek o id {id} nie istnieje!')


class UserDoesNotExistError(Exception):
    def __init__(self, id: int):
        super().__init__(f'Użytkownik o id {id} nie istnieje!')


class WrongArgumentsError(Exception):
    def __init__(self):
        super().__init__('Given parameters are invalid. Please check the docstring of the method/funtion you are trying to call!')


class ViewDoesNotExist(Exception):
    def __init__(self, name: str):
        super().__init__(f'View {name} does not exist!')


class IllegalCharactersInANameError(Exception):
    def __init__(self):
        super().__init__('Nazwa nie może zawierać następujących znaków: "\'", """, ",", "\\n"!')
