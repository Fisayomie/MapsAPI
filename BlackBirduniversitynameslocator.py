#import libaries
import numpy as np
import pandas as pd
# import library to get region from Google Maps
import googlemaps
from apikey.ipynb import myapikey
 
uniloc = pd.DataFrame( pd.read_csv('university names .csv'))
uniloc['country code'] = uniloc['country code'].str[:-1]
print(uniloc.head())

print(uniloc['country code'].nunique())

print(uniloc.info())

# Working with the googlemaps API
# Assigning key to a variable name
MYAPIKEY = googlemaps.Client(key=myapikey)

# Testing to see if myapikey works
print(uniloc.iat[5000, 1])
RES = MYAPIKEY.geocode(uniloc.iat[5000, 1])
print(RES[0]['address_components'])

#Testing the condition
CORRECT = None
if (RES[0]['address_components'][4]['short_name'] == uniloc.iat[5000, 2]):
    CORRECT = RES[0]['address_components'][3]['long_name']
else:
    CORRECT = np.nan
#Works

# Implementing the Condition that regions must be in the same country
uniloc['Region'] = None
for i in range(0, len(uniloc), 1):
    geocode_result = MYAPIKEY.geocode(uniloc.iat[i, 1])
    try:
        region = geocode_result[0]['address_components'][3]['long_name']
        if (geocode_result[0]['address_components'][4]['short_name'] == uniloc.iat[i, 2]):
            uniloc.iat[i, uniloc.columns.get_loc('Region')] = region
        else:
            uniloc.iat[i, uniloc.columns.get_loc('Region')] = np.nan
    except:
        region = np.nan

# Accounting for duplicate region/location
uniloc.drop_duplicates('university names', keep='first', inplace=True)
print(uniloc.head())