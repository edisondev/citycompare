from __future__ import absolute_import
from .api import AIR_QUALITY, EMERGENCY_RESPONSE
import plotly
from plotly.graph_objs import Scatter, Layout, Bar

""" data will be passed into these plot functions in the following format
{ 
    city1: data,
    city2: data,
}
"""

def air_quality_plot(data):
    plot_data = []
    for city in data:
        plot_data.append(Scatter(x=data[city]['date'], y=data[city]['air_quality'], name=city, mode='markers'))

    plot_html = plotly.offline.plot(
        {
            'data': plot_data,
            'layout': Layout(title='Air Quality', legend={'orientation': 'h'})
        },
        output_type='div'
    )
    return plot_html

def emergency_resp_plot(data):
    plot_data = []
    for city in data:
        plot_data.append(Bar(x=data[city]['year'], y=data[city]['count'], name=city))

    plot_html = plotly.offline.plot(
        {
            'data': plot_data,
            'layout': Layout(title='Emergency Response', legend={'orientation': 'h'})
        },
        output_type='div'
    )
    return plot_html


PLOT_MAP = {
    AIR_QUALITY: air_quality_plot,
    EMERGENCY_RESPONSE: emergency_resp_plot
}

def generate_plot(field, data):
    if field not in PLOT_MAP:
        return """<b> no plot for {} field </b>""".format(field)
    return PLOT_MAP[field](data)