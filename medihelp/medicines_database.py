from .medicine import Medicine
from .errors import MalformedDataError, IdAlreadyInUseError, NoSuchIdInTheDatabaseError
from datetime import date
import csv
import ast


class MedicinesDatabase:
    '''
    Stores a dictionary of medicines where IDs of those medicines are the keys.
        Provides methodes to load medicines database from a .csv file and write it to a .file file

    Atributes
    ---------
    :ivar _medicines: Dictionary with all medicines registered in the system. Id of the medicine being the key.
    :vartype _medicines: dict[int, Medicine]
    '''

    def __init__(self):
        self._medicines = {}

    def medicines(self):
        return self._medicines

    def add_medicine(self, medicine):
        if type(medicine) is not Medicine:
            raise ValueError('Medicine object must be given')
        if medicine.id() in self.medicines().keys():
            raise IdAlreadyInUseError
        self._medicines.update({medicine.id(): medicine})

    def delete_medicine(self, id):
        if id not in self.medicines().keys():
            raise NoSuchIdInTheDatabaseError
        del self._medicines[id]

    def clear(self):
        self._medicines.clear()

    def read_from_file(self, file_handler):
        '''
        Reads medicine database from a .csv file
        '''
        try:
            reader = csv.DictReader(file_handler)
        except csv.Error as e:
            raise MalformedDataError(file_handler.name, 1) from e
        row_counter = 2
        try:
            for row in reader:
                # Create instance of Medicine
                try:
                    year, month, day = map(int, row['expiration_date'].split('-'))
                    medicine = Medicine(
                        id=int(row['id']),
                        name=row['name'],
                        manufacturer=row['manufacturer'],
                        illnesses=ast.literal_eval(row['illnesses']),
                        substances=ast.literal_eval(row['substances']),
                        recommended_age=int(row['recommended_age']),
                        doses=int(row['doses']),
                        doses_left=int(row['doses_left']),
                        expiration_date=date(year, month, day),
                        recipients=ast.literal_eval(row['recipients']),
                        notes=ast.literal_eval(row['notes'])
                    )
                    self.add_medicine(medicine)
                except Exception as e:
                    raise MalformedDataError(file_handler.name, row_counter) from e

                row_counter += 1
        except csv.Error as e:
            raise MalformedDataError(file_handler.name, row_counter) from e

    def write_to_file(self, file_handler):
        '''
        Saves medicine database into a .csv file
        '''
        header = [
            'id',
            'name',
            'manufacturer',
            'illnesses',
            'recipients',
            'substances',
            'recommended_age',
            'doses',
            'doses_left',
            'expiration_date',
            'notes'
        ]
        writer = csv.DictWriter(file_handler, fieldnames=header, lineterminator='\n')
        writer.writeheader()
        for medicine in sorted(self.medicines().values(), key=lambda x: x.id()):
            writer.writerow({
                'id': medicine.id(),
                'name': medicine.name(),
                'manufacturer': medicine.manufacturer(),
                'illnesses': medicine.illnesses(),
                'recipients': medicine.recipients(),
                'substances': medicine.substances(),
                'recommended_age': medicine.recommended_age(),
                'doses': medicine.doses(),
                'doses_left': medicine.doses_left(),
                'expiration_date': medicine.expiration_date(),
                'notes': medicine.notes()
            })
