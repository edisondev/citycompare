from sodapy import Socrata
import pandas as pd


def fetch_results(api, order=None, select=None, where=None, rowlimit=2000):
    client = Socrata(api['root'], None)
    return client.get(api['code'], order=order, select=select, where=where, limit=rowlimit)


def can_impaired_driving(api):
    results = fetch_results(api)  # , order='date DESC')
    results_df = pd.DataFrame.from_records(results)
    clean_results_df = pd.DataFrame()
    query = results_df.loc[results_df['police_jurisdiction'] == api['city']]
    query = query.drop(['police_jurisdiction'], axis=1)
    clean_results_df['date'] = [int(i[1:]) for i in query.columns.values]
    clean_results_df['number_impaired'] = query.values[0]
    return clean_results_df
