from medihelp.user import User
from medihelp.prescription import Prescription
from pytest import raises
from medihelp.errors import (InvalidUserNameError,
                             InvalidIllnessNameError,
                             InvalidSubstanceNameError,
                             InvalidBirthdateError,
                             IdAlreadyInUseError,
                             NoSuchIdInUserPrescriptionsError)
from datetime import date


def test_user_create_no_lists():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.id() == 0
    assert user.name() == 'Dad'
    assert user.birth_date() == date(1980, 1, 2)
    assert user.illnesses() == set()
    assert user.allergies() == set()
    assert user.prescriptions() == {}


def test_user_create_with_lists():
    illnesses_set = {'xyz', 'illness2', 'illnes3'}
    allergies_set = {'nicotine', 'sugar'}
    presc0 = Prescription(id=0, medicine_name='med1', dosage=1, weekday=2)
    presc1 = Prescription(id=1, medicine_name='med2', dosage=2, weekday=7)
    user = User(1,
                name='Mom',
                birth_date=date(1980, 1, 2),
                illnesses={'xyz', 'illness2', 'illnes3'},
                allergies=allergies_set,
                prescriptions=[presc0, presc1])
    assert user.id() == 1
    assert user.name() == 'Mom'
    assert user.birth_date() == date(1980, 1, 2)
    assert user.illnesses() == illnesses_set
    assert user.allergies() == allergies_set
    assert user.prescriptions()[0] == presc0
    assert user.prescriptions()[1] == presc1


def test_user_set_name_typical():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.name() == 'Dad'
    user.set_name('Mom')
    assert user.name() == 'Mom'


def test_user_set_name_lowercase():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.name() == 'Dad'
    user.set_name('mom')
    assert user.name() == 'Mom'


def test_user_set_name_empty_name():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.name() == 'Dad'
    with raises(InvalidUserNameError):
        user.set_name('')


def test_user_set_name_all_white_spaces():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.name() == 'Dad'
    with raises(InvalidUserNameError):
        user.set_name('    \n  ')


def test_user_set_name_illegal_character_1():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.name() == 'Dad'
    with raises(InvalidUserNameError):
        user.set_name(',')


def test_user_set_name_illegal_character_2():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.name() == 'Dad'
    with raises(InvalidUserNameError):
        user.set_name("'")


def test_user_set_name_illegal_character_3():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.name() == 'Dad'
    with raises(InvalidUserNameError):
        user.set_name('"')


def test_user_set_name_empty_name_too_long():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.name() == 'Dad'
    with raises(InvalidUserNameError):
        user.set_name('01234567891234567')


def test_user_set_name_edge_case_1():
    user = User(0, name='0123456789123456', birth_date=date(1980, 1, 2))
    assert user.name() == '0123456789123456'


def test_user_set_name_edge_case_2():
    user = User(0, name='1', birth_date=date(1980, 1, 2))
    assert user.name() == '1'


def test_user_set_birth_date_typical():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.birth_date() == date(1980, 1, 2)
    user.set_birth_date(date(2000, 3, 4))
    assert user.birth_date() == date(2000, 3, 4)


def test_user_set_birth_date_future():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.birth_date() == date(1980, 1, 2)
    with raises(InvalidBirthdateError):
        user.set_birth_date(date(3000, 1, 1))


def test_user_add_illness_typical():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.illnesses() == set()
    user.add_illness('illness1')
    assert user.illnesses() == {'illness1'}
    user.add_illness('illness2')
    assert user.illnesses() == {'illness1', 'illness2'}


def test_user_add_illness_uppercase():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.illnesses() == set()
    user.add_illness('illNess1')
    assert user.illnesses() == {'illness1'}
    user.add_illness('Illness2')
    assert user.illnesses() == {'illness1', 'illness2'}


def test_user_add_illness_empty_name():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.illnesses() == set()
    user.add_illness('')
    assert len(user.illnesses()) == 0


def test_user_add_illness_all_white_spaces():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.illnesses() == set()
    user.add_illness('   \n  ')
    assert len(user.illnesses()) == 0


def test_user_add_illness_illegal_character_1():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.illnesses() == set()
    with raises(InvalidIllnessNameError):
        user.add_illness(',')


def test_user_add_illness_illegal_character_2():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.illnesses() == set()
    with raises(InvalidIllnessNameError):
        user.add_illness('"')


def test_user_add_illness_illegal_character_3():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.illnesses() == set()
    with raises(InvalidIllnessNameError):
        user.add_illness('x\nx')


