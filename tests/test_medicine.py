from medihelp.medicine import Medicine
from medihelp.user import User
from datetime import date
from pytest import raises
from medihelp.errors import (InvalidNameError,
                             InvalidDosesError,
                             TooManyDosesLeft,
                             InvalidAgeError,
                             EmptyListError,
                             AllergyWarning,
                             AgeWarning,
                             NotEnoughDosesError,
                             ExpiredMedicineError,
                             InvalidUserIDError)


def test_medicine_create():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    date_instance = date(2025, 12, 31)
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=6, expiration_date=date_instance, recipients=[0, 1, 2])
    assert medicine.id() == 0
    assert medicine.name() == 'Ivermectin'
    assert medicine.manufacturer() == 'Polfarma'
    assert medicine.illnesses() == {'illness1', 'illness2', 'illness3'}
    assert 0 in medicine.recipients()
    assert 1 in medicine.recipients()
    assert 2 in medicine.recipients()
    assert medicine.substances() == {'nicotine', 'caffeine'}
    assert medicine.recommended_age() == 0
    assert medicine.doses() == 10
    assert medicine.doses_left() == 6
    assert medicine.expiration_date() == date_instance
    assert medicine.note(0) is None
    assert medicine.note(1) is None
    assert medicine.note(2) is None


def test_medicine_create_too_many_doses_left():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    date_instance = date(2025, 12, 31)
    with raises(TooManyDosesLeft):
        Medicine(0, name='iveRmectin', manufacturer='polfARma',
                 illnesses=illneses, substances=substances,
                 recommended_age=0, doses=10, doses_left=11, expiration_date=date_instance,
                 recipients=[0, 1, 2])


def test_medicine_note_invalid_id_1():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=100, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    with raises(InvalidUserIDError):
        medicine.note(-1)


def test_medicine_note_invalid_id_2():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=100, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    with raises(InvalidUserIDError):
        medicine.note(3)


def test_medicine_set_note_invalid_id_1():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=100, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    with raises(InvalidUserIDError):
        medicine.set_note(-1, 'Hello World!')


def test_medicine_set_note_invalid_id_2():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=100, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    with raises(InvalidUserIDError):
        medicine.set_note(3, 'Hello World!')


def test_medicine_set_note_typical():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=100, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))

    medicine.set_note(0, 'Hello World! 1')
    medicine.set_note(1, 'Hello World! 2')
    medicine.set_note(2, 'Hello World! 3')

    assert medicine.note(0) == 'Hello World! 1'
    assert medicine.note(1) == 'Hello World! 2'
    assert medicine.note(2) == 'Hello World! 3'


def test_medicine_set_note_none():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=100, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))

    medicine.set_note(0, 'Hello World! 1')
    assert medicine.note(0) == 'Hello World! 1'
    medicine.set_note(0, None)
    assert medicine.note(0) is None


def test_medicine_create_empty_illneses_list():
    substances = ['nicoTine', 'caffeine']
    date_instance = date(2025, 12, 31)
    with raises(EmptyListError):
        Medicine(0, name='iveRmectin', manufacturer='polfARma',
                 illnesses=[], substances=substances,
                 recommended_age=0, doses=10, doses_left=10, expiration_date=date_instance)


def test_medicine_create_empty_substances_list():
    illneses = ['Illnes1, illness2, IllNes3']
    date_instance = date(2025, 12, 31)
    with raises(EmptyListError):
        Medicine(0, name='iveRmectin', manufacturer='polfARma',
                 illnesses=illneses, substances=[],
                 recommended_age=0, doses=10, doses_left=10, expiration_date=date_instance)


def test_medicine_create_empty_name():
    illneses = ['Illnes1, illness2, IllNes3']
    substances = ['nicoTine', 'caffeine']
    date_instance = date(2025, 12, 31)
    with raises(InvalidNameError):
        Medicine(0, name='', manufacturer='polfARma',
                 illnesses=illneses, substances=substances,
                 recommended_age=-1, doses=10, doses_left=10, expiration_date=date_instance)


def test_medicine_create_empty_manufacturer():
    illneses = ['Illnes1, illness2, IllNes3']
    substances = ['nicoTine', 'caffeine']
    date_instance = date(2025, 12, 31)
    with raises(InvalidNameError):
        Medicine(0, name='daadadsdas', manufacturer='',
                 illnesses=illneses, substances=substances,
                 recommended_age=-1, doses=10, doses_left=10, expiration_date=date_instance)


