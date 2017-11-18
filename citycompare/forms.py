from flask_wtf import Form
from wtforms import SelectField

class CityForm(Form):
    first = SelectField(
        label='City 1',
        choices=[
            ('Calgary', 'calgary'),
            ('Edmonton', 'edmonton'),
        ]
    )
    second = SelectField(
        label='City 2',
        choices=[
            ('Calgary', 'calgary'),
            ('Edmonton', 'edmonton'),
        ]
    )