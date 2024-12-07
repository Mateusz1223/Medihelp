from .medicine import Medicine
from .errors import MalformedDataError
from datetime import date
import csv
import ast


class MedicineDatabase:
    '''
    Class that stores a list of all medicines registered in the system.
    Can load the list from .csv file
    Can store the list in .csv file

    Atributes
    ---------
    :ivar _medicines: List of all medicines registered in the system
    :vartype _medicines: list[Medicine]
    '''

    def __init__(self):
        self._medicines = []

    def medicines(self):
        return self._medicines

    def add_medicine(self, medicine):
        if type(medicine) is not Medicine:
            raise ValueError('Medicine object must be given')
        self._medicines.append(medicine)

    def delete_medicine(self, id):
        to_delete = None
        for medicine in self.medicines():
            if medicine.id() == id:
                to_delete = medicine
                break
        self._medicines.remove(to_delete)

    def read_from_file(self, file_handler):
        try:
            reader = csv.DictReader(file_handler)
        except csv.Error as e:
            raise MalformedDataError(1) from e
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
                        recipients=ast.literal_eval(row['recipients'])
                    )
                    notes = ast.literal_eval(row['notes'])
                    for i in range(0, len(notes)):
                        if notes[i] == 'None':
                            notes[i] = None
                    medicine.set_note(0, notes[0])
                    medicine.set_note(1, notes[1])
                    medicine.set_note(2, notes[2])

                    self.add_medicine(medicine)
                except Exception as e:
                    raise MalformedDataError(row_counter) from e

                row_counter += 1
        except csv.Error as e:
            raise MalformedDataError(row_counter) from e

    def write_to_file(self, file_handler):
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
        for medicine in self.medicines():
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
                'notes': [medicine.note(0), medicine.note(1), medicine.note(2)]
            })
