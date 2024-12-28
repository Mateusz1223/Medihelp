from .medicine_database import MedicineDatabase
from .users_database import UsersDatabase
from .medicine import Medicine
from .user import User
from .errors import (DataLoadingError,
                     NoFileOpenedError,
                     DataSavingError,
                     MedicineDoesNotExistError,
                     UserDoesNotExistError)
from medihelp.prescription import Prescription
from typing import Iterable
from datetime import date


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

    def medicines(self):
        '''
        Returns a dictionary of medicines that are stored in self._medicines_database.medicines().
        IDs of the medicine are the keys and Medicine objects are the values.
        This dictionary should not be modify in any way!
        '''
        return self._medicines_database.medicines()

    def users(self):
        '''
        Returns a dictionary of users that are stored in self._medicines_database.medicines().
        IDs of users are the keys and User objects are the values.
        This dictionary should not be modify in any way!
        '''
        return self._users_database.users()

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

    def save_users_data(self):
        '''
        Saves users data to data/users.json file
        '''
        try:
            with open('data/users.json', 'w') as file:
                self._users_database.write_to_file(file)
        except Exception as e:
            raise DataSavingError from e

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

    def set_note(self, medicine_id: int, author_id: int, content: str):
        '''
        Sets the content of the note assigned to medicine with ID medicine_id where user with ID author_id is the author.

        :param medicine_id: ID of the medicine
        :type medicine_id: int

        :param author_id: ID of the user who is an author
        :type author_id: int

        :param content: New content of the note
        :type content: str
        '''
        if author_id not in self.users_database().users().keys():
            raise UserDoesNotExistError(author_id)
        medicine = self.medicines_database().medicines().get(medicine_id)
        if medicine:
            medicine.set_note(author_id, content)
        else:
            raise MedicineDoesNotExistError(medicine_id)

    def del_note(self, medicine_id: int, author_id: int):
        '''
       deletes the note assigned to medicine with ID medicine_id where user with ID author_id is the author.

        :param medicine_id: ID of the medicine
        :type medicine_id: int

        :param author_id: ID of the user who is an author
        :type author_id: int
        '''
        if author_id not in self.users_database().users().keys():
            raise UserDoesNotExistError(author_id)
        medicine = self.medicines_database().medicines().get(medicine_id)
        if medicine:
            medicine.del_note(author_id)
        else:
            raise MedicineDoesNotExistError(medicine_id)

    def add_medicine(self,
                     name: str,
                     manufacturer: str,
                     illnesses: Iterable[str],
                     substances: Iterable[str],
                     recommended_age: int,
                     doses: int,
                     doses_left: int,
                     expiration_date: date,
                     recipients=None,
                     notes: dict[int: str] = None):
        '''
        Adds medicine object to the medicine database and return ID assigned to the medicine

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
        :param recipients: Set of the IDs of the users who are taking the medicine. (optional)
        :type recipients: iterable of int
        :param notes: Dictionary of notes where IDs of authors are the keys and values are comments themselves (optional)
        :type notes: dict[int, str]

        :return: ID assigned to the created medicine object
        :rtype: int
        '''
        id = 0
        while id in self.medicines_database().medicines().keys():
            id += 1
        medicine = Medicine(id,
                            name=name,
                            manufacturer=manufacturer,
                            illnesses=illnesses,
                            substances=substances,
                            recommended_age=recommended_age,
                            doses=doses,
                            doses_left=doses_left,
                            expiration_date=expiration_date,
                            recipients=recipients,
                            notes=notes)
        self.medicines_database().add_medicine(medicine)
        return id

    def del_medicine(self, medicine_id: int):
        '''
        Deletes medicine with given ID from the database

        :param medicine_id: ID of the medicine that is to be deleted
        :type medicine_id: int
        '''
        self.medicines_database().delete_medicine(medicine_id)

    def change_medicine(self,
                        medicine_id: int,
                        name: str,
                        manufacturer: str,
                        illnesses: Iterable[str],
                        substances: Iterable[str],
                        recommended_age: int,
                        doses: int,
                        doses_left: int,
                        expiration_date: date,
                        recipients):
        '''
        Replaces old medicine object under the given id in the database with a new one.

        :param medicine_id: ID of the medicine to be modified
        :type medicine_id: int
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
        :param recipients: Set of the IDs of the users who are taking the medicine.
        :type recipients: iterable of int
        '''
        old_medicine = self.medicines().get(medicine_id)
        if not old_medicine:
            raise MedicineDoesNotExistError(medicine_id)
        new_medicine = Medicine(id=medicine_id,
                                name=name,
                                manufacturer=manufacturer,
                                illnesses=illnesses,
                                substances=substances,
                                recommended_age=recommended_age,
                                doses=doses,
                                doses_left=doses_left,
                                expiration_date=expiration_date,
                                recipients=recipients,
                                notes=old_medicine.notes())
        self.medicines_database().delete_medicine(medicine_id)
        self.medicines_database().add_medicine(new_medicine)

    def take_dose(self, medicine_id: int, user: User):
        '''
        1) Decrements medicine's _doses_left.
        2) Throws exceptions with a reason if the user can't take the medicine.

        :param medicine_id: ID of the medicine
        :type medicine_id: int

        :param user: User object used to determine if the user can take the medicine.
        :type user: User
        '''
        medicine = self.medicines().get(medicine_id)
        if not medicine:
            raise MedicineDoesNotExistError(medicine_id)
        medicine.take_doses(doses=1, user=user)

    def change_user(self,
                    user_id: int,
                    name: str,
                    birth_date: date,
                    illnesses: Iterable[str],
                    allergies: Iterable[str]):
        '''
        Replaces old user object under the given id in the database with a new one
            and saves users datatbase in the file

        :param user_id: User's ID
        :type user_id: int
        :param name: Username.
        :type name: str
        :param birth_date: Age of the user.
        :type birth_date: int
        :param illnesses: list of illnesses that the user has. Names of illneses are written in lowercase.
        :type illnesses: iterable of str
        :param allergies: list of active substances to which the user is allergic to. Names of substances are written in lowercase.
        :type allergies: iterable of str
        :param prescriptions: list of prescriptions that the user is subject to.
        :type prescriptions: list[Prescription]
        '''
        old_user = self.users().get(user_id)
        if not old_user:
            raise UserDoesNotExistError(user_id)
        new_user = User(id=user_id,
                        name=name,
                        birth_date=birth_date,
                        illnesses=illnesses,
                        allergies=allergies,
                        prescriptions=old_user.prescriptions().values())

        self.users_database().delete_user(user_id)
        self.users_database().add_user(new_user)

        self.save_users_data()

    def del_prescription(self, user_id: int, prescription_id: int):
        '''
        Deletes prescription with given ID from the user with given ID
            and saves users datatbase in the file

        :param user_id: ID of the user
        :type user_id: int

        :param prescription_id: ID of the prescription
        :type prescription_id: int
        '''
        user = self.users().get(user_id)
        if not user:
            raise UserDoesNotExistError(user_id)
        user.remove_prescription(prescription_id)

        self.save_users_data()

    def add_prescription(self, user_id: int, medicine_name: str,
                         dosage: int, weekday: int):
        '''
        Adds prescription to the user with given ID
            and saves users datatbase in the file

        :param user_id: ID of the user
        :type user_id: int

        :param prescription: Prescription that is to be added
        :type prescription: int
        '''
        user = self.users().get(user_id)
        if not user:
            raise UserDoesNotExistError(user_id)
        # Choose ID
        prescription_id = 0
        while prescription_id in user.prescriptions().keys():
            prescription_id += 1
        prescription = Prescription(id=prescription_id,
                                    medicine_name=medicine_name,
                                    dosage=dosage,
                                    weekday=weekday)
        user.add_prescription(prescription)

        self.save_users_data()

    def change_prescription(self, user_id: int, prescription_id: int,
                            medicine_name: str, dosage: int, weekday: int):
        '''
        Replaces prescription with given ID in the user with given ID
            with a new prescription, created with passed data
            and saves users datatbase in the file

        :param user_id: ID of the user
        :type user_id: int

        :param prescription_id: ID of the prescription
        :type prescription_id: int

        :param medicine_name: Name of the prescribed medicine
        :type medicine_name: str

        :param dosage: how many doses of the medicine should the user take
        :type dosage: int

        :param weekday: what day should the user take the medicine. Number from 1 to 7
        :type weekday: int
        '''
        user = self.users().get(user_id)
        if not user:
            return UserDoesNotExistError(user_id)
        new_prescription = Prescription(id=prescription_id,
                                        medicine_name=medicine_name,
                                        dosage=dosage,
                                        weekday=weekday)
        user.remove_prescription(prescription_id)
        user.add_prescription(new_prescription)

        self.save_users_data()
