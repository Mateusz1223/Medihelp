from medihelp.system import System
from medihelp.medicine import Medicine
from medihelp.prescription import Prescription
from medihelp.user import User
from medihelp.errors import (DataLoadingError,
                             NoFileOpenedError,
                             MedicineDoesNotExist,
                             UserDoesNotExist)
from pytest import raises
from io import StringIO
import builtins
from datetime import date


def test_system_create():
    system = System()
    system.medicines_database()
    system.users_database()
    assert system.medicines_file_path() is None
    assert system.medicines_file_saved()


def test_system_medicines_database_loaded_true():
    system = System()
    assert not system.medicines_database_loaded()


def test_system_load_users_data(monkeypatch):
    # Create users
    prescriptions_set0 = {
        Prescription(medicine_name='med1', dosage=1, weekday=2),
        Prescription(medicine_name='med2', dosage=2, weekday=7)
    }
    user0 = User(0,
                 name='Dad',
                 birth_date=date(1982, 7, 12),
                 illnesses={'xyz', 'cold'},
                 allergies={'nicotine', 'sugar'},
                 prescriptions=prescriptions_set0)
    user1 = User(1,
                 name='Mom',
                 birth_date=date(1985, 8, 4),
                 illnesses={'xyz', 'illness2', 'illnes3'},
                 allergies={'weed', 'stuff'})
    prescriptions_set2 = {
        Prescription(medicine_name='med3', dosage=3, weekday=4),
    }
    user2 = User(2,
                 name='Child',
                 birth_date=date(2018, 1, 2),
                 illnesses={'diabetes'},
                 allergies={'this', 'that'},
                 prescriptions=prescriptions_set2)

    # Create fake file
    data = '''[
    {
        "id": 0,
        "name": "Dad",
        "birth_date": "1982-07-12",
        "illnesses": [
            "cold",
            "xyz"
        ],
        "allergies": [
            "nicotine",
            "sugar"
        ],
        "prescriptions": [
            {
                "medicine_name": "Med2",
                "dosage": 2,
                "weekday": 7
            },
            {
                "medicine_name": "Med1",
                "dosage": 1,
                "weekday": 2
            }
        ]
    },
    {
        "id": 1,
        "name": "Mom",
        "birth_date": "1985-08-04",
        "illnesses": [
            "illness2",
            "xyz",
            "illnes3"
        ],
        "allergies": [
            "weed",
            "stuff"
        ],
        "prescriptions": []
    },
    {
        "id": 2,
        "name": "Child",
        "birth_date": "2018-01-02",
        "illnesses": [
            "diabetes"
        ],
        "allergies": [
            "that",
            "this"
        ],
        "prescriptions": [
            {
                "medicine_name": "Med3",
                "dosage": 3,
                "weekday": 4
            }
        ]
    }
]
'''
    file = StringIO(data)

    def fake_open(path, mode):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    system.load_users_data()
    assert system.users_database().users()[0] == user0
    assert system.users_database().users()[1] == user1
    assert system.users_database().users()[2] == user2


def test_system_load_users_data_error(monkeypatch):
    # Create fake file
    data = 'Malformed data'
    file = StringIO(data)

    def fake_open(path, mode):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    with raises(DataLoadingError):
        system.load_users_data()


def test_system_medicines_database_loaded(monkeypatch):
    # Create fake file
    data = '''id,name,manufacturer,illnesses,recipients,substances,recommended_age,doses,doses_left,expiration_date,notes
0,Ivermectin,Polfarm,"{'illness2', 'illness3', 'illness1'}","{0, 1, 2}","{'caffeine', 'nicotine'}",0,10,6,2025-12-31,"[None, 'Hello World1', None]"'''
    file = StringIO(data)

    def fake_open(path, mode):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    assert not system.medicines_database_loaded()
    system.load_medicines_database_from('whatever_path')
    assert system.medicines_database_loaded()


