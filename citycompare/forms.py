from flask_wtf import Form
from wtforms import SelectField

CITY_CHOICES = [
    ('', ''),
    ('calgary', 'Calgary'),
    ('edmonton', 'Edmonton'),
]

class CityForm(Form):
    first = SelectField(
        label='City 1',
        choices=CITY_CHOICES
    )
    second = SelectField(
        label='City 2',
        choices=CITY_CHOICES
    )