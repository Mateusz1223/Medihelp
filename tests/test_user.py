from medihelp.user import User
from medihelp.prescription import Prescription
from pytest import raises
from medihelp.errors import InvalidNameError, InvalidAgeError


def test_user_create_no_lists():
    user = User(name='Dad', age=43)
    assert user.name() == 'Dad'
    assert user.age() == 43
    assert user.illnesses() == []
    assert user.allergies() == []
    assert user.prescriptions() == []


def test_user_create_with_lists():
    illnesses_list = ['xyz', 'illness2', 'illnes3']
    allergies_list = ['nicotine', 'sugar']
    prescriptions_list = [
        Prescription(medicine_name='med1', dosage=1, weekday=2),
        Prescription(medicine_name='med2', dosage=2, weekday=7)
    ]
    user = User(name='Dad', age=43, illnesses=illnesses_list, allergies=allergies_list, prescriptions=prescriptions_list)
    assert user.name() == 'Dad'
    assert user.age() == 43
    assert user.illnesses() == illnesses_list
    assert user.allergies() == allergies_list
    assert user.prescriptions() == prescriptions_list


def test_user_set_name_typical():
    user = User(name='Dad', age=43)
    assert user.name() == 'Dad'
    user.set_name('Mom')
    assert user.name() == 'Mom'


def test_user_set_name_lowercase():
    user = User(name='Dad', age=43)
    assert user.name() == 'Dad'
    user.set_name('mom')
    assert user.name() == 'Mom'


def test_user_set_name_empty_name():
    user = User(name='Dad', age=43)
    assert user.name() == 'Dad'
    with raises(InvalidNameError):
        user.set_name('')


def test_user_set_age_typical():
    user = User(name='Dad', age=43)
    assert user.age() == 43
    user.set_age(35)
    assert user.age() == 35


def test_user_set_age_zero():
    user = User(name='Dad', age=43)
    assert user.age() == 43
    user.set_age(0)
    assert user.age() == 0


def test_user_set_age_negative():
    user = User(name='Dad', age=43)
    assert user.age() == 43
    with raises(InvalidAgeError):
        user.set_age(-1)


def test_user_add_illness_typical():
    user = User(name='Dad', age=43)
    assert user.illnesses() == []
    user.add_illness('illness1')
    assert user.illnesses() == ['illness1']
    user.add_illness('illness2')
    assert user.illnesses() == ['illness1', 'illness2']


def test_user_add_illness_uppercase():
    user = User(name='Dad', age=43)
    assert user.illnesses() == []
    user.add_illness('illNess1')
    assert user.illnesses() == ['illness1']
    user.add_illness('Illness2')
    assert user.illnesses() == ['illness1', 'illness2']


def test_user_add_illness_empty_name():
    user = User(name='Dad', age=43)
    assert user.illnesses() == []
    with raises(InvalidNameError):
        user.add_illness('')


def test_user_remove_illness_typical():
    user = User(name='Dad', age=43, illnesses=['illness1', 'illness2'])
    assert user.illnesses() == ['illness1', 'illness2']
    user.remove_illness('illness1')
    assert user.illnesses() == ['illness2']
    user.remove_illness('illness2')
    assert user.illnesses() == []
