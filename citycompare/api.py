from sodapy import Socrata
import pandas as pd

AIR_QUALITY = 'Air Quality'
EMERGENCY_RESPONSE = 'Emergency Response'
BUSINESS = 'Business Licenses'

def fetch_results(api, order=None, select=None, where=None, rowlimit=2000):
    client = Socrata(api['root'], None)
    return client.get(api['code'], order=order, select=select, where=where, limit=rowlimit)

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
    results = fetch_results(api, select = 'alarm_year,incident_count,major_incident_type',
                            where = 'alarm_year>2014', rowlimit=10000)
    df = pd.DataFrame.from_records(results)
    print(df.shape)
    df['incident_count'] = pd.to_numeric(df['incident_count'])
    alarm_years = df.alarm_year.unique().tolist()
    print(alarm_years)
    alarm_type  = ['Fire'] # Arbitrarily selected. Full list by: df.major_incident_type.unique().tolist()

    year = []
    inc_type = []
    count = []
    for y in alarm_years:
        for t in alarm_type:
            year.append(y)
            inc_type.append(t)
            df2 = df.loc[(df['alarm_year'] == y) & (df['major_incident_type'] == t)]
            c = sum(df2['incident_count'].tolist())
            count.append(c)

    d = {'year': year, 'incident type': inc_type, 'count': count}
    conc_df = pd.DataFrame(data=d)
    return  conc_df



def edmonton_emergency_response(api):
    results = fetch_results(api, select = 'dispatch_year, count, event_description',
                            where = 'dispatch_year>2014', rowlimit=30000)
    df = pd.DataFrame.from_records(results)
    print(df.shape)
    df['count'] = pd.to_numeric(df['count'])
    df['event_description'] = df['event_description'].replace(
        ['FIRE', 'VEHICLE FIRE', 'OUTSIDE FIRE', 'PERMIT-BURNING OR OTHER'], 'Fire')
    df['event_description'] = df['event_description'].replace(['MEDICAL', 'RESCUE'], 'Medical/Rescue')


    alarm_years = df.dispatch_year.unique().tolist()
    print(alarm_years)
    alarm_type  = ['Fire'] # Arbitrarily selected. Full list by: df.event_description.unique().tolist()

    year = []
    inc_type = []
    count = []
    for y in alarm_years:
        for t in alarm_type:
            year.append(y)
            inc_type.append(t)
            df2 = df.loc[(df['dispatch_year'] == y) & (df['event_description'] == t)]
            c = sum(df2['count'].tolist())
            count.append(c)

    d = {'year': year, 'incident type': inc_type, 'count': count}
    conc_df = pd.DataFrame(data=d)
    return  conc_df

def calgary_business(api):
    results = fetch_results(api, order='jobcreated DESC',rowlimit=50000)
    results_df = pd.DataFrame.from_records(results)
    
    clean_df=results_df[results_df['jobstatusdesc']!='EXPIRED']
    clean_df=clean_df['licencetypes'].value_counts()
    clean_df=clean_df.iloc[::-1]
    clean_df.index=[x.upper() for x in clean_df.index.values]
    
    return clean_df

def edmonton_business(api):
    results = fetch_results(api, order='status DESC',rowlimit=50000)
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
                'root': r'data.edmonton.ca',
                'code': r'hpqc-zvnm'
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