"""Gets bird data from eBird.

This module contains functions that connect to the eBird API and fetch data from the eBird database. Data from the API call is converted to a pandas DataFrame for easier manipulation and conversion to csv.
    
"""
from distutils.command.config import config
from ebird.api import get_observations
import pandas as pd
import datetime as dt
import configparser
import os

def get_name(frequency):
    """Gets name for bird data file. Has the following structure:
    bird_data + CURRENT_YEAR + WEEK_NUM, where
    WEEK_NUM = the week number of the current day in which the function is being run
    
    Args:
        frequency (int): the number of days back to fetch observations. (default: 14; values: 1-30)
    Returns:
        String: the data file name
        
    """
    today = dt.date.today()
    week_ago = today - dt.timedelta(days=7)
    
    
    if (frequency == 1):
        res = 'bird_data_' + str(today) + '.csv'
    else:
        res = 'bird_data_' + str(week_ago) + '_' + str(today) + '.csv'
    
    return res

def get_data(regionCode, frequency):
    """Fetches weekly bird data by calling a GET request from eBird API and converts the request to a CSV
    
    Args:
        regionCode (str): region code for a given location
        frequency (int): the number of days back to fetch observations. (default: 14; values: 1-30)
    Returns:
        DataFrame: DataFrame of the bird data
        
    """
    # Get API_KEY located in config.ini
    config = configparser.ConfigParser()
    # DELETEEEE LATER!!!!!!
    config_file_path = r'/Users/janekim/Developer/bird proj/birds/config.ini'
    config.read(config_file_path)
    API_KEY = config.get('ebird', 'API_KEY')
        
    records = get_observations(API_KEY, regionCode, back=frequency)
    df = pd.DataFrame(records)
    
    return df