from .medicine_database import MedicineDatabase
from .users_database import UsersDatabase
from .errors import DataLoadingError


class System:
    '''
    Class System is the main class of the program responsible for managing databases, users and gui.

    Attributes
    ----------
    :ivar medicines_database: Database with all the medicines registered in the system
    :vartype medicines_database: MedicineDatabase

    :ivar users_database: Database of users
    :vartype users_database: UsersDatabase
    '''

    def __init__(self):
        self.medicines_database = MedicineDatabase()
        try:
            with open('data/medicines.csv', 'r') as file:
                self.medicines_database.read_from_file(file)
        except Exception as e:
            raise DataLoadingError from e

        self.users_database = UsersDatabase()
        try:
            with open('data/users.json', 'r') as file:
                self.users_database.read_from_file(file)
        except Exception as e:
            raise DataLoadingError from e