def test_system_medicines_database_loaded_false(monkeypatch):
    data = '''id,name,manufacturer,illnesses,recipients,substances,recommended_age,doses,doses_left,expiration_date,notes
0,Ivermectin,Polfarm,"{'illness2', 'illness3', 'illness1'}","{0, 1, 2}","{'caffeine', 'nicotine'}",0,10,6,2025-12-31,"[None, 'Hello World1', None]"
1,Paracetamol,Usdrugs,{'cold'},{0},"{'weed', 'stuff'}",12,5,5,2026-01-03,"[None, None, None]"
'''
    file = StringIO(data)

    def fake_open(path, mode):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    system.load_medicines_database_from('whatever_path')
    assert system.medicines_database_loaded()


def test_system_load_medicines_database_from(monkeypatch):
    medicine1 = Medicine(0, name='Ivermectin', manufacturer='polfarm',
                         illnesses=['Illness1', 'illness2', 'IllNess3'],
                         substances=['nicoTine', 'Caffeine'],
                         recommended_age=0, doses=10, doses_left=6, expiration_date=date(2025, 12, 31), recipients=[0, 1, 2])
    medicine1.set_note(1, "Hello World1")
    medicine2 = Medicine(1, name='Paracetamol', manufacturer='usdrugs',
                         illnesses=['cold'], substances=['weed', 'stuff'],
                         recommended_age=12, doses=5, doses_left=5, expiration_date=date(2026, 1, 3), recipients=[0])

    data = '''id,name,manufacturer,illnesses,recipients,substances,recommended_age,doses,doses_left,expiration_date,notes
0,Ivermectin,Polfarm,"{'illness2', 'illness3', 'illness1'}","{0, 1, 2}","{'caffeine', 'nicotine'}",0,10,6,2025-12-31,"{1: 'Hello World1'}"
1,Paracetamol,Usdrugs,{'cold'},{0},"{'weed', 'stuff'}",12,5,5,2026-01-03,"{}"
'''
    file = StringIO(data)

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    system.load_medicines_database_from('whatever_path')
    assert system.medicines_database_loaded()
    assert medicine1 in system.medicines_database().medicines().values()
    assert medicine2 in system.medicines_database().medicines().values()


def test_system_medicines_database_loaded_false_error(monkeypatch):
    data = '''Malformed data\nMalformed data'''
    file = StringIO(data)

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    with raises(DataLoadingError):
        system.load_medicines_database_from('whatever_path')


def test_system_save_medicines_database_no_file_opened(monkeypatch):
    system = System()
    with raises(NoFileOpenedError):
        system.save_medicines_database()


def test_system_save_medicines_database_1(monkeypatch):
    data = ''
    file = StringIO(data)

    def fake_open(path, mode):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    # passing a path to the file so that it doesn't rise NoFileOpenedError
    system.save_medicines_database('what-ever-path')


def test_system_save_medicines_database_2(monkeypatch):
    data = ''
    file = StringIO(data)

    def fake_open(path, mode):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    system.load_medicines_database_from('whatever-path')  # to open a file so that it doesn't rise NoFileOpenedError

    data = ''
    file = StringIO(data)

    def fake_open(path, mode):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system.save_medicines_database()


def test_system_set_note_typical():
    user = User(0,
                name='Dad',
                birth_date=date(1982, 7, 12),
                illnesses={'xyz', 'cold'},
                allergies={'nicotine', 'sugar'},
                prescriptions={})
    medicine = Medicine(1, name='Ivermectin', manufacturer='polfarm',
                        illnesses=['Illness1', 'illness2', 'IllNess3'],
                        substances=['nicoTine', 'Caffeine'],
                        recommended_age=0, doses=10, doses_left=6,
                        expiration_date=date(2025, 12, 31),
                        recipients=[0, 1, 2],
                        notes={})

    system = System()
    system.users_database()._add_user(user)
    system.medicines_database().add_medicine(medicine)

    assert medicine.notes() == {}
    system.set_note(1, 0, "Hello!")
    assert medicine.note(0) == "Hello!"


