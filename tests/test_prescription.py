from medihelp.prescription import Prescription
from medihelp.errors import InvalidMedicineNameError, InvalidDosesError, InvalidWeekdayError
from pytest import raises


def test_prescription_create_typical():
    prescription = Prescription(id=0, medicine_name="Aloptine", dosage=2, weekday=7)
    assert prescription.id() == 0
    assert prescription.medicine_name() == "Aloptine"
    assert prescription.dosage() == 2
    assert prescription.weekday() == 7


def test_prescription_create_uppercases():
    prescription = Prescription(id=0, medicine_name="AloPtIne", dosage=2, weekday=1)
    assert prescription.id() == 0
    assert prescription.medicine_name() == "Aloptine"
    assert prescription.dosage() == 2
    assert prescription.weekday() == 1


def test_prescription_create_lowercase():
    prescription = Prescription(id=0, medicine_name="aloptine", dosage=2, weekday=1)
    assert prescription.id() == 0
    assert prescription.medicine_name() == "Aloptine"
    assert prescription.dosage() == 2
    assert prescription.weekday() == 1


def test_prescription_create_empty_medicine_name():
    with raises(InvalidMedicineNameError):
        Prescription(id=0, medicine_name='', dosage=2, weekday=3)


def test_prescription_create_medicine_name_all_white_spaces():
    with raises(InvalidMedicineNameError):
        Prescription(id=0, medicine_name='   \n   ', dosage=2, weekday=3)


def test_prescription_create_medicine_name_illegal_character_1():
    with raises(InvalidMedicineNameError):
        Prescription(id=0, medicine_name='x\nx', dosage=2, weekday=3)


def test_prescription_create_medicine_name_illegal_character_2():
    with raises(InvalidMedicineNameError):
        Prescription(id=0, medicine_name=',', dosage=2, weekday=3)


def test_prescription_create_medicine_name_illegal_character_3():
    with raises(InvalidMedicineNameError):
        Prescription(id=0, medicine_name='"', dosage=2, weekday=3)


def test_prescription_create_medicine_name_illegal_character_4():
    with raises(InvalidMedicineNameError):
        Prescription(id=0, medicine_name="'", dosage=2, weekday=3)


def test_prescription_create_medicine_name_too_long():
    with raises(InvalidMedicineNameError):
        Prescription(id=0, medicine_name='01234567891234567', dosage=2, weekday=3)


def test_prescription_create_medicine_name_edge():
    prescription = Prescription(id=0, medicine_name="1", dosage=2, weekday=1)
    assert prescription.id() == 0
    assert prescription.medicine_name() == "1"
    assert prescription.dosage() == 2
    assert prescription.weekday() == 1


def test_prescription_create_negative_dose():
    with raises(InvalidDosesError):
        Prescription(id=0, medicine_name='abc', dosage=-1, weekday=3)


def test_prescription_create_zero_dose():
    with raises(InvalidDosesError):
        Prescription(id=0, medicine_name='abc', dosage=0, weekday=3)


def test_prescription_create_invalid_weekday_1():
    with raises(InvalidWeekdayError):
        Prescription(id=0, medicine_name='abc', dosage=2, weekday=0)


def test_prescription_create_invalid_weekday_2():
    with raises(InvalidWeekdayError):
        Prescription(id=0, medicine_name='abc', dosage=2, weekday=8)
