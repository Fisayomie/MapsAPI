#import libaries
import numpy as np
import pandas as pd
# import library to get region from Google Maps
import googlemaps
from .mykey.py import myapikey
UNILOC = pd.DataFrame(pd.read_csv('university names .csv'))
UNILOC['country code'] = UNILOC['country code'].str[:-1]
print(UNILOC.head())

print(UNILOC['country code'].nunique())

print(UNILOC.info())

# Working with the googlemaps API
# Assigning key to a variable name
MYAPIKEY = googlemaps.Client(key=myapikey)

# Testing to see if myapikey works
print(UNILOC.iat[5000, 1])
RES = MYAPIKEY.geocode(UNILOC.iat[5000, 1])
print(RES[0]['address_components'])

#Testing the condition
CORRECT = None
if (RES[0]['address_components'][4]['short_name'] == UNILOC.iat[5000, 2]):
    CORRECT = RES[0]['address_components'][3]['long_name']
else:
    CORRECT = np.nan
#Works

# Implementing the Condition that regions must be in the same country
UNILOC['Region'] = None
for i in range(0, len(UNILOC), 1):
    geocode_result = MYAPIKEY.geocode(UNILOC.iat[i, 1])
    try:
        region = geocode_result[0]['address_components'][3]['long_name']
        if (geocode_result[0]['address_components'][4]['short_name'] == UNILOC.iat[i, 2]):
            UNILOC.iat[i, UNILOC.columns.get_loc('Region')] = region
        else:
            UNILOC.iat[i, UNILOC.columns.get_loc('Region')] = np.nan
    except:
        region = np.nan

# Accounting for duplicate region/location
UNILOC.drop_duplicates('university names', keep='first', inplace=True)
print(UNILOC.head())