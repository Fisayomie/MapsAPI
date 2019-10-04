""" Code to fill in the location of the University names using Google Maps API """

import numpy as np
import pandas as pd
from key import mykey
# import library to get region from Google Maps
import googlemaps

DF = pd.DataFrame(pd.read_csv('university_names.csv'))
DF['country code'] = DF['country code'].str[:-1]
print(DF.head())

print(DF['country code'].nunique())

print(DF.info())

# Working with the googlemaps API
# Assigning key to be used
MYKEY = googlemaps.Client(key=mykey)

# Testing my key
print(DF.iat[5000, 1])
RES = MYKEY.geocode(DF.iat[5000, 1])
print(RES[0]['address_components'])

#Testing the condition
CORRECT = None
if (RES[0]['address_components'][4]['short_name'] == DF.iat[5000, 2]):
    CORRECT = RES[0]['address_components'][3]['long_name']
else:
    CORRECT = np.nan
#Tested okay...

# Implementing the Condition that regions must be in the same country
DF['Region'] = None
for i in range(0, len(DF), 1):
    geocode_result = MYKEY.geocode(DF.iat[i, 1])
    try:
        region = geocode_result[0]['address_components'][3]['long_name']
        if (geocode_result[0]['address_components'][4]['short_name'] == DF.iat[i, 2]):
            DF.iat[i, DF.columns.get_loc('Region')] = region
        else:
            DF.iat[i, DF.columns.get_loc('Region')] = np.nan
    except:
        region = np.nan

# Accounting for duplicate region/location
DF.drop_duplicates('university names', keep='first', inplace=True)
print(DF.head())
