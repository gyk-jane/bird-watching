"""Contains helper functions to help connect to the eBird API.

The eBird API requires specific codes for locations to retrieve bird data from. This module contains helper functions that return two different types of region specifiers for a given region:  its (latitude, longitude) and subnational type2 region code.

"""
import requests
import json
from geopy import geocoders

def get_lat_long(location):
    """Fetches latitude and longitude of an area.
    
    Args:
        location (str): The location
    Returns:
        List: A list [lat, long] of the location
        
    """
    geolocator = geocoders.Nominatim(user_agent="Geo Locate")
    location = geolocator.geocode(location)
    
    return [location.latitude, location.longitude]
    

def get_region_code(lat, long):
    """Fetches eBird region code using FCC Area API
    
    Args:
        lat (float): latitude
        long (float): longitude 
    Returns: 
        str: region code
    
    """
    
    # FCC Area API that is publicly available to get codes for a given coordinate.
    census_url = str('https://geo.fcc.gov/api/census/area?lat=' + 
                    str(lat) +
                    '&lon=' +
                    str(long) +
                    '&format=json')
    response = requests.get(census_url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()
    fcc_data = ''
    if response.status_code != 204:
        fcc_data = response.json()
        
    fcc_data = json.loads(response.content)['results'][0]
    
    # region_code follows ISO 3166-2 guidelines. Each complete code consists of two parts:
    # 1. The ISO 3166-1 alpha-2 code of the country.
    # 2. A string of up to three alphanumeric characters, obtained from already existing codes for countries. Since we'll be looking at bird data in the US, we use the in-state FIPS code.
    fips = fcc_data['county_fips']
    region_code = 'US-' + fcc_data['state_code'] + '-' + fips[2] + fips[3] + fips[4]
    
    return region_code