def test_user_add_illness_illegal_character_4():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.illnesses() == set()
    with raises(InvalidIllnessNameError):
        user.add_illness("'")


def test_user_remove_illness_typical():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2), illnesses=['illness1', 'illness2'])
    assert user.illnesses() == {'illness1', 'illness2'}
    user.remove_illness('illness1')
    assert user.illnesses() == {'illness2'}
    user.remove_illness('illness2')
    assert user.illnesses() == set()


def test_user_add_allergy_typical():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.allergies() == set()
    user.add_allergy('substance1')
    assert user.allergies() == {'substance1'}
    user.add_allergy('substance2')
    assert user.allergies() == {'substance1', 'substance2'}


def test_user_add_allergy_uppercase():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.allergies() == set()
    user.add_allergy('suBstaNce1')
    assert user.allergies() == {'substance1'}
    user.add_allergy('Substance2')
    assert user.allergies() == {'substance1', 'substance2'}


def test_user_add_allergy_empty_name():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.allergies() == set()
    user.add_allergy('')
    assert user.allergies() == set()


def test_user_add_allergy_all_white_spaces():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.allergies() == set()
    user.add_allergy('  \n   ')
    assert user.allergies() == set()


def test_user_add_allergy_illegal_character_1():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.allergies() == set()
    with raises(InvalidSubstanceNameError):
        user.add_allergy(',')


def test_user_add_allergy_illegal_character_2():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.allergies() == set()
    with raises(InvalidSubstanceNameError):
        user.add_allergy('"')


def test_user_add_allergy_illegal_character_3():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.allergies() == set()
    with raises(InvalidSubstanceNameError):
        user.add_allergy('x\nx')


def test_user_add_allergy_illegal_character_4():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    assert user.allergies() == set()
    with raises(InvalidSubstanceNameError):
        user.add_allergy("'")


def test_user_remove_allergy_typical():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2), allergies={'substance1', 'substance2'})
    assert user.allergies() == {'substance1', 'substance2'}
    user.remove_allergy('substance1')
    assert user.allergies() == {'substance2'}
    user.remove_allergy('substance2')
    assert user.allergies() == set()


def test_user_add_prescription_typical():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    prescription1 = Prescription(id=0, medicine_name='Rutinorut', dosage=2, weekday=1)
    prescription2 = Prescription(id=1, medicine_name='Ivermectin', dosage=1, weekday=7)
    user.add_prescription(prescription1)
    assert user.prescriptions()[0] == prescription1
    user.add_prescription(prescription2)
    assert user.prescriptions()[1] == prescription2


def test_user_add_prescription_different_type():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    with raises(ValueError):
        user.add_prescription("Two doses of ivermectin every sunday")


def test_user_add_prescription_id_in_use():
    user = User(0, name='Dad', birth_date=date(1980, 1, 2))
    prescription1 = Prescription(id=0, medicine_name='Rutinorut', dosage=2, weekday=1)
    prescription2 = Prescription(id=0, medicine_name='Ivermectin', dosage=1, weekday=7)
    user.add_prescription(prescription1)
    with raises(IdAlreadyInUseError):
        user.add_prescription(prescription2)


def test_user_remove_prescription_typical():
    presc0 = Prescription(id=0, medicine_name='med1', dosage=1, weekday=2)
    presc1 = Prescription(id=1, medicine_name='med2', dosage=2, weekday=7)
    user = User(1,
                name='Mom',
                birth_date=date(1980, 1, 2),
                prescriptions=[presc0, presc1])
    assert user.prescriptions()[0] == presc0
    assert user.prescriptions()[1] == presc1
    user.remove_prescription(0)
    assert user.prescriptions().get(0) == None
    assert user.prescriptions()[1] == presc1
    user.remove_prescription(1)
    assert user.prescriptions().get(0) == None
    assert user.prescriptions().get(1) == None


def test_user_remove_prescription_no_such_id():
    user = User(1,
                name='Mom',
                birth_date=date(1980, 1, 2))
    with raises(NoSuchIdInUserPrescriptionsError):
        user.remove_prescription(0)


def test_user_age_typical(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(2024, 12, 2)
    monkeypatch.setattr('medihelp.user.date', MockDate)
    user = User(0, name='Dad', birth_date=date(1980, 11, 7))
    assert user.age() == 44


def test_user_age_no_birthday_this_year(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(2024, 12, 2)
    monkeypatch.setattr('medihelp.user.date', MockDate)
    user = User(0, name='Dad', birth_date=date(1980, 12, 7))
    assert user.age() == 43
