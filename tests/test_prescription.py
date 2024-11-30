from medihelp.prescription import Prescription
from medihelp.errors import InvalidNameError, InvalidDoseError, InvalidWeekdayError
from pytest import raises


def test_prescription_create_typical():
    prescription = Prescription(medicine_name="aloptine", dosage=2, weekday=7)
    assert prescription.medicine_name() == "aloptine"
    assert prescription.dosage() == 2
    assert prescription.weekday() == 7


def test_prescription_create_uppercases_in_name():
    prescription = Prescription(medicine_name="AloPtIne", dosage=2, weekday=1)
    assert prescription.medicine_name() == "aloptine"
    assert prescription.dosage() == 2
    assert prescription.weekday() == 1


def test_prescription_create_empty_name():
    with raises(InvalidNameError):
        Prescription(medicine_name='', dosage=2, weekday=3)


def test_prescription_create_negative_dose():
    with raises(InvalidDoseError):
        Prescription(medicine_name='abc', dosage=-1, weekday=3)


def test_prescription_create_zero_dose():
    with raises(InvalidDoseError):
        Prescription(medicine_name='abc', dosage=0, weekday=3)


def test_prescription_create_invalid_weekday_1():
    with raises(InvalidWeekdayError):
        Prescription(medicine_name='abc', dosage=2, weekday=0)


def test_prescription_create_invalid_weekday_2():
    with raises(InvalidWeekdayError):
        Prescription(medicine_name='abc', dosage=2, weekday=8)
