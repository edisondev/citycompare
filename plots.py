from __future__ import absolute_import
from .api import AIR_QUALITY, EMERGENCY_RESPONSE, BUSINESS
import plotly
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout, Bar
from plotly import tools

""" data will be passed into these plot functions in the following format
{ 
    city1: data,
    city2: data,
}
"""
#Test Line1

#Test Line2
def business_plot(data):
    plot_data = tools.make_subplots(rows=1, cols=2)
    print("Start make plot")
    idx=1
    for city in data:
        dt=Bar(y=data[city].index.values[-20:],
               x=data[city].values[-20:],
               orientation = 'h',
               name=city)
        plot_data.append_trace(dt, 1, idx)
        idx=idx+1
    
    plot_data['layout'].update(font=dict(size=10, color='#000000'),
             legend=dict(orientation="h"),
             margin=go.Margin(l=[350,350],
                              r=0,
                              b=100,
                              t=100
                              ),
             title='Business Comparison'
            )
    plot_html = plotly.offline.plot(plot_data, output_type='div')
        #{
        #    'data': plot_data,
        #    'layout': Layout(title='Air Quality', legend={'orientation': 'h'})
        #},
        #output_type='div'
    #)
    return plot_html



def air_quality_plot(data):
    plot_data = []
    for city in data:
        plot_data.append(Scatter(x=data[city]['date'], y=data[city]['air_quality'], name=city, mode='markers'))

    plot_html = plotly.offline.plot(
        {
            'data': plot_data,
            'layout': Layout(title='Air Quality', legend={'orientation': 'h'})
        },
        output_type='div')
    print("Here2")
    return plot_html


PLOT_MAP = {
    AIR_QUALITY: air_quality_plot,
    BUSINESS: business_plot
}

def generate_plot(field, data):
    if field not in PLOT_MAP:
        return """<b> no plot for {} field </b>""".format(field)
    return PLOT_MAP[field](data)