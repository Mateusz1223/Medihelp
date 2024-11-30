from datetime import date


class Medicine:
    '''
    A class to represent a single medicine.

    Attributes
    ----------
    :ivar _name: Name of the medicine.
    :vartype _name: str
    :ivar _manufacturer: Name of the manufacturer.
    :vartype _manufacturer: str
    :ivar _ilnesses: List of ilnesses that are cured by this medicine. Names should be written in lowercase.
    :vartype _ilnesses: list[str]
    :ivar _recipents: List of the names of the users who are taking the medicine.
    :vartype _recipents: List[str]
    :iver _substances: List of active substances in the medicine. Names should be written in lowercase.
    :vartype _substances: list[str]
    :iver _recommended_age: Recipent recommended age.
    :vartype _recommended_age: int
    :iver _doses: number of doses in the box.
    :vartype _doses: int
    :iver _doses_left: how many doses there is left.
    :vartype _doses_left: int
    :iver _expiration_date: Expiration date.
    :vartype _expiration_date: date
    :iver _notes: Notes that can be added by users.
    :vartype _notes: list[Note]
    '''

    pass
