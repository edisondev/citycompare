from flask_wtf import FlaskForm
from wtforms import SelectField

CITY_CHOICES = [
    (None, 'Pick a city...'),
    ('calgary', 'Calgary'),
    ('edmonton', 'Edmonton'),
]

class CityForm(FlaskForm):
    first = SelectField(
        label='City 1',
        choices=CITY_CHOICES,
    )
    second = SelectField(
        label='City 2',
        choices=CITY_CHOICES
    )