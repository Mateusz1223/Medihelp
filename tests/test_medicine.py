from medihelp.medicine import Medicine
from datetime import date
from pytest import raises
from medihelp.errors import EmptyListError, InvalidNameError, InvalidDoseError, InvalidAgeError


def test_medicine_create():
    illneses = ['Illness1', 'illness2', 'IllNess3']
    substances = ['nicoTine', 'Caffeine']
    date_instance = date(2025, 12, 31)
    medicine = Medicine(name='iveRmectin', manufacturer='polfARma',
                        illnesses=illneses, substances=substances,
                        recommended_age=0, doses=10, expiration_date=date_instance)
    assert medicine.name() == 'Ivermectin'
    assert medicine.manufacturer() == 'Polfarma'
    assert medicine.illnesses() == ['illness1', 'illness2', 'illness3']
    assert medicine.substances() == ['nicotine', 'caffeine']
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
