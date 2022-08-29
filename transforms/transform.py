"""Cleanse and convert bird data from the eBird API call.

Bird data is a pandas DataFrame. There are two functions in this module:
1. Function for cleansing data
2. Function for converting DataFrame to csv.
 
"""
import pandas 

def remove_invalids(df):
    """Removes any records that are invalid (obsValid = FALSE)
    
    Args:
        df (DataFrame): DataFrame of retrieved eBird data
    Returns
        df (DataFrame): cleansed DataFrame
        
    """
    return df.drop(df[df.obsValid=='FALSE'].index)

def convert_to_csv(df, filename):
    """Converts dataframe to csv. This function should be run after remove_invalids() is run.
    
    Args:
        df (DataFrame): DataFrame of retrieved eBird data
        filename (str): filename taken from extracts.getName()
        
    """
    df.to_csv(filename, encoding='utf-8-sig', sep=';')