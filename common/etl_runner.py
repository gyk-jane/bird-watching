"""Runs the ETL process."""

import sys
sys.path.append(".")

import datetime
import pandas as pd
from extracts import ebird_api, region
from transforms import transform
from loads import connect_load, tables

def etl_main():
    # Extract
    location = "Los Angeles, California"
    lat_long = region.get_lat_long(location)
    region_code = region.get_region_code(lat_long[0], lat_long[1])
    time = datetime.datetime.now() 
    print(f"Region code: {region_code}")
    print(f"Time: {time}")
    print(f"Extracting bird data from {location}...")

    frequency = 1
    region_code = "US-CA-037"
    filename = ebird_api.get_name(frequency)
    df = ebird_api.get_data(region_code, frequency)

    # Transform
    df = transform.remove_invalids(df)
    transform.convert_to_csv(df, filename)

    # Load
    bucket_name = "birds-around-my-area"
    connect_load.to_bucket(filename, bucket_name)
    cursor = connect_load.connect_to_tables()

    tables.to_daily_table(filename, bucket_name, cursor)
    tables.to_all_birds_table(cursor)

    cursor.close()
    print("ETL process completed.")

# etl_main()