from sodapy import Socrata
import pandas as pd


def fetch_results(api, order=None, **kwargs):
    client = Socrata(api['root'], None)
    return client.get(api['code'], order=order, limit=kwargs.pop('limit', 50000), **kwargs)


def calgary_voters(api):
    results = fetch_results(api)
    results_df = pd.DataFrame.from_records(results)
    query = results_df.loc[results_df['office'] == 'Mayor']
    total_voters = query['total_votes'].fillna(0).astype(int).sum()
    return total_voters


def edmonton_voters(api):
    results = fetch_results(api)
    results_df = pd.DataFrame.from_records(results)
    query = results_df.loc[results_df['contest_name'] == 'Mayor']
    total_voters = query['votes_received'].fillna(0).astype(int).sum()
    return total_voters
