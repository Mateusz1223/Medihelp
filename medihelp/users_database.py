from medihelp.user import User
import json
from medihelp.errors import MalformedDataError, IdAlreadyInUseError, InvalidUserIDError
from datetime import date
from medihelp.prescription import Prescription


class UsersDatabase:
    '''
    Loads from a file and stores exactly 3 instances of User in a dictionary. Id of the user being the key and must range from 0 to 2.

    Attributes
    ----------
    :ivar _users: Dictionary contianing three instances of User. Id of the user being the key and must range from 0 to 2.
    :vartype _users: dict[int User]
    '''

    def __init__(self):
        self._users = {0: None, 1: None, 2: None}

    def users(self):
        return self._users

    def _add_user(self, user):
        '''
        This method adds user to self._users and makes sure the id stays in the range from 0 to 2
        '''
        if user.id() < 0 or user.id() > 2:
            raise InvalidUserIDError
        if self._users[user.id()] is not None:
            raise IdAlreadyInUseError
        self._users[user.id()] = user

    def read_from_file(self, file_handler):
        '''
        Reads informations about users from a .json file
        '''
        try:
            data = json.load(file_handler)
        except Exception:
            raise MalformedDataError(file_handler.name, 0)
        item_counter = 1
        for item in data:
            try:
                id = item['id']
                name = item['name']
                year, month, day = map(int, item['birth_date'].split('-'))
                birth_date = date(year, month, day)
                illnesses = item['illnesses']
                allergies = item['allergies']
                prescriptions = []
                for pres_set in item['prescriptions']:
                    prescription = Prescription(medicine_name=pres_set['medicine_name'],
                                                dosage=pres_set['dosage'],
                                                weekday=pres_set['weekday'])
                    prescriptions.append(prescription)
                self._add_user(User(id, name, birth_date, illnesses, allergies, prescriptions))
                item_counter += 1
            except Exception:
                raise MalformedDataError(file_handler.name, item_counter)

    def write_to_file(self, file_handler):
        '''
        Saves informations about users into a .json file
        '''
        data = []
        for user in self._users.values():
            prescriptions = []
            for prescription in user.prescriptions():
                prescriptions.append({
                    'medicine_name': prescription.medicine_name(),
                    'dosage': prescription.dosage(),
                    'weekday': prescription.weekday(),
                })
            data.append({
                'id': user.id(),
                'name': user.name(),
                'birth_date': str(user.birth_date()),
                'illnesses': list(user.illnesses()),
                'allergies': list(user.allergies()),
                'prescriptions': prescriptions,
            })
        json.dump(data, file_handler, indent=4)