def test_system_set_note_wrong_medicine_id():
    user = User(0,
                name='Dad',
                birth_date=date(1982, 7, 12),
                illnesses={'xyz', 'cold'},
                allergies={'nicotine', 'sugar'},
                prescriptions={})
    medicine = Medicine(1, name='Ivermectin', manufacturer='polfarm',
                        illnesses=['Illness1', 'illness2', 'IllNess3'],
                        substances=['nicoTine', 'Caffeine'],
                        recommended_age=0, doses=10, doses_left=6,
                        expiration_date=date(2025, 12, 31),
                        recipients=[0, 1, 2],
                        notes={})

    system = System()
    system.users_database()._add_user(user)
    system.medicines_database().add_medicine(medicine)

    with raises(MedicineDoesNotExist):
        system.set_note(-100, 0, "hello")


def test_system_set_note_wrong_user_id():
    user = User(0,
                name='Dad',
                birth_date=date(1982, 7, 12),
                illnesses={'xyz', 'cold'},
                allergies={'nicotine', 'sugar'},
                prescriptions={})
    medicine = Medicine(1, name='Ivermectin', manufacturer='polfarm',
                        illnesses=['Illness1', 'illness2', 'IllNess3'],
                        substances=['nicoTine', 'Caffeine'],
                        recommended_age=0, doses=10, doses_left=6,
                        expiration_date=date(2025, 12, 31),
                        recipients=[0, 1, 2],
                        notes={})

    system = System()
    system.users_database()._add_user(user)
    system.medicines_database().add_medicine(medicine)

    with raises(UserDoesNotExist):
        system.set_note(1, -100, "hello")


def test_system_del_note_typical():
    user = User(0,
                name='Dad',
                birth_date=date(1982, 7, 12),
                illnesses={'xyz', 'cold'},
                allergies={'nicotine', 'sugar'},
                prescriptions={})
    medicine = Medicine(1, name='Ivermectin', manufacturer='polfarm',
                        illnesses=['Illness1', 'illness2', 'IllNess3'],
                        substances=['nicoTine', 'Caffeine'],
                        recommended_age=0, doses=10, doses_left=6,
                        expiration_date=date(2025, 12, 31),
                        recipients=[0, 1, 2],
                        notes={0: 'Hello!'})

    system = System()
    system.users_database()._add_user(user)
    system.medicines_database().add_medicine(medicine)

    assert medicine.note(0) == "Hello!"
    system.del_note(1, 0)
    assert medicine.notes() == {}


def test_system_del_note_wrong_user_id():
    user = User(0,
                name='Dad',
                birth_date=date(1982, 7, 12),
                illnesses={'xyz', 'cold'},
                allergies={'nicotine', 'sugar'},
                prescriptions={})
    medicine = Medicine(1, name='Ivermectin', manufacturer='polfarm',
                        illnesses=['Illness1', 'illness2', 'IllNess3'],
                        substances=['nicoTine', 'Caffeine'],
                        recommended_age=0, doses=10, doses_left=6,
                        expiration_date=date(2025, 12, 31),
                        recipients=[0, 1, 2],
                        notes={0: 'Hello!'})

    system = System()
    system.users_database()._add_user(user)
    system.medicines_database().add_medicine(medicine)

    with raises(UserDoesNotExist):
        system.del_note(1, -100)


def test_system_del_note_wrong_medicine_id():
    user = User(0,
                name='Dad',
                birth_date=date(1982, 7, 12),
                illnesses={'xyz', 'cold'},
                allergies={'nicotine', 'sugar'},
                prescriptions={})
    medicine = Medicine(1, name='Ivermectin', manufacturer='polfarm',
                        illnesses=['Illness1', 'illness2', 'IllNess3'],
                        substances=['nicoTine', 'Caffeine'],
                        recommended_age=0, doses=10, doses_left=6,
                        expiration_date=date(2025, 12, 31),
                        recipients=[0, 1, 2],
                        notes={0: 'Hello!'})

    system = System()
    system.users_database()._add_user(user)
    system.medicines_database().add_medicine(medicine)

    with raises(MedicineDoesNotExist):
        system.del_note(-100, 0)
