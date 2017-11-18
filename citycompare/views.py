from __future__ import absolute_import
from flask import render_template
from citycompare import flask_app
from .forms import CityForm

@flask_app.route('/')
def index():
    return render_template(
        'index.html',
        city_form=CityForm(),
    )
