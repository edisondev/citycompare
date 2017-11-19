from sodapy import Socrata
import pandas as pd

AIR_QUALITY = 'Air Quality'
EMERGENCY_RESPONSE = 'Emergency Response'
BUSINESS = 'Business Licenses'


def fetch_results(api, order=None, row_limit=2000):
    client = Socrata(api['root'], None)
    return client.get(api['code'], order=order, limit=row_limit)

def calgary_air_quality(api):
    results = fetch_results(api, order='date DESC')
    results_df = pd.DataFrame.from_records(results)
    clean_results_df = pd.DataFrame()
    query = results_df.loc[results_df['parameter'] == 'Air Quality Index']
    clean_results_df['date'] = pd.to_datetime(query['date'])
    clean_results_df['air_quality'] = query['average_daily_value']
    return clean_results_df

def edmonton_air_quality(api):
    results = fetch_results(api, order='date_measured DESC')
    results_df = pd.DataFrame.from_records(results)
    clean_results_df = pd.DataFrame()
    query = results_df.loc[results_df['parameter_measured'] == 'Air Quality Index']
    clean_results_df['date'] = pd.to_datetime(query['date_measured'])
    clean_results_df['air_quality'] = query['average_daily_value']
    return clean_results_df

def calgary_emergency_response(api):
    pass

def edmonton_emergency_response(api):
    pass

def calgary_business(api):
    results = fetch_results(api, order='jobcreated DESC',row_limit=50000)
    results_df = pd.DataFrame.from_records(results)
    
    clean_df=results_df[results_df['jobstatusdesc']!='EXPIRED']
    clean_df=clean_df['licencetypes'].value_counts()
    clean_df=clean_df.iloc[::-1]
    clean_df.index=[x.upper() for x in clean_df.index.values]
    
    return clean_df

def edmonton_business(api):
    results = fetch_results(api, order='status DESC',row_limit=50000)
    results_df = pd.DataFrame.from_records(results)

    clean_df=results_df[results_df['status']=='ISSUED']
    clean_df=clean_df['business_category'].value_counts()
    clean_df=clean_df.iloc[::-1] #reverse indeces
    clean_df.index=[x.upper() for x in clean_df.index.values] #set labels to upper
    return clean_df


CITY_DATA_API_MAP = {
    'calgary': {
        AIR_QUALITY: {
            'api': {
                'root': r'data.calgary.ca',
                'code': r'uqjm-jxgp'
            },
            'callback': calgary_air_quality
        },
        EMERGENCY_RESPONSE: {
            'api': {
                'root': r'data.calgary.ca',
                'code': r'bdez-pds9'
            },
            'callback': calgary_emergency_response
        },
        BUSINESS: {
            'api': {
                'root': r'data.calgary.ca',
                'code': r'agnq-4jj6'
            },
            'callback': calgary_business
        } 
    },
    'edmonton': {
        AIR_QUALITY: {
            'api': {
                'root': r'data.edmonton.ca',
                'code': r'44dx-d5qn'
            },
            'callback': edmonton_air_quality
        },
        EMERGENCY_RESPONSE: {
            'api': {
                'root': r'data.calgary.ca',
                'code': r'bdez-pds9'
            },
            'callback': edmonton_emergency_response
        },
        BUSINESS: {
            'api': {
                'root': r'data.edmonton.ca',
                'code': r'3trf-izgx'
            },
            'callback': edmonton_business
        } 
    },
    'another city': {
        AIR_QUALITY: {
            'api': r'fake api',
            'callback': None
        },
    }
}

def city_data(city):
    if city.lower() not in CITY_DATA_API_MAP:
        return None
    return CITY_DATA_API_MAP[city.lower()]


def matched_city_data(cities):
    matched_data = {}
    for city in cities:
        data = city_data(city)
        for data_type in data:
            if data_type not in matched_data:
                matched_data[data_type] = {}
            matched_data[data_type][city] = data[data_type]

    filtered_data = {}
    for data_type in matched_data:
        if len(matched_data[data_type]) >= 2:
            filtered_data[data_type] = matched_data[data_type]
    return filtered_data


# example to test the city_data
if __name__=='__main__':
    import pprint
    pprint.pprint(matched_city_data(['calgary', 'edmonton']))