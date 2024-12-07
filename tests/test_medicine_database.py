from medihelp.medicine_database import MedicineDatabase
from medihelp.medicine import Medicine
from datetime import date
from io import StringIO


def test_medicinedatabase_create():
    database = MedicineDatabase()
    assert database.medicines() == []


def test_medicinedatabase_add_medicine():
    database = MedicineDatabase()
    assert database.medicines() == []

    illneses1 = ['Illness1', 'illness2', 'IllNess3']
    substances1 = ['nicoTine', 'Caffeine']
    date_instance1 = date(2025, 12, 31)
    medicine1 = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                         illnesses=illneses1, substances=substances1,
                         recommended_age=0, doses=10, doses_left=10, expiration_date=date_instance1, recipients=[0, 1, 2])
    database.add_medicine(medicine1)

    assert database.medicines() == [medicine1]


def test_medicinedatabase_delete_medicine():
    database = MedicineDatabase()

    illneses1 = ['Illness1', 'illness2', 'IllNess3']
    substances1 = ['nicoTine', 'Caffeine']
    date_instance1 = date(2025, 12, 31)
    medicine1 = Medicine(0, name='Ivermectin', manufacturer='polfarm',
                         illnesses=illneses1, substances=substances1,
                         recommended_age=0, doses=10, doses_left=6, expiration_date=date_instance1, recipients=[0, 1, 2])
    medicine1.set_note(1, "Hello World1")
    illneses2 = ['cold']
    substances2 = ['weed', 'stuff']
    date_instance2 = date(2026, 1, 3)
    medicine2 = Medicine(1, name='Paracetamol', manufacturer='usdrugs',
                         illnesses=illneses2, substances=substances2,
                         recommended_age=12, doses=5, doses_left=5, expiration_date=date_instance2, recipients=[0])
    database.add_medicine(medicine1)
    database.add_medicine(medicine2)

    assert database.medicines() == [medicine1, medicine2]
    database.delete_medicine(1)
    assert database.medicines() == [medicine1]


def test_medicinedatabase_write_to_file():
    database = MedicineDatabase()

    illneses1 = ['Illness1', 'illness2', 'IllNess3']
    substances1 = ['nicoTine', 'Caffeine']
    date_instance1 = date(2025, 12, 31)
    medicine1 = Medicine(0, name='Ivermectin', manufacturer='polfarm',
                         illnesses=illneses1, substances=substances1,
                         recommended_age=0, doses=10, doses_left=6, expiration_date=date_instance1, recipients=[0, 1, 2])
    medicine1.set_note(1, "Hello World1")
    illneses2 = ['cold']
    substances2 = ['weed', 'stuff']
    date_instance2 = date(2026, 1, 3)
    medicine2 = Medicine(1, name='Paracetamol', manufacturer='usdrugs',
                         illnesses=illneses2, substances=substances2,
                         recommended_age=12, doses=5, doses_left=5, expiration_date=date_instance2, recipients=[0])

    database.add_medicine(medicine1)
    database.add_medicine(medicine2)

    data = ''
    file_handler = StringIO(data)
    database.write_to_file(file_handler)

    database.delete_medicine(0)
    database.delete_medicine(1)

    data = file_handler.getvalue()
    file_handler = StringIO(data)
    database.read_from_file(file_handler)
    assert database.medicines() == [medicine1, medicine2]


def test_medicinedatabase_read_from_file():
    database = MedicineDatabase()

    illneses1 = ['Illness1', 'illness2', 'IllNess3']
    substances1 = ['nicoTine', 'Caffeine']
    date_instance1 = date(2025, 12, 31)
    medicine1 = Medicine(0, name='Ivermectin', manufacturer='polfarm',
                         illnesses=illneses1, substances=substances1,
                         recommended_age=0, doses=10, doses_left=6, expiration_date=date_instance1, recipients=[0, 1, 2])
    medicine1.set_note(1, "Hello World1")
    illneses2 = ['cold']
    substances2 = ['weed', 'stuff']
    date_instance2 = date(2026, 1, 3)
    medicine2 = Medicine(1, name='Paracetamol', manufacturer='usdrugs',
                         illnesses=illneses2, substances=substances2,
                         recommended_age=12, doses=5, doses_left=5, expiration_date=date_instance2, recipients=[0])

    data = '''id,name,manufacturer,illnesses,recipients,substances,recommended_age,doses,doses_left,expiration_date,notes
0,Ivermectin,Polfarm,"{'illness2', 'illness3', 'illness1'}","{0, 1, 2}","{'caffeine', 'nicotine'}",0,10,6,2025-12-31,"[None, 'Hello World1', None]"
1,Paracetamol,Usdrugs,{'cold'},{0},"{'weed', 'stuff'}",12,5,5,2026-01-03,"[None, None, None]"'''
    file_handler = StringIO(data)
    database.read_from_file(file_handler)
    assert database.medicines() == [medicine1, medicine2]
