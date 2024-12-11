from medihelp.users_database import UsersDatabase
from medihelp.user import User
from medihelp.prescription import Prescription
from medihelp.errors import MalformedDataError
from datetime import date
from io import StringIO
from pytest import raises


def test_usersdatabase_create():
    database = UsersDatabase()
    assert database.users() == {0: None, 1: None, 2: None}


def test_usersdatabase_write_to_file_and_read_from_file():
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

    # Create database
    database = UsersDatabase()
    database._add_user(user0)
    database._add_user(user1)
    database._add_user(user2)

    # Write database
    data = ""
    file = StringIO(data)
    database.write_to_file(file)
    data = file.getvalue()

    # Read database
    file = StringIO(data)
    database.__init__()
    database.read_from_file(file)

    assert database.users()[0] == user0
    assert database.users()[1] == user1
    assert database.users()[2] == user2


def test_usersdatabase_read_from_file_malformed_data_wrong_format():
    data = 'Malformed file'
    file = StringIO(data)
    file.name = 'file'
    database = UsersDatabase()
    with raises(MalformedDataError):
        database.read_from_file(file)


def test_usersdatabase_read_from_file_malformed_data_wrong_id():
    data = '''
[
{
        "id": 4,
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
    }
]
'''
    file = StringIO(data)
    file.name = 'file'
    database = UsersDatabase()
    with raises(MalformedDataError):
        database.read_from_file(file)


def test_usersdatabase_read_from_file_malformed_data_attribute_missing():
    data = '''
[
{
        "id": 0,
        "name": "Dad",
        "birth_date": "1982-07-12",
        "illnesses": [
            "cold",
            "xyz"
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
    }
]
'''
    file = StringIO(data)
    file.name = 'file'
    database = UsersDatabase()
    with raises(MalformedDataError):
        database.read_from_file(file)
