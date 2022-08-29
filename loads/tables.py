"""Inserts values to our two main tables, daily_birds and all_birds.

This module contains two functions:
1. One inserts refreshes the daily_birds table with new data
2. Second creates a staging table from daily_birds and inserts values to the all_birds table, a collection of all previous bird records.
"""
import inspect
from loads import connect_load

def to_daily_table(filename, bucket_name, cursor):
    """Loads data to daily_birds from a specified S3 bucket

    Args:
        filename (str): name of the csv file
        bucket_name (str): name of the S3 bucket to connect and store data to
        cursor (Cursor): a pymysql object that allows for connection to the database

    """
    DAILY_BIRDS = 'daily_birds'
    delete_query = "DELETE FROM daily_birds;"
    cursor.execute(delete_query)
    
    connect_load.to_load(filename, bucket_name, cursor, DAILY_BIRDS)
    
    
def to_all_birds_table(cursor):
    """Loads data to birds table from a specified S3 bucket. This function creates a copy of the daily_birds table and applies the following:
    1. Drop obsDt and indexNum
    2. Increment field howMany on duplicate (composite) keys speciesCode and locId when

    Args:
        cursor (Cursor): a pymysql object that allows for connection to the database

    """
    DAILY_BIRDS = 'daily_birds'
    ALL_BIRDS = 'all_birds'
    
    # Create a copy of the daily_birds table and drop obsDt and indexNum variables.
    create_copy_query = inspect.cleandoc(f"""
                                         CREATE TABLE temp_table AS SELECT * FROM {DAILY_BIRDS};""")
    cursor.execute(create_copy_query)
    
    drop_vars_query = inspect.cleandoc(f"""
                                       ALTER TABLE temp_table
                                       DROP COLUMN obsDt,
                                       DROP COLUMN indexNum,
                                       DROP COLUMN locId,
                                       DROP COLUMN locName,
                                       DROP COLUMN lat,
                                       DROP COLUMN lng,
                                       DROP COLUMN locationPrivate;""")
    cursor.execute(drop_vars_query)
    
    # Insert daily data to all_birds table
    insert_query = inspect.cleandoc(f"""
                                    INSERT INTO {ALL_BIRDS}
                                    SELECT * 
                                    FROM temp_table
                                    ON DUPLICATE KEY UPDATE {ALL_BIRDS}.howMany = {ALL_BIRDS}.howMany + temp_table.howMany;""")
    cursor.execute(insert_query)
    
    # Drop temp_table after insertion is complete
    drop_temp_query = "DROP TABLE temp_table"
    cursor.execute(drop_temp_query)