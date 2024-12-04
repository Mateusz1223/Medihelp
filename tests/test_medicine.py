from medihelp.medicine import Medicine
from medihelp.user import User
from datetime import date
from pytest import raises
from medihelp.errors import (InvalidNameError,
                             InvalidDoseError,
                             InvalidAgeError,
                             EmptyListError,
                             AllergyWarning,
                             AgeWarning,
                             NotEnoughDosesError,
                             ExpiredMedicineError)


def test_medicine_create():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    date_instance = date(2025, 12, 31)
    medicine = Medicine(name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, expiration_date=date_instance)
    assert medicine.name() == 'Ivermectin'
    assert medicine.manufacturer() == 'Polfarma'
    assert medicine.illnesses() == {'illness1', 'illness2', 'illness3'}
    assert medicine.substances() == {'nicotine', 'caffeine'}
    assert medicine.recommended_age() == 0
    assert medicine.doses() == 10
    assert medicine.expiration_date() == date_instance


def test_medicine_create_empty_illneses_list():
    substances = ['nicoTine', 'caffeine']
    date_instance = date(2025, 12, 31)
    with raises(EmptyListError):
        Medicine(name='iveRmectin', manufacturer='polfARma',
                 illnesses=[], substances=substances,
                 recommended_age=0, doses=10, expiration_date=date_instance)


def test_medicine_create_empty_substances_list():
    illneses = ['Illnes1, illness2, IllNes3']
    date_instance = date(2025, 12, 31)
    with raises(EmptyListError):
        Medicine(name='iveRmectin', manufacturer='polfARma',
                 illnesses=illneses, substances=[],
                 recommended_age=0, doses=10, expiration_date=date_instance)


def test_medicine_create_empty_name():
    illneses = ['Illnes1, illness2, IllNes3']
    substances = ['nicoTine', 'caffeine']
    date_instance = date(2025, 12, 31)
    with raises(InvalidNameError):
        Medicine(name='', manufacturer='polfARma',
                 illnesses=illneses, substances=substances,
                 recommended_age=-1, doses=10, expiration_date=date_instance)


def test_medicine_create_empty_manufacturer():
    illneses = ['Illnes1, illness2, IllNes3']
    substances = ['nicoTine', 'caffeine']
    date_instance = date(2025, 12, 31)
    with raises(InvalidNameError):
        Medicine(name='daadadsdas', manufacturer='',
                 illnesses=illneses, substances=substances,
                 recommended_age=-1, doses=10, expiration_date=date_instance)


def test_medicine_create_invalid_recommended_age():
    illneses = ['Illnes1, illness2, IllNes3']
    substances = ['nicoTine', 'caffeine']
    date_instance = date(2025, 12, 31)
    with raises(InvalidAgeError):
        Medicine(name='iveRmectin', manufacturer='polfARma',
                 illnesses=illneses, substances=substances,
                 recommended_age=-1, doses=10, expiration_date=date_instance)


def test_medicine_create_invalid_doses():
    illneses = ['Illnes1, illness2, IllNes3']
    substances = ['nicoTine', 'caffeine']
    date_instance = date(2025, 12, 31)
    with raises(InvalidDoseError):
        Medicine(name='iveRmectin', manufacturer='polfARma',
                 illnesses=illneses, substances=substances,
                 recommended_age=0, doses=0, expiration_date=date_instance)


def test_medicine_is_expired_false(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(2024, 12, 2)
    monkeypatch.setattr('medihelp.user.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    date_instance = date(2025, 12, 31)
    medicine = Medicine(name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, expiration_date=date_instance)

    assert not medicine.is_expired()


def test_medicine_is_expired_true(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(2024, 12, 2)
    monkeypatch.setattr('medihelp.medicine.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, expiration_date=date(2024, 12, 1))

    assert medicine.is_expired()


def test_medicine_is_expired_edge_case(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(2024, 12, 2)
    monkeypatch.setattr('medihelp.medicine.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, expiration_date=date(2024, 12, 2))
    assert not medicine.is_expired()


def test_medicine_take_doses_typical(monkeypatch):
    class MockDate(date):
        @classmethod
        def today(cls):
            return cls(1900, 12, 2)
    monkeypatch.setattr('medihelp.medicine.date', MockDate)

    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    medicine = Medicine(name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, expiration_date=date(2024, 12, 2))
    assert medicine.doses_left() == 10
    dad = User(name='Dad', birth_date=date(1980, 1, 2))
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
    medicine = Medicine(name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, expiration_date=date(2024, 12, 2))
    assert medicine.doses_left() == 10
    dad = User(name='Dad', birth_date=date(1980, 1, 2), allergies=['nicotine', 'substance1'])
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
    medicine = Medicine(name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=100, doses=10, expiration_date=date(2024, 12, 2))
    assert medicine.doses_left() == 10
    dad = User(name='Dad', birth_date=date(1980, 1, 2))
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
    medicine = Medicine(name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=10, doses=2, expiration_date=date(2024, 12, 2))
    assert medicine.doses_left() == 2
    dad = User(name='Dad', birth_date=date(1980, 1, 2))
    with raises(NotEnoughDosesError):
        medicine.take_doses(3, dad)


def test_medicine_take_doses_expired():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine', 'substance1']
    medicine = Medicine(name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=10, doses=10, expiration_date=date(1900, 12, 2))
    assert medicine.doses_left() == 10
    dad = User(name='Dad', birth_date=date(1980, 1, 2))
    with raises(ExpiredMedicineError):
        medicine.take_doses(3, dad)
