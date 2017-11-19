from sodapy import Socrata
import pandas as pd
import plotly
from plotly.graph_objs import Scatter, Layout


def fetch_results(api, order=None, **kwargs):
    client = Socrata(api['root'], None)
    return client.get(api['code'], order=order, limit=kwargs.pop('limit', 50000), **kwargs)


def calgary_fires(api):
    results = fetch_results(api, order='date DESC')
    results_df = pd.DataFrame.from_records(results)
    query = results_df.loc[results_df['major_incident_type'] == 'Fire']
    query['date'] = pd.to_datetime(query['date'])
    fire_by_month = query['incident_count'].astype(int).groupby([query['date'].dt.year, query['date'].dt.month]).agg(['sum'])
    df = pd.DataFrame({
        'date': [pd.datetime(year=int(y), month=int(m), day=1) for y, m in fire_by_month.index],
        'number_of_fires': fire_by_month['sum']})
    return df


def edmonton_fires(api):
    fire_df = pd.read_json(r'https://data.edmonton.ca/resource/hpqc-zvnm.json?event_description=FIRE&$limit=10000')
    vehicle_fire_df = pd.read_json(r'https://data.edmonton.ca/resource/hpqc-zvnm.json?event_description=VEHICLE%20FIRE&$limit=10000')
    fire_df['date'] = pd.to_datetime(fire_df['dispatch_date'])
    vehicle_fire_df['date'] = pd.to_datetime(vehicle_fire_df['dispatch_date'])
    fire_by_month = fire_df['date'].groupby([fire_df['date'].dt.year, fire_df['date'].dt.month]).size()
    vehicle_by_month = vehicle_fire_df['date'].groupby([vehicle_fire_df['date'].dt.year, vehicle_fire_df['date'].dt.month]).size()
    total_by_month = vehicle_by_month + fire_by_month
    df = pd.DataFrame({
        'date': [pd.datetime(year=int(y), month=int(m), day=1) for y, m in total_by_month.index],
        'number_of_fires': total_by_month.values})
    return df
