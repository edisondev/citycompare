from __future__ import absolute_import
from flask import render_template, flash, url_for, redirect
from citycompare import flask_app
from sodapy import Socrata
import pandas as pd
import plotly
from plotly.graph_objs import Scatter, Layout,Bar

from .forms import CityForm
from .api import matched_city_data
from .plots import generate_plot
from flask import request

@flask_app.route('/', methods=['GET', 'POST'])
def index():
    city_form = CityForm()
    if request.method == 'POST' and city_form.validate():
        # flash('loading {} vs {}...'.format(city_form.first.data, city_form.second.data))
        return redirect(url_for('plot', first=city_form.first.data, second=city_form.second.data))
    return render_template(
        'index.html',
        city_form=CityForm(),
    )

@flask_app.route('/plot', methods=['GET', 'POST'])
def plot():
    city_form = CityForm()
    if request.method == 'POST' and city_form.validate():
        # flash('loading {} vs {}...'.format(city_form.first.data, city_form.second.data))
        return redirect(url_for('plot', first=city_form.first.data, second=city_form.second.data))

    first = request.args.get('first')
    second = request.args.get('second')

    if first == second:
        flash('Pick two different cities', 'error')
        return render_template(
            'index.html',
            city_form=city_form,
        )

    # get the matched fields
    data_sources = matched_city_data([first, second])

    # for each field generate the data
    plots = []
    for field in data_sources:
        field_data = {}
        for city in data_sources[field]:
            field_data[city] = data_sources[field][city]['callback'](data_sources[field][city]['api'])
        plots.append(generate_plot(field=field, data=field_data))

    return render_template(
        'index.html',
        city_form=city_form,
        plots=plots
    )