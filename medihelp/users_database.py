from medihelp.user import User
import json
from medihelp.errors import (MalformedDataError,
                             IdAlreadyInUseError,
                             NoSuchIdInTheDatabaseError)
from datetime import date
from medihelp.prescription import Prescription


class UsersDatabase:
    '''
    Stores a dictionary of users where IDs of those users are the keys.
        Provides methodes to load users database from a .json file and write it to a .json file

    Attributes
    ----------
    :ivar _users: Dictionary contianing instances of User.
    :vartype _users: dict[int User]
    '''

    def __init__(self):
        self._users = {}

    def users(self):
        return self._users

    def add_user(self, user):
        '''
        This method adds user to self._users
        '''
        if self.users().get(user.id()):
            raise IdAlreadyInUseError
        self._users[user.id()] = user

    def delete_user(self, id):
        if id not in self.users().keys():
            raise NoSuchIdInTheDatabaseError
        del self._users[id]

    def clear(self):
        '''
        Clears database
        '''
        self._users.clear()

    def read_from_file(self, file_handler):
        '''
        Reads informations about users from a .json file and adds them to _users
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
                    prescription = Prescription(id=pres_set['id'],
                                                medicine_name=pres_set['medicine_name'],
                                                dosage=pres_set['dosage'],
                                                weekday=pres_set['weekday'])
                    prescriptions.append(prescription)
                self.add_user(User(id, name, birth_date, illnesses, allergies, prescriptions))
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
            for prescription in user.prescriptions().values():
                prescriptions.append({
                    'id': prescription.id(),
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
