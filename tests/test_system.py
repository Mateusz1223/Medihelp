from medihelp.system import System
from medihelp.medicine import Medicine
from medihelp.prescription import Prescription
from medihelp.users_database import UsersDatabase
from medihelp.user import User
from medihelp.errors import (DataLoadingError,
                             NoFileOpenedError,
                             MedicineDoesNotExistError,
                             UserDoesNotExistError)
from datetime import date
from pytest import raises
from io import StringIO
import builtins


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
        Prescription(id=0, medicine_name='med1', dosage=1, weekday=2),
        Prescription(id=1, medicine_name='med2', dosage=2, weekday=7)
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
        Prescription(id=0, medicine_name='med3', dosage=3, weekday=4),
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
                "id": 1,
                "medicine_name": "Med2",
                "dosage": 2,
                "weekday": 7
            },
            {
                "id": 0,
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
                "id": 0,
                "medicine_name": "Med3",
                "dosage": 3,
                "weekday": 4
            }
        ]
    }
]
'''
    file = StringIO(data)

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    system.load_users_data()
    assert system.users_database().users()[0] == user0
    assert system.users_database().users()[1] == user1
    assert system.users_database().users()[2] == user2


def test_system_save_users_data_typical(monkeypatch):
    file = StringIO()

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    # Create users
    prescriptions_set0 = {
        Prescription(id=0, medicine_name='med1', dosage=1, weekday=2),
        Prescription(id=1, medicine_name='med2', dosage=2, weekday=7)
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
        Prescription(id=0, medicine_name='med3', dosage=3, weekday=4),
    }
    user2 = User(2,
                 name='Child',
                 birth_date=date(2018, 1, 2),
                 illnesses={'diabetes'},
                 allergies={'this', 'that'},
                 prescriptions=prescriptions_set2)

    database = UsersDatabase()
    database.add_user(user0)
    database.add_user(user1)
    database.add_user(user2)
    system = System()
    system._users_database = database
    assert 1


def test_system_load_users_data_error(monkeypatch):
    # Create fake file
    data = 'Malformed data'
    file = StringIO(data)

    def fake_open(path, mode, *args, **kwargs):
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

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    assert not system.medicines_database_loaded()
    system.load_medicines_database_from('whatever-path')
    assert system.medicines_file_path() == 'whatever-path'
    assert system.medicines_file_saved() is True
    assert system.medicines_database_loaded()


def test_system_medicines_database_loaded_false(monkeypatch):
    data = '''id,name,manufacturer,illnesses,recipients,substances,recommended_age,doses,doses_left,expiration_date,notes