def test_medicine_create_invalid_recommended_age():
    illneses = ['Illnes1, illness2, IllNes3']
    substances = ['nicoTine', 'caffeine']
    date_instance = date(2025, 12, 31)
    with raises(InvalidAgeError):
        Medicine(0, name='iveRmectin', manufacturer='polfARma',
                 illnesses=illneses, substances=substances,
                 recommended_age=-1, doses=10, doses_left=10, expiration_date=date_instance)


def test_medicine_create_invalid_doses():
    illneses = ['Illnes1, illness2, IllNes3']
    substances = ['nicoTine', 'caffeine']
    date_instance = date(2025, 12, 31)
    with raises(InvalidDosesError):
        Medicine(0, name='iveRmectin', manufacturer='polfARma',
                 illnesses=illneses, substances=substances,
                 recommended_age=0, doses=0, doses_left=0, expiration_date=date_instance)


def test_medicine_is_expired_false(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(2024, 12, 2)
    monkeypatch.setattr('medihelp.user.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    date_instance = date(2025, 12, 31)
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date_instance)

    assert not medicine.is_expired()


def test_medicine_is_expired_true(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(2024, 12, 2)
    monkeypatch.setattr('medihelp.medicine.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date(2024, 12, 1))

    assert medicine.is_expired()


def test_medicine_is_expired_edge_case(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(2024, 12, 2)
    monkeypatch.setattr('medihelp.medicine.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    assert not medicine.is_expired()


def test_medicine_add_recipient_typical():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    assert medicine.recipients() == set()
    medicine.add_recipient(0)
    medicine.add_recipient(1)
    medicine.add_recipient(2)
    assert 0 in medicine.recipients()
    assert 1 in medicine.recipients()
    assert 2 in medicine.recipients()


def test_medicine_add_recipient_typical_invalid_id_1():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    assert medicine.recipients() == set()
    with raises(InvalidUserIDError):
        medicine.add_recipient(-1)


def test_medicine_add_recipient_typical_invalid_id_2():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    assert medicine.recipients() == set()
    with raises(InvalidUserIDError):
        medicine.add_recipient(3)


def test_medicine_remove_recipient_typical():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date(2024, 12, 2), recipients=[0, 1, 2])
    assert 0 in medicine.recipients()
    assert 1 in medicine.recipients()
    assert 2 in medicine.recipients()
    medicine.remove_recipient(0)
    medicine.remove_recipient(1)
    medicine.remove_recipient(2)
    assert medicine.recipients() == set()


def test_medicine_remove_recipient_typical_invalid_id_1():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    assert medicine.recipients() == set()
    with raises(InvalidUserIDError):
        medicine.remove_recipient(-1)


def test_medicine_remove_recipient_typical_invalid_id_2():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    assert medicine.recipients() == set()
    with raises(InvalidUserIDError):
        medicine.remove_recipient(3)


def test_medicine_take_doses_typical(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(1900, 12, 2)
    monkeypatch.setattr('medihelp.medicine.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    assert medicine.doses_left() == 10
    dad = User(0, name='Dad', birth_date=date(1980, 1, 2))
    medicine.take_doses(2, dad)
    assert medicine.doses_left() == 8


def test_medicine_take_doses_allergy_warning(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(1900, 12, 2)
    monkeypatch.setattr('medihelp.medicine.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    assert medicine.doses_left() == 10
    dad = User(0, name='Dad', birth_date=date(1980, 1, 2), allergies=['nicotine', 'substance1'])
    with raises(AllergyWarning, match=r'Medicine cannot be given to the user because he is allergic to nicotine, substance1.'):
        medicine.take_doses(1, dad)


def test_medicine_take_doses_age_warning(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(1900, 12, 2)
    monkeypatch.setattr('medihelp.medicine.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=100, doses=10, doses_left=10, expiration_date=date(2024, 12, 2))
    assert medicine.doses_left() == 10
    dad = User(0, name='Dad', birth_date=date(1980, 1, 2))
    with raises(AgeWarning):
        medicine.take_doses(3, dad)


def test_medicine_take_doses_not_enough_doses(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(1900, 12, 2)
    monkeypatch.setattr('medihelp.medicine.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=10, doses=10, doses_left=2, expiration_date=date(2024, 12, 2))
    assert medicine.doses_left() == 2
    dad = User(0, name='Dad', birth_date=date(1980, 1, 2))
    with raises(NotEnoughDosesError):
        medicine.take_doses(3, dad)


def test_medicine_take_doses_expired():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(0, name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=10, doses=10, doses_left=10, expiration_date=date(1900, 12, 2))
    assert medicine.doses_left() == 10
    dad = User(0, name='Dad', birth_date=date(1980, 1, 2))
    with raises(ExpiredMedicineError):
        medicine.take_doses(3, dad)
