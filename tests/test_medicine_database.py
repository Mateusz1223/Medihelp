from medihelp.medicines_database import MedicinesDatabase
from medihelp.medicine import Medicine
from medihelp.errors import NoSuchIdInTheDatabaseError, IdAlreadyInUseError, MalformedDataError
from datetime import date
from io import StringIO
from pytest import raises


def test_medicinesdatabase_create():
    database = MedicinesDatabase()
    assert database.medicines() == {}


def test_medicinesdatabase_add_medicine():
    database = MedicinesDatabase()
    assert database.medicines() == {}
    date_instance1 = date(2025, 12, 31)
    medicine1 = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                         illnesses=['Illness1', 'illness2', 'IllNess3'],
                         substances=['nicoTine', 'Caffeine'],
                         recommended_age=0, doses=10, doses_left=10,
                         expiration_date=date_instance1, recipients=[0, 1, 2],
                         notes={0: "hello"})
    database.add_medicine(medicine1)

    assert medicine1 in database.medicines().values()
    assert medicine1.id() in database.medicines().keys()


def test_medicinesdatabase_add_medicine_id_already_in_use():
    database = MedicinesDatabase()
    date_instance1 = date(2025, 12, 31)
    medicine1 = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                         illnesses=['Illness1', 'illness2', 'IllNess3'],
                         substances=['nicoTine', 'Caffeine'],
                         recommended_age=0, doses=10, doses_left=10,
                         expiration_date=date_instance1, recipients=[0, 1, 2],
                         notes={0: "hello"})
    database.add_medicine(medicine1)
    with raises(IdAlreadyInUseError):
        database.add_medicine(medicine1)


def test_medicinesdatabase_delete_medicine_1():
    database = MedicinesDatabase()
    assert database.medicines() == {}

    illneses1 = ['Illness1', 'illness2', 'IllNess3']
    substances1 = ['nicoTine', 'Caffeine']
    date_instance1 = date(2025, 12, 31)
    medicine1 = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                         illnesses=illneses1, substances=substances1,
                         recommended_age=0, doses=10, doses_left=10,
                         expiration_date=date_instance1, recipients=[0, 1, 2],
                         notes={0: "hello"})
    database.add_medicine(medicine1)
    assert medicine1 in database.medicines().values()
    assert medicine1.id() in database.medicines().keys()

    database.delete_medicine(0)
    assert database.medicines() == {}


def test_medicinesdatabase_delete_medicine_wrong_id():
    database = MedicinesDatabase()
    assert database.medicines() == {}
    with raises(NoSuchIdInTheDatabaseError):
        database.delete_medicine(0)


def test_medicinesdatabase_write_to_file_read_from_file():
    database = MedicinesDatabase()
    date_instance1 = date(2025, 12, 31)
    medicine1 = Medicine(0, name='Ivermectin', manufacturer='polfarm',
                         illnesses=['Illness1', 'illness2', 'IllNess3'],
                         substances=['nicoTine', 'Caffeine'],
                         recommended_age=0, doses=10, doses_left=6,
                         expiration_date=date_instance1, recipients=[0, 1, 2],
                         notes={0: 'Note 1', 2: 'Note 2'})
    date_instance2 = date(2026, 1, 3)
    medicine2 = Medicine(1, name='Paracetamol', manufacturer='usdrugs',
                         illnesses=['cold'],
                         substances=['weed', 'stuff'],
                         recommended_age=12, doses=5, doses_left=5,
                         expiration_date=date_instance2, recipients=[0])

    database.add_medicine(medicine1)
    database.add_medicine(medicine2)

    data = ''
    file_handler = StringIO(data)
    database.write_to_file(file_handler)

    database.clear()

    data = file_handler.getvalue()
    file_handler = StringIO(data)
    database.read_from_file(file_handler)
    assert medicine1 in database.medicines().values()
    assert medicine1.id() in database.medicines().keys()
    assert medicine2 in database.medicines().values()
    assert medicine2.id() in database.medicines().keys()


def test_medicinesdatabase_read_from_file():
    database = MedicinesDatabase()
    date_instance1 = date(2025, 12, 31)
    medicine1 = Medicine(0, name='Ivermectin', manufacturer='polfarm',
                         illnesses=['Illness1', 'illness2', 'IllNess3'],
                         substances=['nicoTine', 'Caffeine'],
                         recommended_age=0, doses=10, doses_left=6,
                         expiration_date=date_instance1, recipients=[0, 1, 2],
                         notes={1: "Hello World1"})
    date_instance2 = date(2026, 1, 3)
    medicine2 = Medicine(1, name='Paracetamol', manufacturer='usdrugs',
                         illnesses=['cold'],
                         substances=['weed', 'stuff'],
                         recommended_age=12, doses=5, doses_left=5,
                         expiration_date=date_instance2, recipients=[0])

    data = '''id,name,manufacturer,illnesses,recipients,substances,recommended_age,doses,doses_left,expiration_date,notes
0,Ivermectin,Polfarm,"{'illness2', 'illness3', 'illness1'}","{0, 1, 2}","{'caffeine', 'nicotine'}",0,10,6,2025-12-31,"{1: 'Hello World1'}"
1,Paracetamol,Usdrugs,{'cold'},{0},"{'weed', 'stuff'}",12,5,5,2026-01-03,"{}"'''
    file_handler = StringIO(data)
    database.read_from_file(file_handler)
    assert medicine1 in database.medicines().values()
    assert medicine1.id() in database.medicines().keys()
    assert medicine2 in database.medicines().values()
    assert medicine2.id() in database.medicines().keys()


def test_medicinesdatabase_read_from_file_malformed_data_wrong_format():
    database = MedicinesDatabase()
    data = '''Malformed header\nMalformed row'''
    file_handler = StringIO(data)
    file_handler.name = 'file'
    with raises(MalformedDataError):
        database.read_from_file(file_handler)


def test_medicinesdatabase_read_from_file_malformed_incorrect_row_empty_name():
    database = MedicinesDatabase()
    data = '''id,name,manufacturer,illnesses,recipients,substances,recommended_age,doses,doses_left,expiration_date,notes
0,,Polfarm,"{'illness2', 'illness3', 'illness1'}","{0, 1, 2}","{'caffeine', 'nicotine'}",0,10,6,2025-12-31,"[None, 'Hello World1', None]'''
    file_handler = StringIO(data)
    file_handler.name = 'file'
    with raises(MalformedDataError):
        database.read_from_file(file_handler)
