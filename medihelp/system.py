from .medicine_database import MedicineDatabase
from .users_database import UsersDatabase
from .errors import DataLoadingError, NoFileOpenedError, DataSavingError


class System:
    '''
    Class System is the main class of the programs logic. Manages users and medicines databases.

    Attributes
    ----------
    :ivar _medicines_database: Database with all the medicines registered in the system
    :vartype _medicines_database: MedicineDatabase

    :ivar _users_database: Database of users
    :vartype _users_database: UsersDatabase

    :ivar _medicines_file_path: Path to the file with medicines database the system is currently working with.
    :vartype _medicines_file_path: str

    :ivar _medicines_file_saved: True if there are no unsaved changes in medicines database, else False
    :vartype _medicines_file_saved: bool
    '''

    def __init__(self):
        self._medicines_database = MedicineDatabase()
        self._users_database = UsersDatabase()
        self._medicines_file_path = None
        self._medicines_file_saved = True

    def medicines_database(self):
        return self._medicines_database

    def users_database(self):
        return self._users_database

    def medicines_file_path(self):
        return self._medicines_file_path

    def medicines_file_saved(self):
        '''
        Useful for determining wheather or not changes are saved in currently loaded medicines file
        '''
        return self._medicines_file_saved

    def load_users_data(self):
        '''
        Loads users data from a data/users.json file
        '''
        try:
            with open('data/users.json', 'r') as file:
                self._users_database.read_from_file(file)
        except Exception as e:
            raise DataLoadingError from e

    def medicines_database_loaded(self):
        '''
        Checks if there is a medicines file loaded ???
        '''
        if self._medicines_file_path:
            return True
        return False

    def load_medicines_database_from(self, path: str):
        '''
        Clears self._medicines_database
        Loads database from the given file path
        Sets self._medicines_file_path to path
        Sets self._medicines_file_saved to True as the file was just opened

        :param path: Path to the file
        :type path: str
        '''
        self._medicines_database.clear()
        try:
            with open(path, 'r') as file:
                self._medicines_database.read_from_file(file)
        except Exception as e:
            raise DataLoadingError from e
        self._medicines_file_path = path
        self._medicines_file_saved = True

    def save_medicines_database(self, path=None):
        '''
        Saves data from medicine database to the file given by path or to the opened medicine file if there is no path given

        :param path: Path to the file (optional)
        :type path: str
        '''

        if not self.medicines_database_loaded() and not path:
            raise NoFileOpenedError
        if not path:
            path = self._medicines_file_path
        try:
            with open(path, 'w') as file:
                self._medicines_database.write_to_file(file)
        except Exception as e:
            raise DataSavingError from e
        self._medicines_file_saved = True
        if not self.medicines_database_loaded():
            self._medicines_file_path = path

    def get_medicines_list(self):
        '''
        Returns a list of medicines that are stored in self._medicines_database
        '''
        ret_list = []
        for medicine in self._medicines_database.medicines().values():
            ret_list.append(medicine)
        return ret_list