0,Ivermectin,Polfarm,"{'illness2', 'illness3', 'illness1'}","{0, 1, 2}","{'caffeine', 'nicotine'}",0,10,6,2025-12-31,"[None, 'Hello World1', None]"
1,Paracetamol,Usdrugs,{'cold'},{0},"{'weed', 'stuff'}",12,5,5,2026-01-03,"[None, None, None]"
'''
    file = StringIO(data)

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    system.load_medicines_database_from('whatever-path')
    assert system.medicines_file_path() == 'whatever-path'
    assert system.medicines_file_saved() is True
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
    system.load_medicines_database_from('whatever-path')
    assert system.medicines_database_loaded()
    assert system.medicines_file_path() == 'whatever-path'
    assert system.medicines_file_saved() is True
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
        system.load_medicines_database_from('whatever-path')


def test_system_save_medicines_database_no_file_opened(monkeypatch):
    system = System()
    with raises(NoFileOpenedError):
        system.save_medicines_database()


def test_system_save_medicines_database_1(monkeypatch):
    data = ''
    file = StringIO(data)

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    system._medicines_file_saved = False
    # passing a path to the file so that it doesn't rise NoFileOpenedError
    system.save_medicines_database('whatever-path')
    assert system.medicines_file_path() == 'whatever-path'
    assert system.medicines_file_saved() is True


def test_system_save_medicines_database_2(monkeypatch):
    data = ''
    file = StringIO(data)

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    system.load_medicines_database_from('whatever-path')  # to open a file so that it doesn't rise NoFileOpenedError

    data = ''
    file = StringIO(data)

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system._medicines_file_saved = False
    system.save_medicines_database()
    assert system.medicines_file_saved() is True


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
    system.users_database().add_user(user)
    system.medicines_database().add_medicine(medicine)

    assert medicine.notes() == {}
    system._medicines_file_saved = True
    system.set_note(1, 0, "Hello!")
    assert medicine.note(0) == "Hello!"
    assert system.medicines_file_saved() is False


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
    system.users_database().add_user(user)
    system.medicines_database().add_medicine(medicine)

    with raises(MedicineDoesNotExistError):
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
    system.users_database().add_user(user)
    system.medicines_database().add_medicine(medicine)

    with raises(UserDoesNotExistError):
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
    system.users_database().add_user(user)
    system.medicines_database().add_medicine(medicine)

    assert medicine.note(0) == "Hello!"
    system._medicines_file_saved = True
    system.del_note(1, 0)
    assert system.medicines_file_saved() is False
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
    system.users_database().add_user(user)
    system.medicines_database().add_medicine(medicine)

    with raises(UserDoesNotExistError):
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
    system.users_database().add_user(user)
    system.medicines_database().add_medicine(medicine)

    with raises(MedicineDoesNotExistError):
        system.del_note(-100, 0)


def test_system_add_medicine():
    system = System()
    assert system.medicines_file_saved() is True

    id1 = system.add_medicine(name='Ivermectin', manufacturer='polfarm',
                              illnesses=['Illness1', 'illness2', 'IllNess3'],
                              substances=['nicoTine', 'Caffeine'],
                              recommended_age=0, doses=10, doses_left=6,
                              expiration_date=date(2025, 12, 31), recipients=[0, 1, 2],
                              notes={1: 'Hello'})
    medicine1 = Medicine(id=id1, name='Ivermectin', manufacturer='polfarm',
                         illnesses=['Illness1', 'illness2', 'IllNess3'],
                         substances=['nicoTine', 'Caffeine'],
                         recommended_age=0, doses=10, doses_left=6,
                         expiration_date=date(2025, 12, 31), recipients=[0, 1, 2],
                         notes={1: 'Hello'})
    id2 = system.add_medicine(name='Paracetamol', manufacturer='usdrugs',
                              illnesses=['cold'], substances=['weed', 'stuff'],
                              recommended_age=12, doses=5, doses_left=5,
                              expiration_date=date(2026, 1, 3), recipients=[0])
    medicine2 = Medicine(id=id2, name='Paracetamol', manufacturer='usdrugs',
                         illnesses=['cold'], substances=['weed', 'stuff'],
                         recommended_age=12, doses=5, doses_left=5,
                         expiration_date=date(2026, 1, 3), recipients=[0])

    assert system.medicines_file_saved() is False

    assert system.medicines()[id1] == medicine1
    assert system.medicines()[id2] == medicine2


def test_system_change_medicine_wrong_id():
    system = System()

    id = system.add_medicine(name='Ivermectin', manufacturer='polfarm',
                             illnesses=['Illness1', 'illness2', 'IllNess3'],
                             substances=['nicoTine', 'Caffeine'],
                             recommended_age=0, doses=10, doses_left=6,
                             expiration_date=date(2025, 12, 31), recipients=[0, 1, 2],
                             notes={1: 'Hello'})
    medicine = Medicine(id=id, name='Ivermectin', manufacturer='polfarm',
                        illnesses=['Illness1', 'illness2', 'IllNess3'],
                        substances=['nicoTine', 'Caffeine'],
                        recommended_age=0, doses=10, doses_left=6,
                        expiration_date=date(2025, 12, 31), recipients=[0, 1, 2],
                        notes={1: 'Hello'})
    assert system.medicines()[id] == medicine
    with raises(MedicineDoesNotExistError):
        system.change_medicine(medicine_id=id + 1, name='Paracetamol', manufacturer='usdrugs',
                               illnesses=['cold'], substances=['weed', 'stuff'],
                               recommended_age=12, doses=5, doses_left=5,
                               expiration_date=date(2026, 1, 3), recipients=[0])


def test_system_change_medicine_typical():
    system = System()

    id = system.add_medicine(name='Ivermectin', manufacturer='polfarm',
                             illnesses=['Illness1', 'illness2', 'IllNess3'],
                             substances=['nicoTine', 'Caffeine'],
                             recommended_age=0, doses=10, doses_left=6,
                             expiration_date=date(2025, 12, 31), recipients=[0, 1, 2],
                             notes={1: 'Hello'})
    medicine = Medicine(id=id, name='Ivermectin', manufacturer='polfarm',
                        illnesses=['Illness1', 'illness2', 'IllNess3'],
                        substances=['nicoTine', 'Caffeine'],
                        recommended_age=0, doses=10, doses_left=6,
                        expiration_date=date(2025, 12, 31), recipients=[0, 1, 2],
                        notes={1: 'Hello'})
    assert system.medicines()[id] == medicine

    system.change_medicine(medicine_id=id, name='Paracetamol', manufacturer='usdrugs',
                           illnesses=['cold'], substances=['weed', 'stuff'],
                           recommended_age=12, doses=5, doses_left=5,
                           expiration_date=date(2026, 1, 3), recipients=[0])
    medicine = Medicine(id=id, name='Paracetamol', manufacturer='usdrugs',
                        illnesses=['cold'], substances=['weed', 'stuff'],
                        recommended_age=12, doses=5, doses_left=5,
                        expiration_date=date(2026, 1, 3), recipients=[0],
                        notes={1: 'Hello'})
    assert system.medicines()[id] == medicine


def test_system_take_dose_typical():
    system = System()

    user = User(id=0,
                name='Dad',
                birth_date=date(1982, 7, 12),
                illnesses={'xyz', 'cold'},
                allergies={'sugar'},
                prescriptions=[])

    id = system.add_medicine(name='Ivermectin', manufacturer='polfarm',
                             illnesses=['Illness1', 'illness2', 'IllNess3'],
                             substances=['nicoTine', 'Caffeine'],
                             recommended_age=0, doses=10, doses_left=6,
                             expiration_date=date(2025, 12, 31), recipients=[0, 1, 2],
                             notes={1: 'Hello'})
    assert system.medicines()[id].doses_left() == 6
    system._medicines_file_saved = True
    system.take_dose(id, user)
    assert system.medicines()[id].doses_left() == 5
    assert system.medicines_file_saved() is False


def test_system_take_dose():
    system = System()

    user = User(id=0,
                name='Dad',
                birth_date=date(1982, 7, 12),
                illnesses={'xyz', 'cold'},
                allergies={'sugar'},
                prescriptions=[])

    id = system.add_medicine(name='Ivermectin', manufacturer='polfarm',
                             illnesses=['Illness1', 'illness2', 'IllNess3'],
                             substances=['nicoTine', 'Caffeine'],
                             recommended_age=0, doses=10, doses_left=6,
                             expiration_date=date(2025, 12, 31), recipients=[0, 1, 2],
                             notes={1: 'Hello'})

    with raises(MedicineDoesNotExistError):
        system.take_dose(id + 1, user)


def test_system_change_user_same_perscriptions(monkeypatch):
    # Very important, otherwise the test will override data/users.json file !!!
    file = StringIO()

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    user0 = User(id=0,
                 name='Dad',
                 birth_date=date(1982, 7, 12),
                 illnesses={'xyz', 'cold'},
                 allergies={'nicotine', 'sugar'},
                 prescriptions=[Prescription(id=0, medicine_name='med3', dosage=3, weekday=4)])
    user1 = User(id=0,
                 name='Mom',
                 birth_date=date(1985, 8, 4),
                 illnesses={'xyz', 'illness2', 'illnes3'},
                 allergies={'weed', 'stuff'},
                 prescriptions=[Prescription(id=0, medicine_name='med3', dosage=3, weekday=4)])

    database = UsersDatabase()
    database.add_user(user0)

    system = System()
    system._users_database = database

    assert system.users()[0] == user0

    system.change_user(user_id=0,
                       name='Mom',
                       birth_date=date(1985, 8, 4),
                       illnesses={'xyz', 'illness2', 'illnes3'},
                       allergies={'weed', 'stuff'},)
    assert system.users()[0] == user1


def test_system_change_user_not_the_same_perscriptions(monkeypatch):
    # Very important, otherwise the test will override data/users.json file !!!
    file = StringIO()

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)
    user0 = User(id=0,
                 name='Dad',
                 birth_date=date(1982, 7, 12),
                 illnesses={'xyz', 'cold'},
                 allergies={'nicotine', 'sugar'},
                 prescriptions=[Prescription(id=0, medicine_name='med3', dosage=3, weekday=4)])
    user1 = User(id=0,
                 name='Mom',
                 birth_date=date(1985, 8, 4),
                 illnesses={'xyz', 'illness2', 'illnes3'},
                 allergies={'weed', 'stuff'})

    database = UsersDatabase()
    database.add_user(user0)

    system = System()
    system._users_database = database

    assert system.users()[0] == user0

    system.change_user(user_id=0,
                       name='Mom',
                       birth_date=date(1985, 8, 4),
                       illnesses={'xyz', 'illness2', 'illnes3'},
                       allergies={'weed', 'stuff'})
    assert not system.users()[0] == user1


def test_system_change_user_wrong_id(monkeypatch):
    # Very important, otherwise the test will override data/users.json file !!!
    file = StringIO()

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    user0 = User(id=0,
                 name='Dad',
                 birth_date=date(1982, 7, 12),
                 illnesses={'xyz', 'cold'},
                 allergies={'nicotine', 'sugar'},
                 prescriptions=[Prescription(id=0, medicine_name='med3', dosage=3, weekday=4)])

    database = UsersDatabase()
    database.add_user(user0)

    system = System()
    system._users_database = database

    assert system.users()[0] == user0

    with raises(UserDoesNotExistError):
        system.change_user(user_id=1,
                           name='Mom',
                           birth_date=date(1985, 8, 4),
                           illnesses={'xyz', 'illness2', 'illnes3'},
                           allergies={'weed', 'stuff'})


def test_system_del_perscription(monkeypatch):
    # Very important, otherwise the test will override data/users.json file !!!
    file = StringIO()

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    presc0 = Prescription(id=0, medicine_name='med3', dosage=3, weekday=4)
    user0 = User(id=1,
                 name='Dad',
                 birth_date=date(1982, 7, 12),
                 illnesses={'xyz', 'cold'},
                 allergies={'nicotine', 'sugar'},
                 prescriptions=[presc0])

    database = UsersDatabase()
    database.add_user(user0)

    system = System()
    system._users_database = database
    assert system.users()[1].prescriptions()[0] == presc0
    system.del_prescription(1, 0)
    assert system.users()[1].prescriptions().get(0) is None


def test_system_del_perscription_wrong_user(monkeypatch):
    # Very important, otherwise the test will override data/users.json file !!!
    file = StringIO()

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    with raises(UserDoesNotExistError):
        system.del_prescription(1, 0)


def test_system_add_perscription_typical(monkeypatch):
    # Very important, otherwise the test will override data/users.json file !!!
    file = StringIO()

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    user0 = User(id=1,
                 name='Dad',
                 birth_date=date(1982, 7, 12),
                 illnesses={'xyz', 'cold'},
                 allergies={'nicotine', 'sugar'})

    database = UsersDatabase()
    database.add_user(user0)

    system = System()
    system._users_database = database

    assert system.users()[1].prescriptions().get(0) is None
    system.add_prescription(user_id=1, medicine_name='med3', dosage=3, weekday=4)

    file = StringIO()

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system.add_prescription(user_id=1, medicine_name='med1', dosage=1, weekday=2)
    presc0 = Prescription(id=0, medicine_name='med3', dosage=3, weekday=4)
    presc1 = Prescription(id=1, medicine_name='med1', dosage=1, weekday=2)
    assert system.users()[1].prescriptions()[0] == presc0
    assert system.users()[1].prescriptions()[1] == presc1


def test_system_add_perscription_wrong_user(monkeypatch):
    # Very important, otherwise the test will override data/users.json file !!!
    file = StringIO()

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    system = System()
    with raises(UserDoesNotExistError):
        system.add_prescription(user_id=1, medicine_name='med3', dosage=3, weekday=4)


def test_system_change_perscription_typical(monkeypatch):
    # Very important, otherwise the test will override data/users.json file !!!
    file = StringIO()

    def fake_open(path, mode, *args, **kwargs):
        return file
    monkeypatch.setattr(builtins, 'open', fake_open)

    presc = Prescription(id=0, medicine_name='med3', dosage=3, weekday=4)
    user0 = User(id=1,
                 name='Dad',
                 birth_date=date(1982, 7, 12),
                 illnesses={'xyz', 'cold'},
                 allergies={'nicotine', 'sugar'},
                 prescriptions=[presc])

    database = UsersDatabase()
    database.add_user(user0)

    system = System()
    system._users_database = database

    presc = Prescription(id=0, medicine_name='med3', dosage=3, weekday=4)
    assert system.users()[1].prescriptions()[0] == presc
    system.change_prescription(user_id=1, prescription_id=0,
                               medicine_name='new_name',
                               dosage=2, weekday=1)
    presc_new = Prescription(id=0, medicine_name='new_name', dosage=2, weekday=1)
    assert system.users()[1].prescriptions()[0] == presc_new
