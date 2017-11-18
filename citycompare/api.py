AIR_QUALITY = 'Air Quality'
EMERGENCY_RESPONSE = 'Emergency Response'

def calgary_air_quality(api):
    pass


def calgary_emergency_response(api):
    pass


def edmonton_air_quality(api):
    pass


def edmonton_emergency_response(api):
    pass


CITY_DATA_API_MAP = {
    'calgary': {
        AIR_QUALITY: {
            'api': r'https://data.calgary.ca/api/odata/v4/uqjm-jxgp',
            'callback': calgary_air_quality
        },
        EMERGENCY_RESPONSE: {
            'api': r'https://data.calgary.ca/api/odata/v4/bdez-pds9',
            'callback': calgary_emergency_response
        }
    },
    'edmonton': {
        AIR_QUALITY: {
            'api': r'https://data.calgary.ca/api/odata/v4/uqjm-jxgp',
            'callback': edmonton_air_quality
        },
        EMERGENCY_RESPONSE: {
            'api': r'https://data.calgary.ca/api/odata/v4/bdez-pds9',
            'callback': edmonton_emergency_response
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